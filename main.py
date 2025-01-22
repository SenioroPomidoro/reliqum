import pygame
from scripts.helping_scripts.chain import main_menu
from scripts.game.game_main import Game


if __name__ == '__main__':
    """Запуск игры"""
    pygame.init()  # ИНИЦИАЛИЗАЦИЯ pygame

    pygame.mixer.pre_init()  # ИНИЦИАЛИЗАЦИЯ ИНСТРУМЕНТА, ПОЗВОЛЯЮЩЕГО ПРОИГРЫВАТЬ МУЗЫКУ В PYGAME
    main_menu = main_menu(1400, 900)  # СОЗДАНИЕ ОБЪЕКТА ОКНА МЕНЮ
    # main_menu.start_menu()  # ЗАПУСК МЕНЮ

    game = Game(1400, 900)
    game.start_game()
