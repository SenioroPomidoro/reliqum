import pygame
import pygame_gui

from data.settings import *

from source.menu.menu_scripts.settings_scripts import slider_moved_process
from source.menu.menu_scripts.main_scripts import button_pressed_process
from source.menu.menu_scripts.main_scripts import start_exit_dialog
from source.menu.menu_scripts.main_scripts import keydown_process

from source.menu.user_interface.main_ui import load_main_ui

from source.helping_scripts.imports import import_music_settings
from source.helping_scripts.races_append import append_result
from source.helping_scripts.draw_labels import draw_labels
from source.helping_scripts.load_sounds import load_music

from source.game.user_interface.game_ui import load_end_ui
from source.game.game_scripts.game_level import Level

# ---------------------------------------------------------------------------------------------------------------------


# КЛАСС ГЛАВНОГО ИГРОВОГО ПОТОКА
class MainStream:
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, w, h):
        """
        Инициализация главного меню
        :param w: ширина экрана
        :param h: высота экрана
        :param music: музыка, проигрывающаяся в меню
        """
        # ===================
        self.fullscreen = False  # РЕЖИМ ЭКРАНА ПО УМОЛЧАНИЮ - ОКОННЫЙ
        self.w, self.h = self.size = w, h  # ЗАПИСЬ РАЗМЕРОВ ЭКРАНА
        self.status = None  # СТАТУС ВКЛЮЧЕНО НА ДАННЫЙ МОМЕНТ ЭКРАНА (для отрисовки) ПО УМОЛЧАНИЮ - None
        # ===================
        load_music(self)  # ЗАГРУЗКА МУЗЫКИ
        # ===================
        self.custom_font = pygame.font.Font("data/fonts/base_font.ttf", 40)  # ОПРЕДЕЛЕНИЕ СОБСТВЕННОГО ШРИФТА
        self.custom_font_small = pygame.font.Font("data/fonts/base_font.ttf", size=25)  # ШРИФТ МЕНЬШЕГО РАЗМЕРА
        self.window_surface = pygame.display.set_mode(self.size)  # СОЗДАНИЕ ЭКРАННОЙ ПОВЕРХНОСТИ ДЛЯ МЕНЮ
        # ===================
        self.import_music_settings = import_music_settings
        self.import_music_settings(self)  # ПОЛУЧЕНИЕ НАСТРОЕК ИЗ ФАЙЛА settings.csv
        load_main_ui(self)  # ЗАГРУЗКА ГЛАВНОГО МЕНЮ - ПО УМОЛЧАНИЮ
        # И ЗАПИСЬ В АТРИБУТЫ self (ГРОМКОСТЬ МУЗЫКИ)
        # ===================
    # -----------------------------------------------------------------------------------------------------------------

    def start_menu(self) -> None:
        """Запуск основного игрового потока"""
        # ===================
        # УСТАНОВКА ИКОНКИ ИГРЫ
        pygame.display.set_icon(pygame.image.load("data/images/main_images/game_icon.png"))
        # ===================
        self.background = pygame.Surface(self.size)  # ЗАДНИЙ ФОН
        self.background.fill(pygame.Color(BG_COLOR))  # ЗАПОЛНЕНИЯ ЗАДНЕГО ФОНА ЗАДАННЫМ ЦВЕТОМ
        # ===================
        self.level_type = 0  # ТИП УРОВНЯ: 0 - ПЕРВЫЙ, 1 - ВТОРОЙ
        self.level_1 = Level()  # ЗАГРУЗКА ПЕРВОГО УРОВНЯ
        self.level_2 = Level(1)  # ЗАГРУЗКА ВТОРОГО УРОВНЯ
        self.levels = [self.level_1, self.level_2]  # СПИСОК ИЗ ДВУХ УРОВНЕЙ
        # ===================
        self.is_game_started = False  # ЗАПУЩЕНА ЛИ ИГРА
        self.is_game_paused = False  # ПОСТАВЛЕНА ЛИ ИГРА НА ПАУЗУ
        self.is_game_ended = False  # ЗАКОНЧИЛАСЬ ЛИ ИГРА (проиграл игрок/выйграл)
        self.win = False  # ПОБЕДИЛ ЛИ ИГРОК
        self.lose = False  # ПРОИГРАЛ ЛИ ИГРОК
        # ===================
        self.clock = pygame.time.Clock()  # ОПРЕДЕЛЕНИЕ ОБЪЕКТА ЧАСОВ
        # ===================

        # -------------------------------------------------------------------------------------------------------------
        self.running = True  # ОПРЕДЕЛЕНИЕ ПАРАМЕТРА, ОПРЕДЕЛЯЮЩЕГО ЗАПУЩЕНО ПРИЛОЖЕНИЕ ИЛИ НЕТ
        while self.running:  # ГЛАВНЫЙ ЦИКЛ ИГРЫ
            self.update_time()  # ОБНОВЛЕНИЕ ИГРОВОГО ВРЕМЕНИ (если игрок находится в каком-то из уровней)

            self.event_handler()  # ОБРАБОТКА ПОСТУПАЮЩИХ СОБЫТИЙ

            self.main_render()  # ОТРИСОВКА ЭКРАНА

            self.check_end_game()  # ПРОВЕРКА ИГРЫ НА ВЫИГРЫШ / ПРОИГРЫШ

            pygame.display.update()  # ОБНОВЛЕНИЕ ОКНА
        # -------------------------------------------------------------------------------------------------------------

    # -----------------------------------------------------------------------------------------------------------------
    def update_time(self) -> None:
        """Метод, обновляющий игровое время в процессе забега"""
        self.time_delta = self.clock.tick(FPS) / 1000.0  # ПОЛУЧЕНИЯ ПРОШЕДШЕГО ВРЕМЕНИ С ПРОШЛОГО ТИКА ИГРОВЫХ ЧАСОВ
        if self.is_game_started and not self.is_game_ended:  # ОБНОВЛЕНИЕ ИГРОВОГО ТАЙМЕРА, ЕСЛИ ЗАПУЩЕН ИГРОВОЙ УРОВЕНЬ
            if not self.level_type:  # ЕСЛИ ТИП ИГРОВОГО УРОВНЯ РАВЕН 0 (начальный уровень)
                self.level_1.game_time += self.time_delta  # ОБНОВЛЕНИЕ ВРЕМЕНИ НА НАЧАЛЬНОМ УРОВНЕ
            else:  # ИНАЧЕ (уровень с боссом)
                self.level_2.game_time += self.time_delta  # ОБНОВЛЕНИЕ ВРЕМЕНИ НА УРОВЕН С БОССОМ

    # -----------------------------------------------------------------------------------------------------------------
    def event_handler(self) -> None:
        """Метод, перебирающий и обрабатывающий поступающие в главный цикл игры события"""
        for event in pygame.event.get():  # ПОЛУЧЕНИЕ СОБЫТИЙ
            if event.type == pygame.QUIT:  # ПОПЫТКА ВЫХОДА
                start_exit_dialog(self)  # ВЫЗЫВАЕТСЯ ДИАЛОГОВОЕ ОКНО С ПОДТВЕРЖДЕНИЕМ ВЫХОДА

            if event.type == pygame.KEYDOWN:  # ОБРАБОТКА СОБЫТИЙ НАЖАТИЯ НА КЛАВИШИ
                keydown_process(self, event, self.level_1.player)

            if event.type == pygame.USEREVENT:  # ОБРАБОТКА ПОЛЬЗОВАТЕЛЬСКОГО СОБЫТИЯ (в частности из pygame_gui)
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:  # ОБРАБОТКА СДВИГА СЛАЙДЕРА
                    slider_moved_process(self, event)
                if event.user_type == pygame_gui.UI_CONFIRMATION_DIALOG_CONFIRMED:  # ОБРАБОТКА ВЫХОДА
                    self.running = False  # ГЛАВНЫЙ ЦИКЛ ИГРЫ ЗАВЕРШАЕТСЯ (закрытие приложения)
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:  # ОБРАБОТКА СОБЫТИЙ НАЖАТИЯ НА КНОПКИ
                    button_pressed_process(self, event)
            self.manager.process_events(event)  # ПЕРЕДАЧА СОБЫТИЯ МЕНЕДЖЕРУ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА

    # -----------------------------------------------------------------------------------------------------------------
    def check_end_game(self) -> None:
        """Метод, осуществляющий проверку того, закончилась ли игра (умер игрок или победил)"""
        if self.level_2.check_win() and not self.win:  # ЕСЛИ ИГРОК ПОБЕЖДАЕТ
            # ===================
            self.is_game_paused = True  # ИГРА СТАВИТСЯ НА ПАУЗУ
            self.win = True  # ИГРОК ПОБЕЖДАЕТ
            self.play_time = self.level_2.game_time  # УСТАНАВЛИВАЕТСЯ ИГРОВОЕ ВРЕМЯ
            self.killed = 17  # РАЗ ИГРОК ПОБЕДИЛ, ТО ОН ОДОЛЕЛ ВСЕХ ВРАГОВ - А ВСЕГО ИХ 17
            # ===================
            append_result(self.play_time, 17)  # ЗАГРУЗКА РЕЗУЛЬТАТА В csv ФАЙЛ С РЕЗУЛЬТАТАМИ ЗАБЕГОВ
            load_end_ui(self)  # ЗАГРУЗКА МЕНЮ ОКОНЧАНИЯ (победа)

        if (self.level_1.check_lose() or self.level_2.check_lose()) and not self.lose:  # ЕСЛИ ИГРОК УМИРАЕТ
            # ===================
            if self.level_1.check_lose():  # ЕСЛИ ИГРОК УМИРАЕТ НА ПЕРВОМ УРОВНЕ
                t = self.level_1.game_time  # БЕРЁТСЯ ВРЕМЯ С ПЕРВОГО УРОВНЯ
            else:  # ИНАЧЕ
                t = self.level_2.game_time  # БЕРЁТСЯ ВРЕМЯ СО ВТОРОГО УРОВНЯ
            # ===================
            self.is_game_paused = True  # ИГРА СТАВИТСЯ НА ПАУЗУ
            self.lose = True  # ИГРОК ПРОИГРЫВАЕТ
            self.play_time = t  # УСТАНАВЛИВАЕТСЯ ТЕКУЩЕЕ ИГРОВОЕ ВРЕМЯ
            self.killed = self.level_1.player.kill_counter  # КОЛИЧЕСТВО УБИТЫХ ВРАГОВ
            # ===================
            append_result(self.play_time, self.killed)  # ЗАГРУЗКА РЕЗУЛЬТАТА В csv ФАЙЛ С РЕЗУЛЬТАТАМИ ЗАБЕГОВ
            load_end_ui(self, False)  # ЗАГРУЗКА МЕНЮ ОКОНЧАНИЯ (пораженеие)

    # -----------------------------------------------------------------------------------------------------------------
    def main_render(self) -> None:
        """Метод, осуществляющий отрисовку тех или иных частей приложения,
         в зависимости от процессов, в нём происходящих"""
        # ===================
        if not self.is_game_started:  # ЕСЛИ ИГРОВОЙ ПРОЦЕСС НЕ НАЧАТ
            self.window_surface.blit(self.background, (0, 0))  # ЗАПОЛНЕНИЕ ОСНОВНОГО СЛОЯ ФОНОМ ГЛАВНОГО МЕНЮ
        # ===================
        draw_labels(self)  # ОТРИСОВКА ДОПОЛНИТЕЛЬНЫХ ЧАСТЕЙ ОКНА (тексты, примечания и т.п.)
        # ===================
        if self.is_game_started and not self.is_game_paused and not self.is_game_ended:  # ЕСЛИ ИГРА В ПРОЦЕССЕ
            self.draw_levels()  # ОТРИСОВКА УРОВНЯ
        # ===================
        # СЛУЧАЙ, КОГДА ИГРА НЕ ЗАПУЩЕНА, ИЛИ ИГРА НА ПАУЗЕ
        if not self.is_game_started or (self.is_game_started and self.is_game_paused):
            self.manager.update(self.time_delta)  # ОБНОВЛЕНИЕ МЕНЕДЖЕРА ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
            self.manager.draw_ui(self.window_surface)  # ОТРИСОВКА ЧАСТЕЙ ОКНА, ОТВЕЧАЮЩИХ ЗА ГРАФИЧЕСКИЙ ИНТЕРФЕЙС
        # ===================

    # -----------------------------------------------------------------------------------------------------------------
    def draw_levels(self) -> None:
        # ===================
        if not self.level_type:  # ЕСЛИ ЭТО ПЕРВЫЙ УРОВЕНЬ
            if not self.is_game_music_playing:  # ЕСЛИ ИГРОВАЯ МУЗЫКА ЕЩЁ НЕ ЗАПУЩЕНА (А СООТВЕТСВЕННО И УРОВЕНЬ)
                self.main_music.stop()  # ОСТАНОВКА МУЗЫКИ ИЗ МЕНЮ
                self.game_music.play(100)  # ВКЛЮЧЕНИЕ ИГРОВОЙ МУЗЫКИ
                self.game_music.set_volume(self.ingame_music_value / 100)  # УСТАНОВКА ГРОМКОСТИ ИГРОВОЙ МУЗЫКИ
                self.is_game_music_playing = True  # МУЗЫКА НА ГЛАВНОМ УРОВНЕ ИГРАЕТ
            self.level_1.run()  # ОТРИСОВКА ПЕРВОГО УРОВНЯ

        else:  # ЕСЛИ ЭТО ВТОРОЙ УРОВЕНЬ
            if not self.is_boss_music_playing:  # ЕСЛИ ИГРОВАЯ МУЗЫКА ЕЩЁ НЕ ЗАПУЩЕНА (А СООТВЕТСВЕННО И БОЙ С БОССОМ)
                self.game_music.stop()  # ОСТАНОВКА МУЗЫКИ С ПЕРВОГО УРОВНЯ
                self.boss_music.play(100)  # ВКЛЮЧЕНИЕ МУЗЫКИ БИТВЫ С БОССОМ
                self.boss_music.set_volume(self.ingame_music_value / 100)  # УСТАНОВКА ГРОМКОСТИ МУЗЫКИ БОССА
                self.is_boss_music_playing = True  # МУЗЫКА БИТВЫ С БОССОМ ИГРАЕТ
                self.is_game_music_playing = False  # МУЗЫКА НА ГЛАВНОМ УРОВНЕ НЕ ИГРАЕТ
            self.level_2.run()  # ОТРИСОВКА ВТОРОГО УРОВНЯ
        # ===================
# ---------------------------------------------------------------------------------------------------------------------
