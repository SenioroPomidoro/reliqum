import pygame

from source.game.sub_menu_scripts.enemy import Enemy

from source.helping_scripts.imports import import_csv_layout
from source.helping_scripts.imports import import_graphics
from source.game.sub_menu_scripts.player import Player
from source.game.sub_menu_scripts.weapon import Weapon
from source.game.user_interface.game_ui import GameUI
from source.game.sub_menu_scripts.tile import Tile

from data.settings import *


# КЛАСС ИГРОВОГО УРОВНЯ
class Level:
    def __init__(self) -> None:
        """Функция инициализации объекта класса игрового уровня"""
        self.display_surface = pygame.display.get_surface()  # ПОЛУЧЕНИЕ ТЕКУЩЕГО СЛОЯ ДЛЯ ОТРИСОВКИ

        self.passable_sprites = pygame.sprite.Group()  # СПРАЙТЫ, ЗА КОТОРЫМИ ИГРОК МОЖЕТ ПРЯТАТЬСЯ
        self.visible_sprites = Camera()  # ВИДИМЫЕ СПРАЙТЫ
        self.obstacle_sprites = pygame.sprite.Group()  # СПРАЙТЫ, С КОТОРЫМИ У ИГРОКА ПРОИСХОДИТ СТОЛКНОВЕНИЕ

        self.current_attack = None  # СПРАЙТ АТАКИ
        self.attack_sprites = pygame.sprite.Group()  # ГРУППА СПРАЙТОВ АТАКИ
        self.attackable_sprites = pygame.sprite.Group()  # СПРАЙТЫ, КОТОРЫЕ МОЖНО АТАКОВАТЬ

        self.create_map()  # СОЗДАНИЕ КАРТЫ

        self.ui = GameUI()  # ОБЪЕКТ ДЛЯ ОТРИСОВКИ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА

    def create_map(self) -> None:
        """Функция создания карты"""

        # ЗАГРУЗКА РАЗЛИЧНЫХ СЛОЁВ ПЕРВОГО УРОВНЯ
        layouts = {
            "boundary": import_csv_layout("data/game_map_files/map/map_FloorBlocks.csv"),
            "Trees": import_csv_layout("data/game_map_files/map/map_Trees.csv"),
            "Objects": import_csv_layout("data/game_map_files/map/map_Objects.csv"),
            "entities": import_csv_layout("data/game_map_files/map/map_Enemies.csv")
        }
        graphics = import_graphics("data/images/tileset_images")  # ЗАГРУЗКА ИЗОБРАЖЕНИЙ С ГРАФИКОЙ

        # ОТРИСОВКА КАРТЫ
        for style, layout in layouts.items():
            for row_i, row in enumerate(layout):
                for col_i, col in enumerate(row):
                    if col != "-1":
                        x = col_i * TILESIZE
                        y = row_i * TILESIZE

                        # НУЖНЫЙ ЭЛЕМЕНТ НА ИЗОБРАЖЕНИИ С ГРАФИКОЙ
                        required_element = int(col) + 1

                        # ОТРИСОВКА ПРЕПЯТСТВИЙ
                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")

                        # ОТРИСОВКА ДЕРЕВЬЕВ (МОЖЕТ НЕ БЫТЬ)
                        if style == "Trees":
                            w, h = graphics[style].width // 64, graphics[style].height // 64
                            i, j = int((required_element - 1) / w) * 64, (required_element - 1) % w * 64

                            current_surface = graphics[style].subsurface(j, i, 64, 64)
                            Tile((x, y), [self.passable_sprites, self.visible_sprites],
                                 "tree", current_surface, int(col))

                        # ОТРИСОВКА ОБЪЕКТОВ
                        if style == "Objects":
                            w, h = graphics[style].width // 64, graphics[style].height // 64
                            i, j = int((required_element - 1) / w) * 64, (required_element - 1) % w * 64

                            current_surface = graphics[style].subsurface(j, i, 64, 64)
                            Tile((x, y), [self.passable_sprites, self.visible_sprites],
                                 "object", current_surface, int(col))

                        if style == "entities":
                            if required_element == 639:
                                # СОЗДАНИЕ ИГРОКА
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic
                                )
                            else:
                                if required_element == 640:
                                    monster_name = "Eye"
                                if required_element == 638:
                                    monster_name = "Bamboo"
                                Enemy(monster_name,
                                      (x, y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player)

    def create_attack(self) -> None:
        """Функция, создающая физическую атаку"""
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost):
        """
        Функия, создающая магическую атаку
        :param style: стиль магии
        :param strength: сила магии
        :param cost: стоимость магии в энергии
        """
        print(style, strength, cost)

    def destroy_attack(self):
        """Функция, отменяющая атаку после её проведение"""
        if self.current_attack is not None:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self):
        """Функция, отвечающая за реализацию взаимодействия между игроком и врагами"""
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type):
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

    def run(self):
        """Функция отрисовки и обновления уровня, отображения игрока"""
        self.visible_sprites.custom_draw(self.player)  # ОТРИСОВКА ИГРОКА
        self.visible_sprites.update()  # ОТРИСОВКА ВИДИМЫХ СПРАЙТОВ
        self.visible_sprites.enemy_update(self.player)
        self.player_attack_logic()
        self.ui.display(self.player)  # ОТРИСОВКА ГРАФИЧЕСКОГО ИНТЕРФЕЙСА В ИГРЕ


# КЛАСС ИГРОВОЙ КАМЕРЫ
class Camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Создание фона
        self.floor_surface = pygame.image.load("data/game_map_files/map/ground.png").convert()
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        # Получеени сдвига камеры
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

        # Отрисовка фона
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # Первичная отрисовка спрайтов (Над которыми будет игрок)
        for sprite in self.sprites():
            if sprite.sprite_id in PASSABLE_IDS:
                offset_rect = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_rect)

        last = []
        # Отрисовка промежуточных спрайтов (Положения игрока регулируется его отношением в пространстве к этому спрайту)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            if sprite.sprite_id in PASSABLE_IDS:
                continue
            if sprite.sprite_type in ["tree", "object"]:  # Отбор спрайтов, под которыми будет игрок
                last.append(sprite)
                continue
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)

        # Отрисовка тех спрайтов, под которыми будет игрок
        for sprite in last:
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    def enemy_update(self, player) -> None:
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and sprite.sprite_type == "enemy"]
        for enemy in enemy_sprites:
            enemy.enemy_update(player)