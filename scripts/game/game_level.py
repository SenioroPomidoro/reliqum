import pygame
from data.settings import *
from scripts.game.tile import Tile
from scripts.game.player import Player

from scripts.helping_scripts.imports import import_csv_layout
from scripts.helping_scripts.imports import import_graphics
from scripts.game.weapon import Weapon


class Level:
    def __init__(self, surface):
        self.display_surface = pygame.display.get_surface()

        self.passable_sprites = pygame.sprite.Group()  # Спрайты, за которыми игрок может прятаться
        self.visible_sprites = YSortCameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None # спрайт атаки

        self.create_map()

    def create_map(self):
        """Функция создания карты"""
        layouts = {
            "boundary": import_csv_layout("../../data/game_map_files/map/map_FloorBlocks.csv"),
            "Trees": import_csv_layout("../../data/game_map_files/map/map_Trees.csv"),
            "Objects": import_csv_layout("../../data/game_map_files/map/map_Objects.csv")
        }
        graphics = import_graphics("../../data/images/tileset_images")

        for style, layout in layouts.items():
            for row_i, row in enumerate(layout):
                for col_i, col in enumerate(row):
                    if col != "-1":
                        x = col_i * TILESIZE
                        y = row_i * TILESIZE

                        required_element = int(col) + 1

                        if style == "boundary":
                            Tile((x, y), [self.obstacle_sprites], "invisible")

                        if style == "Trees":
                            w, h = graphics[style].width // 64, graphics[style].height // 64
                            i, j = int((required_element - 1) / w) * 64, (required_element - 1) % w * 64

                            current_surface = graphics[style].subsurface(j, i, 64, 64)
                            Tile((x, y), [self.passable_sprites, self.visible_sprites], "tree", current_surface, int(col))

                        if style == "Objects":
                            w, h = graphics[style].width // 64, graphics[style].height // 64
                            i, j = int((required_element - 1) / w) * 64, (required_element - 1) % w * 64

                            current_surface = graphics[style].subsurface(j, i, 64, 64)
                            Tile((x, y), [self.passable_sprites, self.visible_sprites], "object", current_surface, int(col))

        self.player = Player((3300, 4000), [self.visible_sprites], self.obstacle_sprites, self.passable_sprites, self.create_attack, self.destroy_attack)

    def create_attack(self):
        self.current_attack = Weapon(self.player, [self.visible_sprites])

    def destroy_attack(self):
        if self.current_attack is not None:
            self.current_attack.kill()
        self.current_attack = None

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()


class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_w = self.display_surface.get_size()[0] // 2
        self.half_h = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()

        # Создание фона
        self.floor_surface = pygame.image.load("../../data/game_map_files/map/ground.png").convert()
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
