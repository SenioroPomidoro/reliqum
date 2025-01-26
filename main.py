import pygame

from data.settings import SCREEN_SIZE
from source.menu.menu_windows.main_menu import MainMenu


if __name__ == '__main__':
    """Запуск игры"""
    pygame.init()  # ИНИЦИАЛИЗАЦИЯ pygame

    pygame.mixer.pre_init()  # ИНИЦИАЛИЗАЦИЯ ИНСТРУМЕНТА, ПОЗВОЛЯЮЩЕГО ПРОИГРЫВАТЬ МУЗЫКУ В PYGAME
    main_menu = MainMenu(*SCREEN_SIZE)  # СОЗДАНИЕ ОБЪЕКТА ОКНА МЕНЮ
    main_menu.start_menu()  # ЗАПУСК МЕНЮ
