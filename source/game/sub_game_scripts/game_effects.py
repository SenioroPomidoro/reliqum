import pygame


# КЛАСС ВИЗУАЛЬНЫХ ЭФФЕКТОВ
class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, groups, box_size):
        """
        Конструктор объектов класса визуальных эффектов
        :param pos: позиция эффекта
        :param animation: анимация эффекта (по кадрам)
        :param groups: группы спрайтов, в которых будет находится эффект
        """
        super().__init__(groups)

        self.sprite_type = "magic"
        self.sprite_id = None
        self.box_size = box_size

        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames.subsurface((int(self.frame_index) * box_size, 0, box_size, box_size))
        self.rect = self.image.get_rect(center=pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= self.frames.width / self.box_size:
            self.kill()
        else:
            self.image = self.frames.subsurface((int(self.frame_index) * self.box_size, 0,
                                                 self.box_size, self.box_size))

    def update(self):
        self.animate()
