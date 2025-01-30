import pygame

from source.main_stream import MainStream
from data.settings import SCREEN_SIZE


# ---------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    """Запуск игры"""
    pygame.init()  # ИНИЦИАЛИЗАЦИЯ pygame
    pygame.mixer.pre_init()  # ИНИЦИАЛИЗАЦИЯ ИНСТРУМЕНТА, ПОЗВОЛЯЮЩЕГО ПРОИГРЫВАТЬ МУЗЫКУ В PYGAME

    main_menu = MainStream(*SCREEN_SIZE)  # СОЗДАНИЕ ОБЪЕКТА ОКНА МЕНЮ
    main_menu.start_menu()  # ЗАПУСК МЕНЮ

# ---------------------------------------------------------------------------------------------------------------------
