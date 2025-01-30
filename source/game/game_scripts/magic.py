import pygame
from data.settings import *
from source.game.game_scripts.game_effects import ParticleEffect
from random import randint


class Magic:
    def __init__(self):
        self.animation_flame = pygame.image.load("data/images/sprites/magic/flame/fire_attack.png").convert_alpha()
        self.animation_heal = pygame.image.load("data/images/sprites/magic/heal/heal_attack.png").convert_alpha()

    def heal(self, player, strength, cost):
        if player.energy >= cost:
            player.health += strength
            player.energy -= cost
            if player.health >= player.stats["health"]:
                player.health = player.stats["health"]
            return True
        return False

    def flame(self, player, cost, groups):
        if player.energy >= cost:
            player.energy -= cost

            player_direction = player.status.split("_")[0]

            if player_direction == "right":
                flame_direction = pygame.math.Vector2(1, 0)
            elif player_direction == "left":
                flame_direction = pygame.math.Vector2(-1, 0)
            elif player_direction == "up":
                flame_direction = pygame.math.Vector2(0, -1)
            elif player_direction == "down":
                flame_direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):
                offset_x = (flame_direction.x * i) * TILESIZE
                offset_y = (flame_direction.y * i) * TILESIZE
                if flame_direction.x:  # ЕСЛИ ПОЛОЖЕНИЕ ГОРИЗОНТАЛЬНОЕ
                    offset_y = 0
                else:  # ИНАЧЕ (если вертикальное)
                    offset_x = 0
                x = player.rect.centerx + offset_x + randint(-20, 20)
                y = player.rect.centery + offset_y + randint(-20, 20)
                ParticleEffect((x, y), self.animation_flame, groups, 24)
