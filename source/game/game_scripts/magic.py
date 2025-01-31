import pygame

from data.settings import *

from source.game.game_scripts.game_effects import ParticleEffect

from random import randint

# ---------------------------------------------------------------------------------------------------------------------


class Magic:

    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self) -> None:
        """Конструктор класса магии"""
        # ПОДГРУЗКА АНИМАЦИЙ ПЛАМЕННОЙ АТАКИ И ЛЕЧЕНИЯ
        self.animation_flame = pygame.image.load("data/images/sprites/magic/flame/fire_attack.png").convert_alpha()
        self.animation_heal = pygame.image.load("data/images/sprites/magic/heal/heal_attack.png").convert_alpha()

    # -----------------------------------------------------------------------------------------------------------------
    def heal(self, player, strength, cost) -> bool:
        """
        Метод, реализующий скилл лечения
        :param player: объект игрока
        :param strength: сила данной магии
        :param cost: стоимость данной магии в очках энергии
        """
        if player.energy >= cost:  # ЕСЛИ У ИГРОКА ХВАТАЕТ ЭНЕРГИИ НА АТАКУ
            player.health += strength  # ИГРОКУ ПРИБАВЛЯЕТСЯ КОЛ-ВО ЗДОРОВЬЕ, РАВНОЕ СИЛЕ ДАННОЙ МАГИИ
            player.energy -= cost  # КОЛИЧЕСТВО ЭНЕРГИИ ИГРОКА УМЕНЬШАЕТСЯ НА СТОИМОСТЬ ДАННОЙ МАГИИ
            if player.health >= player.stats["health"]:  # ЕСЛИ ЗДОРОВЬЕ ИГРОКА БОЛЬШЕ, ЧЕМ ДОПУСТИМОЕ
                player.health = player.stats["health"]  # ОНО ОСТАЁТСЯ МАКСИМАЛЬНЫМ
            return True  # -> True
        return False  # -> False

    # -----------------------------------------------------------------------------------------------------------------
    def flame(self, player, cost, groups):
        """
        Метод, реализующий скилл удара огнём
        :param player: объект игрока
        :param cost: стоимость данной магии в очках энергии
        :param groups: группы спрайтов, в которых находится эта атака
        """
        if player.energy >= cost:  # ЕСЛИ ЭНЕРГИИ ХВАТАЕТ ДЛЯ АТАКИ
            player.energy -= cost  # ЭНЕРГИЯ УМЕНЬШАЕТСЯ

            player_direction = player.status.split("_")[0]  # НАПРАВЛЕНИЕ ДВИЖЕНИЯ ИГРОКА

            # УСТАНОВКА НАПРАВЛЕНИЯ АТАКИ
            if player_direction == "right":  # ДЛЯ ПРАВОГО НАПРАВЛЕНИЯ
                flame_direction = pygame.math.Vector2(1, 0)
            elif player_direction == "left":  # ДЛЯ ЛЕВОГО НАПРАВЛЕНИЯ
                flame_direction = pygame.math.Vector2(-1, 0)
            elif player_direction == "up":  # ДЛЯ ВЕРХНЕГО НАПРАВЛЕНИЯ
                flame_direction = pygame.math.Vector2(0, -1)
            elif player_direction == "down":  # ДЛЯ НИЖНЕГО НАПРАВЛЕНИЯ
                flame_direction = pygame.math.Vector2(0, 1)

            for i in range(1, 6):  # СПАВН СПРАЙТОВ ОГОНЬКОВ
                offset_x = (flame_direction.x * i) * TILESIZE  # СДВИГ СПРАЙТОВ (для реалистики) ПО ИКСАМ
                offset_y = (flame_direction.y * i) * TILESIZE  # ПО ИГРИКАМ

                # ОТКЛЮЧЕНИЕ РАЗБРОСА В НАПРАВЛЕНИИ НЕСООТВЕТСВУЮЩЕМ АТАКЕ
                if flame_direction.x:
                    offset_y = 0
                else:
                    offset_x = 0

                x = player.rect.centerx + offset_x + randint(-20, 20)  # ПОЛОЖЕНИЕ АТАКИ ПО ИКСАМ
                y = player.rect.centery + offset_y + randint(-20, 20)  # ПОЛОЖЕНИЕ АТАКИ ПО ИГРИКАМ

                ParticleEffect((x, y), self.animation_flame, groups, 24)  # СПАВН ЭФФЕКТА АТАКИ

# ---------------------------------------------------------------------------------------------------------------------
