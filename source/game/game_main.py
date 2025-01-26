import pygame

from source.game.sub_game_scripts.game_level import Level


# ГЛАВНЫЙ КЛАСС ИГРОВОГО ОКНА
class Game:
    def __init__(self, w: int, h: int) -> None:
        """
        Инициализация главного игрового окна
        :param w: ширина окна
        :param h: высота окна
        """
        self.pause = False
        self.w, self.h = self.size = w, h  # ЗАПИСЬ РАЗМЕРОВ ОКНА

    def start_game(self) -> None:
        """Запуск игрового окна и его особенности"""
        pygame.display.set_caption("Reliqum")  # УСТАНОВКА НАЗВАНИЯ ИГРОВОГО ОКНА
        window_surface = pygame.display.set_mode(self.size, pygame.FULLSCREEN)  # СОЗДАНИЕ ПОВЕРХНОСТИ ДЛЯ МЕНЮ

        self.level = Level()  # СОЗДАНИЕ ИГРОВОГО УРОВНЯ

        clock = pygame.time.Clock()  # ОПРЕДЕЛЕНИЯ ОБЪЕКТА ЧАСОВ
        running = True  # ОПРЕДЕЛЕНИЕ ПАРАМЕТРА, ОПРЕДЕЛЯЮЩЕГО РАБОТАЕТ МЕНЮ ИЛИ НЕТ
        while running:  # ЦИКЛ ОКНА ГЛАВНОГО МЕНЮ
            for event in pygame.event.get():  # ПОЛУЧЕНИЕ ВОЗНИКАЮЩИХ СОБЫТИЙ В ЦИКЛЕ
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.pause = not self.pause
                if event.type == pygame.QUIT:
                    running = False
            if self.pause:
                continue
            window_surface.fill((0, 0, 0))  # ЗАПОЛНЕНИЕ ОСНОВОГО СЛОЯ ОДНОТОННЫМ ЧЁРНЫМ ЦВЕТОМ
            self.level.run()  # ЗАПУСК УРОВНЯ
            pygame.display.update()  # ОБНОВЛЕНИЯ ИГРОВОГО ЭКРАНА
            clock.tick(60)  # ТИК ЧАСОВ С ЧАСТОТОЙ 60 КАДРОВ В СЕКУНДУ
