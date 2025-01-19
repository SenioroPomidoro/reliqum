import pygame
from data.settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, groups, sprite_type, surface=pygame.Surface((TILESIZE, TILESIZE)), sprite_id=-1):
        super().__init__(groups)

        self.sprite_type = sprite_type
        self.image = surface

        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(topleft=pos)

        self.hitbox = self.rect.inflate(-20, -20)  # От основного ректангла отрезается сверху и снизу по 5 пикселей

        self.sprite_id = sprite_id
