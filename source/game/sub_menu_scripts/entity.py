import pygame
from math import sin


# КЛАСС-НАСЛЕДНИК ЖИВОГО СУЩЕСТВА (игрок/враг)
class Entity(pygame.sprite.Sprite):
    def __init__(self, groups) -> None:
        super().__init__(groups)
        self.frame_index = 0  # ИНДЕКС ТОГО КАДРА, КОТОРЫЙ ПРОИГРЫВАЕТСЯ В ДАННЫЙ МОМЕНТ
        self.animation_speed = 0.15  # СКОРОСТЬ АНИМАЦИИ
        self.direction = pygame.math.Vector2()  # НАПРАВЛЕНИЕ ДВИЖЕНИЯ ИГРОКА

    def collision(self, direction: str) -> None:
        """
        Функция для обработки столкновений
        :param direction: направление по которому происходит столкновению спрайтов
        """
        if direction == "horizontal":  # ОБРАБОТКА СТОЛКНОВЕНИЙ ПО ГОРИЗОНТАЛИ
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # ДВИЖЕНИЕ ВПРАВО
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # ДВИЖЕНИЯ ВЛЕВО
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":  # ОБРАБОТКА СТОЛКНОВЕНИЙ ПО ВЕРТИКАЛИ
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # ДВИЖЕНИЕ ВНИЗ
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # ДВИЖЕНИЕ ВВЕРХ
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed: int) -> None:
        """
        Функция, вызывающая движения игрока
        :param speed: СКОРОСТЬ ДВИЖЕНИЯ ИГРОКА
        """

        # МОМЕНТУ НИЖЕ СТОИТЬ УДЕЛИТЬ ЧУТЬ БОЛЬШЕ ВНИМАНИЯ: ЕСЛИ У НАС ПРОИСХОДИТ ОДНОВРЕМЕННОЕ ПЕРЕМЕЩЕНИЕ И
        # ПО ГОРИЗОНТАЛИ И ПО ВЕРТИКАЛИ МОЖЕТ ВОЗНИКНУТЬ ТАКАЯ ПРОБЛЕМА, КАК НЕСАНКЦИОНИРОВАННОЕ УВЕЛЕЧЕНИЕ СКОРОСТИ
        # В 2 РАЗА ВВИДУ ТОГО, ЧТО МОНСТР ПЕРЕМЕЩАЕТСЯ СРАЗУ НА ДВЕ КЛЕТКИ. ВО ИЗБЕЖАНИЕ ЭТОГО НУЖНО ПРЕДСТАВЛЯТЬ
        # ДВИЖЕНИЕ ПОЛЬЗОВАТЕЛЬ В РАМКАХ НЕКОТОРОЙ ОКРУЖНОСТИ, У КОТОРОЙ ВЕКТОР ОДНОВРЕМЕННОГО ДВИЖЕНИЯ В
        # ВЕРТИКАЛЬ И ГОРИЗОНТАЛЬ БУДЕТ СОСТАВЛЯТЬ УГОЛ С ОСЯМИ В 45 ГРАДУСОВ. ДЛЯ ВЫЧИСЛЕНИЕ КООРДИНАТ ЭТОГО ВЕКТОРА И
        # ИСПОЛЬЗУЕТСЯ МЕТОД .normalize
        if self.direction.magnitude() != 0:  # ЕСЛИ СУЛЧАЕТСЯ ОПИСАННАЯ ВЫШЕ СИТУАЦИЯ ОСУЩЕСТВЛЯЕМ НОРМАЛИЗАЦИЮ ВЕКТОРА
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed  # ПЕРМЕЩАЕМ ХИТБОКС МОНСТРА НА ЗНАЧЕНИЕ СКОРОСТИ (по иксам)
        self.collision("horizontal")  # ПРОВЕРЯЕМ СТОЛКНОВЕНИЯ

        self.hitbox.y += self.direction.y * speed  # ПЕРЕМЕЩАЕМ ХИТБОКС МОНСТРА НА ЗНАЧЕНИЕ СКОРОСТИ (по игрикам)
        self.collision("vertical")  # ПРОВЕРЯЕМ СТОЛКНОВЕНИЯ

        self.rect.center = self.hitbox.center  # ЗАМЕНЯЕМ РАМКУ В КОТОРОЙ НАХОДИТСЯ МОНСТР НА ЕГО ХИТБОКС
        # (т.к. переместили мы его)

    def wave_value(self) -> int:
        """Функция, реализующая механику мерцания при получении урона"""
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        return 0