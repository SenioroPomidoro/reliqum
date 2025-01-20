import pygame
from scripts.helping_scripts.chain import main_menu

if __name__ == '__main__':
    """Запуск игры"""
    pygame.init()  # Инициализация pygame

    pygame.mixer.pre_init()  # Инициализация инструмента, позволяющего проигрывать музыку в pygame
    main_menu = main_menu(1400, 900)  # Создание объекта окна меню
    main_menu.start_menu()  # Старт меню
