import pygame

from data.settings import SCREEN_SIZE
from source.helping_scripts.chain import main_menu
from source.game.game_main import Game


if __name__ == '__main__':
    """Запуск игры"""
    pygame.init()  # ИНИЦИАЛИЗАЦИЯ pygame

    pygame.mixer.pre_init()  # ИНИЦИАЛИЗАЦИЯ ИНСТРУМЕНТА, ПОЗВОЛЯЮЩЕГО ПРОИГРЫВАТЬ МУЗЫКУ В PYGAME
    main_menu = main_menu(*SCREEN_SIZE)  # СОЗДАНИЕ ОБЪЕКТА ОКНА МЕНЮ
    # main_menu.start_menu()  # ЗАПУСК МЕНЮ

    game = Game(*SCREEN_SIZE)
    game.start_game()
