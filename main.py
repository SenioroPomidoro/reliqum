import pygame
from scripts.helping_scripts.chain import main_menu

if __name__ == '__main__':
    pygame.init()

    info = pygame.display.Info()
    w, h = info.current_w, info.current_h

    pygame.mixer.pre_init()
    main_menu = main_menu(1400, 900)
    main_menu.start_menu()
