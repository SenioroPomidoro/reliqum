import pygame

import source.game.game_scripts.player


# КЛАСС ОРУЖИЯ
class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups: list) -> None:
        """
        Инициализация объекта оружия
        :param player: объект игрока, к которому это оружие привязано
        """
        super().__init__(groups)  # ВЫЗОВ РОДИТЕЛЬСКОЙ ФУНКЦИИ ИНИЦИАЛИЗАЦИИ ДЛЯ ЗАПИСИ СПРАЙТА В ГРУППЫ ИЗ groups
        direction = player.status.split("_")[0]  # ОРИЕНТАЦИЯ ИГРОКА (left/right/up/down)

        self.sprite_id = None  # УНИКАЛЬНЫЙ ИДЕНТИФАКТОР СПРАЙТА (нужен этому типу спрайтов, так как проверяется на
        # уровне со всеми остальными)
        self.sprite_type = "Weapon"  # УСТАНОВКА ТИПА СПРАЙТА ОРУЖИЯ

        full_path = f'data/images/sprites/weapons/{player.weapon}/{direction}.png'  # ПОЛНЫЙ ПУТЬ ДО ИЗОБРАЖЕНИЯ
        # ОРУЖИЯ С УЧЁТОМ НАПРАВЛЕНИЯ УДАРА
        self.image = pygame.image.load(full_path).convert_alpha()  # ЗАГРУЗКА ИЗОБРАЖЕНИЯ ПО ПОЛУЧЕННОМУ ПУТИ

        # РАСПОЛОЖЕНИЯ ОРУЖИЙ (всё по центру направлений)
        if direction == "right":
            self.rect = self.image.get_rect(midleft=player.rect.midright + pygame.math.Vector2(0, 12))
        elif direction == "left":
            self.rect = self.image.get_rect(midright=player.rect.midleft + pygame.math.Vector2(0, 12))
        elif direction == "up":
            self.rect = self.image.get_rect(midbottom=player.rect.midtop + pygame.math.Vector2(-10, 0))
        elif direction == "down":
            self.rect = self.image.get_rect(midtop=player.rect.midbottom + pygame.math.Vector2(-10, 0))
