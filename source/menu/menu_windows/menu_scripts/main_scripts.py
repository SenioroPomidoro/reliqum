import pygame_gui
import pygame

from source.menu.menu_windows.menu_scripts.settings_scripts import write_settings_csv
from source.menu.menu_windows.user_interface.settings_ui import load_settings_ui
from source.menu.menu_windows.user_interface.main_ui import load_main_ui
from source.game.user_interface.game_ui import load_pause_ui
from source.game.sub_game_scripts.game_level import Level


# ---------------------------------------------------------------------------------------------------------------------
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
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def button_pressed_process(self, event):
    self.click.play()  # ПРОИГРЫВАНИЕ ЗВУКА НАЖАТИЯ НА КНОПКУ

    if event.ui_element == self.exit_button:  # ОБРАБОТКА НАЖАТИЯ НА КНОПКУ ВЫХОДА
        start_exit_dialog(self)  # ЗАПУСК ДИАЛОГА ПОДТВЕРЖДЕНИЯ ВЫХОДА

    if event.ui_element == self.back_button:  # НАЖАТИЕ НА КНОПКУ ВОЗВРАЩЕНИЯ В ГЛ. МЕНЮ
        load_main_ui(self)  # ЗАПУСК ГЛАВНОГО МЕНЮ

    if event.ui_element == self.settings_button:  # НАЖАТИЕ НА КНОПКУ ПЕРЕХОДА В НАСТРОЙКИ
        load_settings_ui(self)  # ЗАПУСК ОКНА НАСТРОЕК

    if event.ui_element == self.load_game_button:  # НАЖАТИЕ НА КНОПКУ ПЕРЕХОДА В ОКНО ЗАГРУЗКИ ИГРЫ
        self.is_game_started = True
        load_pause_ui(self)  # ЗАГРУЗКА ИНТЕРФЕЙСА, ИСПОЛЬЗУЕМОГО ВО ВРЕМЯ ПАУЗЫ

    if event.ui_element == self.quit_button:
        self.level_1 = Level()
        self.level_2 = Level(1)

        self.level_type = 0

        self.is_game_started = False
        self.is_game_paused = False
        self.is_game_ended = False
        self.win = None

        load_main_ui(self)

    if event.ui_element == self.save_and_quit_button:
        self.level_1 = Level()
        self.level_2 = Level(1)

        self.level_type = 0

        self.is_game_started = False
        self.is_game_paused = False
        self.is_game_ended = False
        self.win = None

        load_main_ui(self)

    if event.ui_element == self.save_button:  # НАЖАТИЕ НА КНОПКУ СОХРАНЕНИЯ В ОКНЕ НАСТРОЕК
        write_settings_csv(self)  # ЗАПИСЬ ИМЕЮЩИХСЯ ИЗМЕНЕНИЙ В ФАЙЛ С НАСТРОЙКАМИ
        self.music.set_volume(self.main_music_val / 100)  # УСТАНОВКА НОВОЙ ГРОМКОСТИ МУЗЫКИ
        self.save_button.set_text("УСПЕШНО СОХРАНЕНО")  # ПОДТВЕРЖДЕНИЕ СОХРАНЕНИЯ НА КНОПКЕ
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def keydown_process(self, event, player):
    if event.key == pygame.K_F4:  # F4 - СМЕНА РЕЖИМА ЭКРАНА (полноэкранный/оконный)
        if self.fullscreen:
            pygame.display.set_mode(self.size, pygame.SCALED)
        else:
            pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        self.fullscreen = not self.fullscreen

    if event.key == pygame.K_ESCAPE:
        if self.is_game_started:
            self.is_game_paused = not self.is_game_paused

    if event.key == pygame.K_t:
        if self.is_game_started and player.can_change and not self.level_type:
            self.level_type = not self.level_type
            self.level_2.game_time = self.level_1.game_time
# ---------------------------------------------------------------------------------------------------------------------
