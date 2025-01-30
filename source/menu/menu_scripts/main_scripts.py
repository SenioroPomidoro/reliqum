import pygame_gui
import pygame

from source.menu.user_interface.statistics_ui import load_statistics_ui
from source.menu.menu_scripts.settings_scripts import write_settings_csv
from source.menu.user_interface.settings_ui import load_settings_ui
from source.menu.user_interface.main_ui import load_main_ui
from source.game.user_interface.game_ui import load_pause_ui
from source.game.game_scripts.game_level import Level


# ---------------------------------------------------------------------------------------------------------------------
def start_exit_dialog(self) -> None:
    """
    Функция, открывающая окно выхода из игры
    :param self: объект главного потока
    """
    self.exit_dialog = pygame_gui.windows.UIConfirmationDialog(
        rect=pygame.Rect((self.w / 3, self.h / 4), (self.w / 3, self.h / 4)),
        manager=self.manager,  # МЕНЕДЖЕР ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
        window_title="Подтверждение выхода из игры",  # НАЗВАНИЕ ВСПЛЫВАЮЩЕГО ОКНА
        action_long_desc="ВЫ УВЕРЕНЫ, ЧТО ХОТИТЕ ВЫЙТИ ИЗ ИГРЫ?",  # ВОПРОС О ВЫХОДЕ ИЗ ИГРЫ
        action_short_name="ДА",  # НАДПИСЬ НА КНОПКЕ ПОДТВЕРЖДЕНИЯ
        blocking=True  # БЛОКИРОВКА ЛЮБОГО НАЖАТИЯ ДО РЕАКЦИИ НА ВСПЛЫВАЮЩЕЕ ОКНО
    )
    self.exit_dialog.cancel_button.set_text("НЕТ")  # НАДПИСЬ НА КНОПКЕ ОТКАЗА
# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def button_pressed_process(self, event) -> None:
    """
    Функция, обрабатывающая нажатие на кнопки по поступившему событию
    :param self: объект главного потока
    :param event: кортеж события
    """
    self.click.play()  # ПРОИГРЫВАНИЕ ЗВУКА НАЖАТИЯ НА КНОПКУ

    # -----------------------------------------------------------------------------------------------------------------
    if event.ui_element == self.exit_button:  # ОБРАБОТКА НАЖАТИЯ НА КНОПКУ ВЫХОДА
        start_exit_dialog(self)  # ЗАПУСК ДИАЛОГА ПОДТВЕРЖДЕНИЯ ВЫХОДА

    # -----------------------------------------------------------------------------------------------------------------
    if event.ui_element == self.back_button:  # НАЖАТИЕ НА КНОПКУ ВОЗВРАЩЕНИЯ В ГЛ. МЕНЮ
        load_main_ui(self)  # ЗАПУСК ГЛАВНОГО МЕНЮ

    # -----------------------------------------------------------------------------------------------------------------
    if event.ui_element == self.settings_button:  # НАЖАТИЕ НА КНОПКУ ПЕРЕХОДА В НАСТРОЙКИ
        load_settings_ui(self)  # ЗАПУСК ОКНА НАСТРОЕК

    # -----------------------------------------------------------------------------------------------------------------
    if event.ui_element == self.statistics_button:
        load_statistics_ui(self)

    # -----------------------------------------------------------------------------------------------------------------
    if event.ui_element == self.load_game_button:  # НАЖАТИЕ НА КНОПКУ ПЕРЕХОДА В ОКНО ЗАГРУЗКИ ИГРЫ
        self.is_game_started = True
        load_pause_ui(self)  # ЗАГРУЗКА ИНТЕРФЕЙСА, ИСПОЛЬЗУЕМОГО ВО ВРЕМЯ ПАУЗЫ

    # -----------------------------------------------------------------------------------------------------------------
    if event.ui_element == self.quit_button:  # КНОПКА ВЫХОДЫ В ГЛАВНОЕ МЕНЮ
        self.level_1 = Level()  # ОБНОВЛЕНИЕ ПЕРВОГО ИГРОВОГО УРОВНЯ
        self.level_2 = Level(1)  # ОБНОВЛЕНИЕ ВТОРОГО ИГРОВОГО УРОВНЯ

        self.level_type = 0  # УСТАНОВКА ЗНАЧЕНИЯ ТИПА УРОВНЯ В 0 (первый уровень)

        self.is_game_started = False  # ИГРА НЕ ЗАПУЩЕНА
        self.is_game_paused = False  # ИГРА НЕ СТОИТ НА ПАУЗЕ
        self.is_game_ended = False  # ИГРА НЕ ЗАКОНЧЕНА
        self.win = False  # ИГРОК НЕ ПОБЕДИЛ
        self.lose = False  # ИГРОК НЕ ВЫЙГРАЛ

        load_main_ui(self)  # ЗАГРУКЗА ГЛАВНОГО МЕНЮ

    # -----------------------------------------------------------------------------------------------------------------
    if event.ui_element == self.save_button:  # НАЖАТИЕ НА КНОПКУ СОХРАНЕНИЯ В ОКНЕ НАСТРОЕК
        write_settings_csv(self)  # ЗАПИСЬ ИМЕЮЩИХСЯ ИЗМЕНЕНИЙ В ФАЙЛ С НАСТРОЙКАМИ
        self.music.set_volume(self.main_music_val / 100)  # УСТАНОВКА НОВОЙ ГРОМКОСТИ МУЗЫКИ
        self.save_button.set_text("УСПЕШНО СОХРАНЕНО")  # ПОДТВЕРЖДЕНИЕ СОХРАНЕНИЯ НА КНОПКЕ

# ---------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------
def keydown_process(self, event, player):
    """
    Функция, обрабатывающая нажатия на кнопки клавиатуры
    :param self: объект главного потока
    :param event: кортеж события
    :param player: объект игрока
    """
    # -----------------------------------------------------------------------------------------------------------------
    if event.key == pygame.K_F4:  # F4 - СМЕНА РЕЖИМА ЭКРАНА (полноэкранный/оконный)
        if self.fullscreen:  # БЫЛ ПОЛНОЭКРАННЫЙ
            pygame.display.set_mode(self.size, pygame.SCALED)  # СТАЛ ОКОННЫЙ
        else:  # БЫЛ ОКОННЫЙ
            pygame.display.set_mode(self.size, pygame.FULLSCREEN)  # СТАЛ ПОЛНОЭКРАННЫЙ
        self.fullscreen = not self.fullscreen  # СМЕНА ЗНАЧЕНИЯ РЕЖИМА ЭКРАНА НА ПРОТИВОПОЛОЖНОЕ

    # -----------------------------------------------------------------------------------------------------------------
    if event.key == pygame.K_ESCAPE:  # ЕСЛИ НАЖАТА КНОПКА ПАУЗЫ (ESCAPE)
        if self.is_game_started and not self.win and not self.lose:  # ЕСЛИ ЭТО СДЕЛАНО ВО ВРЕМЯ ИГРЫ, НО НЕ КОНЦА
            self.is_game_paused = not self.is_game_paused  # МЕНЯЕМ ЗНАЧЕНИЕ ПАУЗЫ НА ПРОТИВОПОЛОЖНОЕ

    # -----------------------------------------------------------------------------------------------------------------
    if event.key == pygame.K_t:  # ЕСЛИ НАЖАТА КНОПКА T (для перехода в локацию с боссом)
        # ПРИ ВЫПОЛНЕНИИ ВСЕХ УСЛОВИЙ, НЕОБХОДИМЫЙ ДЛЯ ПЕРЕХОДА
        if self.is_game_started and player.can_change and not self.level_type and not self.is_game_ended:
            self.level_type = not self.level_type  # СМЕНЯЕТСЯ УРОВЕНЬ
            self.level_2.game_time = self.level_1.game_time  # ИГРОВОЕ ВРЕМЯ ПЕРЕДАЁТСЯ ВТОРОМУ УРОВНЮ ДЛЯ ЕГО ПРОДОЛЖ.

    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
