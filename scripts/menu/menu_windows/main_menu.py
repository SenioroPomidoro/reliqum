import sys
import pygame
import pygame_gui
import pprint

from scripts.menu.menu_windows.user_interfaces.main_ui import load_main_ui
from scripts.menu.menu_windows.user_interfaces.load_game_menu_ui import load_game_menu_ui
from scripts.menu.menu_windows.user_interfaces.new_game_ui import new_game_menu_ui
from scripts.menu.menu_windows.user_interfaces.settings_ui import load_settings_ui
from scripts.menu.menu_windows.user_interfaces.statistics_ui import load_statistics_menu_ui


# КЛАСС ОКНА ГЛАВНОГО МЕНЮ
class MainMenu:
    def __init__(self, w, h, music=None):
        """Инициализация объекта класса окна главного меню"""

        self.fullscreen = False
        self.background_color = "#483c32"
        self.w, self.h = self.size = w, h

        self.click = pygame.mixer.Sound("data/sounds/click.mp3")

        if music is None:
            self.music = pygame.mixer.Sound("data/sounds/main_music.mp3")
        else:
            self.music = music

        self.custom_font = pygame.font.Font("data/fonts/base_font.ttf", 30)
        self.window_surface = pygame.display.set_mode(self.size)
        load_main_ui(self)

    def start_exit_dialog(self):
        """Открытие окна выхода из игры"""
        self.exit_dialog = pygame_gui.windows.UIConfirmationDialog(
            rect=pygame.Rect((self.w / 3, self.h / 4), (self.w / 3, self.h / 4)),
            manager=self.manager,
            window_title="Подтверждение выхода из игры",
            action_long_desc="ВЫ УВЕРЕНЫ, ЧТО ХОТИТЕ ВЫЙТИ ИЗ ИГРЫ?",
            action_short_name="ДА",
            blocking=True  # БЛОКИРОВКА ЛЮБОГО НАЖАТИЯ ДО РЕАКЦИИ НА ВСПЛЫВАЮЩЕЕ ОКНО
        )
        self.exit_dialog.cancel_button.set_text("НЕТ")
        self.menu = self

    def start_menu(self):
        """Запуск главного меню и его особенности"""

        background = pygame.Surface(self.size)
        background.fill(pygame.Color(self.background_color))

        self.music.play(100)
        self.music_playing = True

        clock = pygame.time.Clock()
        running = True
        while running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.start_exit_dialog()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F4:
                        if self.fullscreen:
                            pygame.display.set_mode(self.size, pygame.SCALED)
                        else:
                            pygame.display.set_mode(self.size, pygame.FULLSCREEN)
                        self.fullscreen = not self.fullscreen

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:
                        running = False

                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        self.click.play()
                        if event.ui_element == self.exit_button:
                            self.start_exit_dialog()

                        if event.ui_element == self.back_button:
                            load_main_ui(self)

                        if event.ui_element == self.settings_button:
                            load_settings_ui(self)
                            self.label = False

                        if event.ui_element == self.load_game_button:
                            load_game_menu_ui(self)
                            self.label = False

                        if event.ui_element == self.new_game_button:
                            new_game_menu_ui(self)
                            self.label = False

                        if event.ui_element == self.statistics_button:
                            load_statistics_menu_ui(self)
                            self.label = False

                self.manager.process_events(event)
            self.manager.update(time_delta)

            self.window_surface.blit(background, (0, 0))
            if self.label:
                label = self.custom_font.render("F4 - ПОЛНЫЙ ЭКРАН", 1, (0, 0, 0))
                self.window_surface.blit(label, (self.w // 90, self.h - self.custom_font.get_height()))
                self.window_surface.blit(self.game_label, (20, 20))
            self.manager.draw_ui(self.window_surface)

            pygame.display.flip()
