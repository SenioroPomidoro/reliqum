import pygame_gui
import pygame

from source.helping_scripts.load_sounds import off_all_game_music

# ---------------------------------------------------------------------------------------------------------------------


def load_main_ui(self) -> None:
    """Подгрузка интерфейса окна главного меню"""
    # -----------------------------------------------------------------------------------------------------------------
    self.manager = pygame_gui.UIManager(self.size, "data/theme.json")  # МЕНЕДЖЕР ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
    pygame.display.set_caption("ГЛАВНОЕ МЕНЮ")  # УСТАНОВКА НАЗВАНИЯ ОКНА

    # -----------------------------------------------------------------------------------------------------------------
    # КНОПКА ВЫХОДА ИЗ ИГРЫ
    self.exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 5 // 6), (self.w // 3, self.h // 7)),
        text="ВЫХОД",
        manager=self.manager,
    )

    # -----------------------------------------------------------------------------------------------------------------
    # КНОПКА ПЕРЕХОДА В ОКНО НАСТРОЕК
    self.settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 4 // 6), (self.w // 3, self.h // 7)),
        text="НАСТРОЙКИ",
        manager=self.manager
    )

    # -----------------------------------------------------------------------------------------------------------------
    # КНОПКА ЗАПУСКА ИГРЫ
    self.load_game_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 3 // 6), (self.w // 3, self.h // 7)),
        text="ИГРАТЬ",
        manager=self.manager
    )

    # -----------------------------------------------------------------------------------------------------------------
    # КНОПКА ПЕРЕХОДА В ОКНО СО СТАТИСТИКОЙ
    self.statistics_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w - self.w // 5, self.h - self.h * 1 // 12), (self.w // 6, self.h // 14)),
        text="СТАТИСТИКА",
        manager=self.manager
    )

    # -----------------------------------------------------------------------------------------------------------------
    # КНОПКИ, КОТОРЫХ НЕТ В ГЛАВНОМ МЕНЮ, НО НЕОБХОДИМОСТЬ ИХ ОПРЕДЕЛЕНИЯ ЗАКЛЮЧАЕТСЯ В ТОМ, ЧТО ОНИ ПРОВЕРЯЮТСЯ В
    # ЦИКЛЕ С СОБЫТИЯМИ:
    self.back_button = None
    self.save_button = None
    self.quit_button = None
    self.save_and_quit_button = None

    # -----------------------------------------------------------------------------------------------------------------
    # УСТАНОВКА ИЗОБРАЖЕНИЯ С НАЗВАНИЕМ ИГРЫ
    image = pygame.image.load("data/images/main_images/game_label.png")
    self.game_label = pygame.transform.scale(image, (1360, 200))

    # -----------------------------------------------------------------------------------------------------------------
    off_all_game_music(self)  # ОТКЛЮЧЕНИЕ ИГРОВОЙ МУЗЫКИ, КОТОРАЯ МОГЛА ИГРАТЬ РАНЕЕ (за искл. той, что в главном меню)

    if self.status in ["settings", "statistics", "main"]:  # ЕСЛИ ДО ЭТОГО СТАТУС МЕНЮ БЫЛ СРЕДИ ОПИСАННЫХ ОКОН
        need_to_play = False  # СНОВА СТАВИТЬ МУЗЫКУ НА ПРОИГРЫВАНИЕ НЕ НУЖНО
    else:  # ИНАЧЕ
        need_to_play = True  # НУЖНО

    self.status = "main"  # УСТАНОВКА СТАТУСА ОКНА ГЛАВНОГО МЕНЮ

    if need_to_play:
        self.main_music.play(100)  # ВКЛЮЧЕНИЕ МУЗЫКИ ГЛАВНОГО МЕНЮ

    self.import_music_settings(self)  # ПОЛУЧЕНИЕ АКТУАЛЬНЫХ ЗНАЧЕНИЙ ГРОМКОСТИ МУЗЫКИ
    self.main_music.set_volume(self.main_music_value / 100)  # УСТАНОВКА ГРОМКОСТИ МУЗЫКИ

    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
