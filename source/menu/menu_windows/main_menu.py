import sys
import pygame
import pygame_gui
import pprint

from source.menu.menu_windows.user_interface.draw_labels import draw_labels

from source.helping_scripts.imports import import_settings
from source.menu.menu_windows.sub_menu_scripts.settings_menu import write_settings_csv

from source.menu.menu_windows.user_interface.main_ui import load_main_ui
from source.menu.menu_windows.user_interface.load_game_menu_ui import load_game_menu_ui
from source.menu.menu_windows.user_interface.new_game_ui import new_game_menu_ui
from source.menu.menu_windows.user_interface.settings_ui import load_settings_ui
from source.menu.menu_windows.user_interface.statistics_ui import load_statistics_menu_ui


# ГЛАВНЫЙ КЛАСС ОКНА ГЛАВНОГО МЕНЮ
class MainMenu:
    def __init__(self, w, h, music=None):
        """
        Инициализация главного меню
        :param w: ширина экрана
        :param h: высота экрана
        :param music: музыка, проигрывающаяся в меню
        """

        self.fullscreen = False  # РЕЖИМ ЭКРАНА ПО УМОЛЧАНИЮ - ОКОННЫЙ
        self.background_color = "#483c32"
        self.w, self.h = self.size = w, h  # ЗАПИСЬ РАЗМЕРОВ ЭКРАНА

        self.click = pygame.mixer.Sound("data/sounds/menu_sounds/click.mp3")  # ЗВУК КЛИКА

        if music is None:
            self.music = pygame.mixer.Sound("data/sounds/menu_sounds/main_music.mp3")
        else:
            self.music = music

        self.custom_font = pygame.font.Font("data/fonts/base_font.ttf", 40)  # ОПРЕДЕЛЕНИЯ СОБСТВЕННОГО ШРИФТА
        self.window_surface = pygame.display.set_mode(self.size)  # СОЗДАНИЕ ПОВЕРХНОСТИ ДЛЯ МЕНЮ

        self.status = None  # ПЕРЕМЕННАЯ, КОТОРАЯ УКАЗЫВАЕТ НА ТО, КАКОЙ ТИП МЕНЮ СЕЙЧАСТ ОТКРЫТ
        # (главное, настройки и т.д.)

        load_main_ui(self)  # ЗАГРУЗКА ГЛАВНОГО МЕНЮ - ПО УМОЛЧАНИЮ
        import_settings(self)  # ПОЛУЧЕНИЕ НАСТРОЕК ИЗ ФАЙЛА settings.csv И ЗАПИСЬ В АТРИБУТЫ self (ГРОМКОСТЬ МУЗЫКИ)

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

        background = pygame.Surface(self.size)  # ЗАДНИЙ ФОН
        background.fill(pygame.Color(self.background_color))  # ЗАПОЛНЕНИЯ ЗАДНЕГО ФОНА ЗАДАННЫМ ЦВЕТОМ

        self.music.play(100)  # ВКЛЮЧЕНИЕ МУЗЫКИ
        self.music.set_volume(self.main_music_value / 100)  # УСТАНОВКА ГРОМКОСТИ МУЗЫКИ
        self.music_playing = True

        clock = pygame.time.Clock()  # ОПРЕДЕЛЕНИЕ ОБЪЕКТА ЧАСОВ
        running = True  # ОПРЕДЕЛЕНИЕ ПАРАМЕТРА, ОПРЕДЕЛЯЮЩЕГО РАБОТАЕТ МЕНЮ ИЛИ НЕТ
        while running:  # ЦИКЛ ОКНА ГЛАВНОГО МЕНЮ
            time_delta = clock.tick(60) / 1000.0  # ПОЛУЧЕНИЯ ЗНАЧЕНИЯ ЧАСОВ С ПРОШЛОГО ТИКА (60 кадров в секунду)

            for event in pygame.event.get():  # ПОЛУЧЕНИЕ ВОНЗИКАЮЩИХ СОБЫТИЙ В ЦИКЛЕ
                if event.type == pygame.QUIT:  # ОБРАБОТКА ПОПЫТКИ ЗАКРЫТЬ ПРИЛОЖЕНИЕ
                    self.start_exit_dialog()  # ВЫЗЫВАЕТСЯ ДИАЛОГОВОЕ ОКНО С ПОДТВЕРЖДЕНИЕМ ВЫХОДА

                if event.type == pygame.KEYDOWN:  # ОБРАБОТКА СОБЫТИЙ НАЖАТИЯ НА КЛАВИШИ
                    if event.key == pygame.K_F4:  # F4 - СМЕНА РЕЖИМА ЭКРАНА (полноэкранный/оконный)
                        if self.fullscreen:
                            pygame.display.set_mode(self.size, pygame.SCALED)
                        else:
                            pygame.display.set_mode(self.size, pygame.FULLSCREEN)
                        self.fullscreen = not self.fullscreen

                if event.type == pygame.USEREVENT:  # ЕСЛИ ПОЛУЧЕНО ПОЛЬЗОВАТЕЛЬСКОЕ СОБЫТИЕ (в том числе и
                    # любое из тех, что может быть получено в библиотеке для оформления ui pygame_gui)
                    if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:  # ОБРАБОТКА СДВИГА СЛАЙДЕРА
                        if event.ui_element == self.main_menu_music_slider:  # ИЗМЕНЕНИЕ ГРОМКОСТИ МУЗЫКИ В МЕНЮ
                            self.temprorary_main_music_val = self.main_menu_music_slider.get_current_value()
                        if event.ui_element == self.game_music_slider:  # ИЗМЕНЕНИЕ ГРОМКОСТИ МУЗЫКИ В ИГРЕ
                            self.temprorary_ingame_music_val = self.game_music_slider.get_current_value()

                    if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:  # ОБРАБОТКА ПОДТВЕРЖДЕНИЯ ВЫХОДА
                        running = False  # ЦИКЛ ЗАВЕРШАЕТСЯ

                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:  # ОБРАБОТКА СОБЫТИЙ НАЖАТИЯ НА КНОПКИ
                        self.click.play()  # ПРОИГРЫВАНИЕ ЗВУКА НАЖАТИЯ НА КНОПКУ

                        if event.ui_element == self.exit_button:  # ОБРАБОТКА НАЖАТИЯ НА КНОПКУ ВЫХОДА
                            self.start_exit_dialog()  # ЗАПУСК ДИАЛОГА ПОДТВЕРЖДЕНИЯ ВЫХОДА

                        if event.ui_element == self.back_button:  # НАЖАТИЕ НА КНОПКУ ВОЗВРАЩЕНИЯ В ГЛ. МЕНЮ
                            load_main_ui(self)  # ЗАПУСК ГЛАВНОГО МЕНЮ

                        if event.ui_element == self.settings_button:  # НАЖАТИЕ НА КНОПКУ ПЕРЕХОДА В НАСТРОЙКИ
                            load_settings_ui(self)  # ЗАПУСК ОКНА НАСТРОЕК

                        if event.ui_element == self.load_game_button:  # НАЖАТИЕ НА КНОПКУ ПЕРЕХОДА В ОКНО ЗАГРУЗКИ ИГРЫ
                            load_game_menu_ui(self)  # ЗАПУСК ОКНА ЗАГРУЗКИ ИГРЫ

                        if event.ui_element == self.new_game_button:  # НАЖАТИЕ НА КНОПКУ ПЕРЕХОДА В ОКНО СОЗДАНИЯ ИГРЫ
                            new_game_menu_ui(self)  # ЗАПУСК ОКНА СОЗДАНИЯ НОВОЙ ИГРЫ

                        if event.ui_element == self.statistics_button:  # НАЖАТИЕ НА КНОПКУ ПЕРЕХОЖА В ОКНО СТАТИСТИКИ
                            load_statistics_menu_ui(self)  # ЗАПУСК ОКНА СО СТАТИСТИКОЙ

                        if event.ui_element == self.save_button:  # НАЖАТИЕ НА КНОПКУ СОХРАНЕНИЯ В ОКНЕ НАСТРОЕК
                            write_settings_csv(self)  # ЗАПИСЬ ИМЕЮЩИХСЯ ИЗМЕНЕНИЙ В ФАЙЛ С НАСТРОЙКАМИ
                            self.music.set_volume(self.main_music_val / 100)  # УСТАНОВКА НОВОЙ ГРОМКОСТИ МУЗЫКИ
                            self.save_button.set_text("УСПЕШНО СОХРАНЕНО")  # ПОДТВЕРЖДЕНИЕ СОХРАНЕНИЯ НА КНОПКЕ

                self.manager.process_events(event)  # ПЕРЕДАЧА СОБЫТИЯ МЕНЕДЖЕРУ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
            self.manager.update(time_delta)  # ОБНОВЛЕНИЕ МЕНЕДЖЕРА ГРАФИЧЕСКОГО ИНТЕРФЕЙСА

            self.window_surface.blit(background, (0, 0))  # ЗАПОЛНЕНИЕ ОСНОВНОГО СЛОЯ ФОНОМ

            draw_labels(self)  # ОТРИСОВКА ТЕКСТОВЫХ ЧАСТЕЙ ОКНА

            self.manager.draw_ui(self.window_surface)  # ОТРИСОВКА ЧАСТЕЙ ОКНА, ОТВЕЧАЮЩИХ ЗА ГРАФИЧЕСКИЙ ИНТЕРФЕЙС
            pygame.display.flip()  # ОБНОВЛЕНИЕ ОКНА
