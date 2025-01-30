import pygame

from source.game.game_scripts.enemy import Enemy

from source.helping_scripts.imports import import_csv_layout
from source.helping_scripts.imports import import_graphics
from source.game.game_scripts.player import Player
from source.game.game_scripts.weapon import Weapon
from source.game.user_interface.game_ui import GameUI
from source.game.game_scripts.tile import Tile

from source.game.game_scripts.game_effects import ParticleEffect

from source.game.game_scripts.magic import Magic


from data.settings import *


# КЛАСС ИГРОВОГО УРОВНЯ
class Level:
    def __init__(self, level_index=0) -> None:
        """
        Функция инициализации объекта класса игрового уровня
        :param level_index: индекс уровня. 0 - уровень с картой основного мира, 1 - карта с боссом
        """
        self.display_surface = pygame.display.get_surface()  # ПОЛУЧЕНИЕ ТЕКУЩЕГО СЛОЯ ДЛЯ ОТРИСОВКИ
        self.level_index = level_index

        if self.level_index:
            map_ = "boss_map"
        else:
            map_ = "map"

        self.passable_sprites = pygame.sprite.Group()  # СПРАЙТЫ, ЗА КОТОРЫМИ ИГРОК МОЖЕТ ПРЯТАТЬСЯ
        self.visible_sprites = Camera(map_)  # ВИДИМЫЕ СПРАЙТЫ
        self.obstacle_sprites = pygame.sprite.Group()  # СПРАЙТЫ, С КОТОРЫМИ У ИГРОКА ПРОИСХОДИТ СТОЛКНОВЕНИЕ

        self.current_attack = None  # СПРАЙТ АТАКИ
        self.attack_sprites = pygame.sprite.Group()  # ГРУППА СПРАЙТОВ АТАКИ
        self.attackable_sprites = pygame.sprite.Group()  # СПРАЙТЫ, КОТОРЫЕ МОЖНО АТАКОВАТЬ

        self.create_map()  # СОЗДАНИЕ КАРТЫ

        self.ui = GameUI()  # ОБЪЕКТ ДЛЯ ОТРИСОВКИ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА

        self.magic = Magic()  # ОБЪЕКТ, ОТВЕЧАЮЩИЙ ЗА ИСПОЛЬЗОВАНИЕ МАГИИ
        self.game_time = 0

    def create_map(self) -> None:
        """Функция создания карты"""

        # ЗАГРУЗКА РАЗЛИЧНЫХ СЛОЁВ ПЕРВОГО УРОВНЯ
        if self.level_index == 0:
            layouts = {
                "boundary": import_csv_layout(F"data/game_map_files/map/map_FloorBlocks.csv"),
                "Trees": import_csv_layout(F"data/game_map_files/map/map_Trees.csv"),
                "Objects": import_csv_layout(F"data/game_map_files/map/map_Objects.csv"),
                "entities": import_csv_layout(F"data/game_map_files/map/map_Enemies.csv"),
                "door_closed": import_csv_layout(F"data/game_map_files/map/map_Doors_closed.csv"),
                "door_open": import_csv_layout(F"data/game_map_files/map/map_Doors_open.csv")
            }
        else:
            layouts = {
                "boundary": import_csv_layout(F"data/game_map_files/boss_map/map_FloorBlocks.csv"),
                "Objects": import_csv_layout(F"data/game_map_files/boss_map/map_Objects.csv"),
                "entities": import_csv_layout(F"data/game_map_files/boss_map/map_Enemies.csv")

                }
        graphics = import_graphics("data/images/tileset_images")  # ЗАГРУЗКА ИЗОБРАЖЕНИЙ С ГРАФИКОЙ

        # ОТРИСОВКА КАРТЫ
        for style, layout in layouts.items():
            for row_i, row in enumerate(layout):
                for col_i, col in enumerate(row):
                    if col != "-1":
                        x = col_i * TILESIZE
                        y = row_i * TILESIZE

                        required_element = int(col) + 1  # НУЖНЫЙ ЭЛЕМЕНТ НА ИЗОБРАЖЕНИИ С ГРАФИКОЙ

                        if style == "boundary":  # ОТРИСОВКА ПРЕПЯТСТВИЙ
                            Tile((x, y), [self.obstacle_sprites], "invisible")

                        if style == "Trees":  # ОТРИСОВКА ДЕРЕВЬЕВ
                            w, h = graphics[style].width // 64, graphics[style].height // 64
                            i, j = int((required_element - 1) / w) * 64, (required_element - 1) % w * 64

                            current_surface = graphics[style].subsurface(j, i, 64, 64)
                            Tile((x, y), [self.passable_sprites, self.visible_sprites],
                                 "tree", current_surface, int(col))

                        if style == "Objects":  # ОТРИСОВКА ОБЪЕКТОВ
                            w, h = graphics[style].width // 64, graphics[style].height // 64
                            i, j = int((required_element - 1) / w) * 64, (required_element - 1) % w * 64

                            current_surface = graphics[style].subsurface(j, i, 64, 64)
                            Tile((x, y), [self.passable_sprites, self.visible_sprites],
                                 "object", current_surface, int(col))

                        if style == "door_open":
                            w, h = graphics["Objects"].width // 64, graphics["Objects"].height // 64
                            i, j = int((required_element - 1) / w) * 64, (required_element - 1) % w * 64

                            current_surface = graphics["Objects"].subsurface(j, i, 64, 64)
                            Tile((x, y), [self.passable_sprites, self.visible_sprites],
                                 "door_open", current_surface, int(col))

                        if style == "door_closed":
                            w, h = graphics["Objects"].width // 64, graphics["Objects"].height // 64
                            i, j = int((required_element - 1) / w) * 64, (required_element - 1) % w * 64

                            current_surface = graphics["Objects"].subsurface(j, i, 64, 64)
                            Tile((x, y), [self.obstacle_sprites, self.visible_sprites],
                                 "door_closed", current_surface, int(col))

                        if style == "entities":  # ОТРИСОВКА СУЩЕСТВ
                            if required_element == 639:  # СОЗДАНИЕ ИГРОКА
                                self.player = Player(
                                    (x, y),
                                    [self.visible_sprites],
                                    self.obstacle_sprites,
                                    self.create_attack,
                                    self.destroy_attack,
                                    self.create_magic
                                )
                                if self.level_index:
                                    self.player.kill_counter = 16
                            else:
                                if required_element == 640:  # МОНСТР-ГЛАЗ
                                    monster_name = "Eye"
                                if required_element == 638:  # БОСС БАМБУК
                                    if self.level_index:
                                        monster_name = "Bamboo"
                                    else:
                                        monster_name = "Eye"
                                Enemy(monster_name,
                                      (x, y),
                                      [self.visible_sprites, self.attackable_sprites],
                                      self.obstacle_sprites,
                                      self.damage_player,
                                      self.trigger_death_particles)

    def create_attack(self) -> None:
        """Функция, создающая физическую атаку"""
        self.current_attack = Weapon(self.player, [self.visible_sprites, self.attack_sprites])

    def create_magic(self, style, strength, cost) -> None:
        """
        Функия, создающая магическую атаку
        :param style: стиль магии
        :param strength: сила магии
        :param cost: стоимость магии в энергии
        """
        if style == "heal":
            if self.magic.heal(self.player, strength, cost):
                ParticleEffect(self.player.rect.center, self.magic.animation_heal, [self.visible_sprites], 64)

        if style == "flame":
            self.magic.flame(self.player, cost, [self.visible_sprites, self.attack_sprites])

    def destroy_attack(self) -> None:
        """Функция, отменяющая атаку после её проведения"""
        if self.current_attack is not None:
            self.current_attack.kill()
        self.current_attack = None

    def player_attack_logic(self) -> None:
        """Функция, отвечающая за получения урона врагами"""
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites:
                        target_sprite.get_damage(self.player, attack_sprite.sprite_type)

    def damage_player(self, amount, attack_type) -> None:
        """Функция, отвечающая за получение урона игроком"""
        if self.player.vulnerable:
            self.player.health -= amount
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()

            frames = pygame.image.load(F"data/images/sprites/attacks/{attack_type}.png").convert_alpha()
            ParticleEffect(self.player.rect.center, frames, [self.visible_sprites], 64)

    def trigger_death_particles(self, pos) -> None:
        frames = pygame.image.load(F"data/images/sprites/death/death.png").convert_alpha()
        ParticleEffect(pos, frames, [self.visible_sprites], 64)

    def check_win(self) -> bool:
        """Функция проверки на победу"""
        if self.player.is_player_win:  # ЕСЛИ ИГРОК ПОБЕДИЛ ГЛАВНОГО БОССА
            return True
        return False

    def check_lose(self) -> bool:
        if self.player.is_player_lose:
            return True
        return False

    def run(self) -> None:
        """Функция отрисовки и обновления уровня, отображения игрока"""
        self.visible_sprites.custom_draw(self.player, is_boss=self.level_index)  # ОТРИСОВКА ИГРОКА
        self.visible_sprites.update()  # ОТРИСОВКА ВИДИМЫХ СПРАЙТОВ
        self.visible_sprites.enemy_update(self.player)  # ОБНОВЛЕНИЯ ПОВЕДЕНИЯ ВРАГОВ
        self.player_attack_logic()  # ПРОВЕРКА АТАКИ ИГРОКОМ
        self.ui.display(self.player, self.game_time)  # ОТРИСОВКА ГРАФИЧЕСКОГО ИНТЕРФЕЙСА В ИГРЕ


# КЛАСС ИГРОВОЙ КАМЕРЫ
class Camera(pygame.sprite.Group):
    def __init__(self, map_) -> None:
        """Функция инициализации камеры"""
        super().__init__()
        self.display_surface = pygame.display.get_surface()  # ПОЛУЧЕНИЕ ИГРОВОЙ КАРТЫ
        self.half_w = self.display_surface.get_size()[0] // 2  # ПОЛОВИНА ОТ ШИРИНЫ
        self.half_h = self.display_surface.get_size()[1] // 2  # ПОЛОВИНА ОТ ВЫСОТЫ
        self.offset = pygame.math.Vector2()  # ВЕКТОР, ОТВЕЧАЮЩИЙ ЗА СДВИГ КАМЕРЫ

        self.floor_surface = pygame.image.load(F"data/game_map_files/{map_}/ground.png").convert()  # ЗАГРУЗКА КАРТЫ
        self.floor_rect = self.floor_surface.get_rect(topleft=(0, 0))

    def custom_draw(self, player, is_boss=False) -> None:
        """
        Функция отрисовки изображения камеры
        :param is_boss: находится ли игрок в локации с боссом (в этом случае нужно, чтобы камера не заходила за стенки
        :param player: объект игрока
        """
        self.offset.x = player.rect.centerx - self.half_w
        self.offset.y = player.rect.centery - self.half_h

        if is_boss:
            if self.offset.x < 0:
                self.offset.x = 0
            if self.offset.x > 517:
                self.offset.x = 517

            if self.offset.y < 0:
                self.offset.y = 0
            if self.offset.y > 1017:
                self.offset.y = 1017

        # ОТРИСОВКА ФОНА
        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.display_surface.blit(self.floor_surface, floor_offset_pos)

        # ПЕРВИЧНАЯ ОТРИСОВКА СПРАЙТОВ (НАД КОТОРЫМИ БУДЕТ ИГРОК)
        for sprite in self.sprites():
            if sprite.sprite_id in PASSABLE_IDS:
                offset_rect = sprite.rect.topleft - self.offset
                self.display_surface.blit(sprite.image, offset_rect)

        last = []  # СЮДА ОТБИРАЮТСЯ СПРАЙТЫ, КОТОРЫЕ БУДУТ РИСОВАТЬСЯ В КОНЦЕ
        # ОТРИСОВКА ПРОМЕЖУТОЧНЫХ СПРАЙТОВ (ПОЛОЖЕНИЯ ИГРОКА РЕГУЛИРУЕТСЯ ЕГО ОТНОШЕНИЕМ В ПРОСТРАНСТВЕ К ЭТОМУ СПРАЙТУ)
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_rect = sprite.rect.topleft - self.offset

            if sprite.sprite_type == "door_open" and player.kill_counter < 15:
                continue

            if sprite.sprite_type == "door_closed":
                if player.kill_counter >= 16:
                    sprite.kill()
                else:
                    self.display_surface.blit(sprite.image, offset_rect)
                continue

            if sprite.sprite_id in PASSABLE_IDS:
                continue

            if sprite.sprite_type in ["tree", "object"]:  # ОТБОР СПРАЙТОВ, ПОД КОТОРЫМИ БУДЕТ ИГРОК
                last.append(sprite)
                continue

            self.display_surface.blit(sprite.image, offset_rect)

        # ОТРИСОВКА ТЕХ СПРАЙТОВ, ПОД КОТОРЫМИ БУДЕТ ИГРОК
        for sprite in last:
            offset_rect = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_rect)

    def enemy_update(self, player) -> None:
        """
        Метод, обновляющий врагов
        :param player:
        """
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, "sprite_type") and
                         sprite.sprite_type == "enemy"]  # ОТБОР СПРАЙТОВ ВРАГОВ
        for enemy in enemy_sprites:  # ВВЫЗОВ  ОДНОИМЁННОГО МЕТОДА.enemy_update У ОБЪЕКТА ВРАГА
            enemy.enemy_update(player)