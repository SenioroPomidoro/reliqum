import sys
import pygame
import pygame_gui
import pprint

from data.settings import *

from source.menu.menu_windows.user_interface.draw_labels import draw_labels
from source.helping_scripts.imports import import_settings
from source.menu.menu_windows.menu_scripts.settings_scripts import write_settings_csv
from source.menu.menu_windows.menu_scripts.main_scripts import start_exit_dialog
from source.menu.menu_windows.menu_scripts.main_scripts import button_pressed_process
from source.menu.menu_windows.menu_scripts.main_scripts import keydown_process
from source.menu.menu_windows.user_interface.main_ui import load_main_ui
from source.game.sub_game_scripts.game_level import Level
from source.menu.menu_windows.menu_scripts.settings_scripts import slider_moved_process


from source.game.user_interface.game_ui import load_end_ui

# ---------------------------------------------------------------------------------------------------------------------


# ГЛАВНЫЙ КЛАСС ОКНА ГЛАВНОГО МЕНЮ
class MainMenu:
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, w, h):
        """
        Инициализация главного меню
        :param w: ширина экрана
        :param h: высота экрана
        :param music: музыка, проигрывающаяся в меню
        """

        self.fullscreen = False  # РЕЖИМ ЭКРАНА ПО УМОЛЧАНИЮ - ОКОННЫЙ
        self.w, self.h = self.size = w, h  # ЗАПИСЬ РАЗМЕРОВ ЭКРАНА

        self.click = pygame.mixer.Sound("data/sounds/menu_sounds/click.mp3")  # ЗВУК КЛИКА
        self.music = pygame.mixer.Sound("data/sounds/menu_sounds/main_music.mp3")

        self.custom_font = pygame.font.Font("data/fonts/base_font.ttf", 40)  # ОПРЕДЕЛЕНИЯ СОБСТВЕННОГО ШРИФТА
        self.window_surface = pygame.display.set_mode(self.size)  # СОЗДАНИЕ ПОВЕРХНОСТИ ДЛЯ МЕНЮ

        load_main_ui(self)  # ЗАГРУЗКА ГЛАВНОГО МЕНЮ - ПО УМОЛЧАНИЮ
        import_settings(self)  # ПОЛУЧЕНИЕ НАСТРОЕК ИЗ ФАЙЛА settings.csv И ЗАПИСЬ В АТРИБУТЫ self (ГРОМКОСТЬ МУЗЫКИ)

    # -----------------------------------------------------------------------------------------------------------------

    def start_menu(self):
        """Запуск главного меню и его особенности"""

        self.background = pygame.Surface(self.size)  # ЗАДНИЙ ФОН
        self.background.fill(pygame.Color(BG_COLOR))  # ЗАПОЛНЕНИЯ ЗАДНЕГО ФОНА ЗАДАННЫМ ЦВЕТОМ

        self.music.play(100)  # ВКЛЮЧЕНИЕ МУЗЫКИ
        self.music.set_volume(self.main_music_value / 100)  # УСТАНОВКА ГРОМКОСТИ МУЗЫКИ

        self.level_type = 0
        self.level_1 = Level()
        self.level_2 = Level(1)
        self.levels = [self.level_1, self.level_2]

        self.is_game_started = False
        self.is_game_paused = False
        self.is_game_ended = False
        self.win = False
        self.lose = False

        self.clock = pygame.time.Clock()  # ОПРЕДЕЛЕНИЕ ОБЪЕКТА ЧАСОВ

        # -------------------------------------------------------------------------------------------------------------
        running = True  # ОПРЕДЕЛЕНИЕ ПАРАМЕТРА, ОПРЕДЕЛЯЮЩЕГО РАБОТАЕТ МЕНЮ ИЛИ НЕТ
        while running:  # ЦИКЛ ОКНА ГЛАВНОГО МЕНЮ
            time_delta = self.clock.tick(FPS) / 1000.0  # ПОЛУЧЕНИЯ ЗНАЧЕНИЯ ЧАСОВ С ПРОШЛОГО ТИКА (60 кадров в секунду)

            if self.is_game_started and not self.is_game_ended:
                if not self.level_type:
                    self.level_1.game_time += time_delta
                else:
                    self.level_2.game_time += time_delta

            for event in pygame.event.get():  # ПОЛУЧЕНИЕ СОБЫТИЙ
                if event.type == pygame.QUIT:  # ПОПЫТКА ВЫХОДА
                    start_exit_dialog(self)  # ВЫЗЫВАЕТСЯ ДИАЛОГОВОЕ ОКНО С ПОДТВЕРЖДЕНИЕМ ВЫХОДА

                if event.type == pygame.KEYDOWN:  # ОБРАБОТКА СОБЫТИЙ НАЖАТИЯ НА КЛАВИШИ
                    keydown_process(self, event, self.level_1.player)

                if event.type == pygame.USEREVENT:  # ОБРАБОТКА ПОЛЬЗОВАТЕЛЬСКОГО СОБЫТИЯ (в частности из pygame_gui)
                    if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:  # ОБРАБОТКА СДВИГА СЛАЙДЕРА
                        slider_moved_process(self, event)
                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:  # ОБРАБОТКА ВЫХОДА
                        running = False  # ЦИКЛ ЗАВЕРШАЕТСЯ
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:  # ОБРАБОТКА СОБЫТИЙ НАЖАТИЯ НА КНОПКИ
                        button_pressed_process(self, event)
                self.manager.process_events(event)  # ПЕРЕДАЧА СОБЫТИЯ МЕНЕДЖЕРУ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА

            if not self.is_game_started:
                self.window_surface.blit(self.background, (0, 0))  # ЗАПОЛНЕНИЕ ОСНОВНОГО СЛОЯ ФОНОМ

            draw_labels(self)  # ОТРИСОВКА ДОПОЛНИТЕЛЬНЫХ ЧАСТЕЙ ОКНА

            if self.is_game_started and not self.is_game_paused and not self.is_game_ended:
                if not self.level_type:
                    self.level_1.run()
                else:
                    self.level_2.run()

            if self.level_2.check_win() and not self.win:
                print("WIN")
                self.is_game_paused = True
                self.win = True
                self.play_time = self.level_2.game_time
                load_end_ui(self)

            if self.levels[self.level_type].check_lose() and not self.lose:
                print("ВМЕР")
                self.is_game_paused = True
                self.lose = True
                self.play_time = self.levels[self.level_type].game_time
                self.killed = self.levels[self.level_type].player.kill_counter
                load_end_ui(self, False)

            if not self.is_game_started or (self.is_game_started and self.is_game_paused):
                self.manager.update(time_delta)  # ОБНОВЛЕНИЕ МЕНЕДЖЕРА ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
                self.manager.draw_ui(self.window_surface)  # ОТРИСОВКА ЧАСТЕЙ ОКНА, ОТВЕЧАЮЩИХ ЗА ГРАФИЧЕСКИЙ ИНТЕРФЕЙС

            pygame.display.update()  # ОБНОВЛЕНИЕ ОКНА
        # -------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
