import pygame

# ---------------------------------------------------------------------------------------------------------------------


# КЛАСС ВИЗУАЛЬНЫХ ЭФФЕКТОВ
class ParticleEffect(pygame.sprite.Sprite):
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, pos, animation_frames, groups, box_size) -> None:
        """
        Конструктор объектов класса визуальных эффектов
        :param pos: позиция эффекта
        :param animation_frames: анимация эффекта (по кадрам) - изображение
        :param groups: группы спрайтов, в которых будет находиться эффект
        :param box_size: кадра эффекта
        """
        super().__init__(groups)  # ПОМЕЩЕНИЕ СПРАЙТОВ В ГРУППЫ groups

        # ЗАПИСЬ НЕКОТОРЫХ ЭЛЕМЕНТОВ В АТРИБУТЫ ОБЪЕКТА
        self.sprite_type = "magic"  # ТИП СПРАЙТА
        self.sprite_id = None  # АЙДИ СПРАЙТА
        self.box_size = box_size  # РАЗМЕРЫ СПРАЙТА
        self.frame_index = 0  # ИНДЕКС СПРАЙТА ПО АНИМАЦИИ
        self.animation_speed = 0.15  # СКОРОСТЬ АНИМАЦИИ
        self.frames = animation_frames  # КАДРЫ АНИМАЦИИ
        self.image = self.frames.subsurface((int(self.frame_index) * box_size, 0, box_size, box_size))  # ПЕРВЫЙ КАДР
        self.rect = self.image.get_rect(center=pos)  # РАСПОЛОЖЕНИЕ КАДРА НА ЭКРАНЕ

    # -----------------------------------------------------------------------------------------------------------------
    def animate(self) -> None:
        """Метод, анимиирующий объект визуального эффекта"""
        self.frame_index += self.animation_speed  # ПРИБАВЛЯЕМ К ЗНАЧЕНИЮ КАДРА СКОРОСТЬ АНИМАЦИИ
        if self.frame_index >= self.frames.width / self.box_size:  # ЕСЛИ АНИМАЦИЯ ЗАВЕРШЕНА
            self.kill()  # УНИЧТОЖАЕМ СПРАЙТ
        else:  # ИНАЧЕ
            self.image = self.frames.subsurface((int(self.frame_index) * self.box_size, 0,
                                                 self.box_size, self.box_size))  # СПАВНИМ ИЗОБРАЖЕНИЕ ТЕКУЩЕГО КАДРА

    # -----------------------------------------------------------------------------------------------------------------
    def update(self) -> None:
        """Метод, обновляющий объект класса визуальных эффектов"""
        self.animate()  # ВЫЗОВ МЕТОДА АНИМАЦИИ

    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
