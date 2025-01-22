import pygame
from data.settings import *


# КЛАСС ДЛЯ ОТРАБОТКИ ПЛИТКИ НА ЭКРАНЕ ИГРЫ
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos: tuple, groups: list, sprite_type: str, surface=pygame.Surface((TILESIZE, TILESIZE)),
                 sprite_id=-1):
        """
        Инициализация объекта плитки
        :param pos: позиция плитки на игровой поверхности
        :param groups: группы спрайтов, в которые эта плитка будет помещаться
        :param sprite_type: тип спрайта (нужен для обработки некоторых особенностей плиток)
        :param surface:  поверхнсоть на которой будет отрисовываться плитка
        :param sprite_id: уникальный номер спрайта (уникальный на набор)
        """
        super().__init__(groups)  # ВЫЗОВ ФУНКЦИИ РОДИТЕЛЬСКОГО КЛАССА СПРАЙТА ДЛЯ ЗАГРУЗКИ ЭТОГО СПРАЙТА В ГРУППЫ
        # СПРАЙТОВ, УКАЗАННЫХ В group

        self.sprite_type = sprite_type  # ЗАПИСЬ ТИПА ПЛИТКИ В ЕЁ АТРИБУТЫ

        self.image = surface  # ЗАПИСЬ ПОВЕРХНОСТИ СПРАЙТА В ЕЁ АТРИБУТЫ
        self.image = pygame.transform.scale(self.image, (64, 64))  # ИЗМЕНЕНИЕ РАЗМЕРА ПОВЕРХНСОТИ ДО РАЗМЕРОВ ПЛИТКИ
        self.rect = self.image.get_rect(topleft=pos)  # ОПРЕДЕЛЕНИЕ ПЛИТКИ В ПРОСТРАНСТВЕ

        self.hitbox = self.rect.inflate(-20, -20)  # ОТ ОСНОВНОГО РЕКТАНГЛА ОТРЕЗАЕТСЯ
        # СВЕРХУ, СПРАВА И СНИЗУ ПО 10 ПИКСЕЛЕЙ

        self.sprite_id = sprite_id  # ЗАПИСЬ УНИКАЛЬНОГО НОМЕРА СПРАЙТА В ЕГО АТРИБУТЫ
