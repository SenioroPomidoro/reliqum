import pygame_gui
import pygame

from source.helping_scripts.imports import import_music_settings

# ---------------------------------------------------------------------------------------------------------------------


def load_settings_ui(self):
    """Подгрузка интерфейса окна настроек"""
    # -----------------------------------------------------------------------------------------------------------------
    self.manager = pygame_gui.UIManager(self.size, "data/theme.json")  # МЕНЕДЖЕР ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
    pygame.display.set_caption("НАСТРОЙКИ")  # УСТАНОВКА НАЗВАНИЯ ОКНА
    import_music_settings(self)  # ЗАПИСЬ НАСТРОЕК В АТРИБУТЫ ОБЪЕКТА КЛАССА ОКНА

    # -----------------------------------------------------------------------------------------------------------------
    # КНОПКА ВОЗВРАЩЕНИЯ В ГЛАВНОЕ МЕНЮ
    self.back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 90, self.h * 5 / 6), (self.w // 3, self.h // 7)),
        text="В ГЛАВНОЕ МЕНЮ",
        manager=self.manager
    )

    # -----------------------------------------------------------------------------------------------------------------
    # СЛАЙДЕР ДЛЯ ИЗМЕНЕНИЯ ГРОМКОСТИ МУЗЫКИ В ГЛАВНО МЕНЮ
    self.main_menu_music_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((self.w // 90, self.h // 6), (self.w // 3, self.h // 20)),
        value_range=(0, 100),
        start_value=0,
        manager=self.manager

    )

    # -----------------------------------------------------------------------------------------------------------------
    # СЛАЙДЕР ДЛЯ ИЗМЕНЕНИЯ ГРОМКОСТИ МУЗЫКИ В ОКНЕ ИГРЫ
    self.game_music_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((self.w // 90, self. h // 2), (self.w // 3, self.h // 20)),
        value_range=(0, 100),
        start_value=0,
        manager=self.manager
    )

    # -----------------------------------------------------------------------------------------------------------------
    # КНОПКА СОХРАНЕНИЯ НАСТРОЕК
    self.save_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 2, self.h * 5 // 6), (self.w // 3, self.h // 7)),
        text="СОХРАНИТЬ",
        manager=self.manager
    )

    # -----------------------------------------------------------------------------------------------------------------
    # ПЕРЕМЕННЫЕ, ИЗМЕНЯЮЩИЕСЯ ПРИ ИЗМЕНЕНИИ ЗНАЧЕНИЯ СЛАЙДЕРОВ, ПОСЛЕ ПОДТВЕРЖДЕНИЯ СОХРАНЯЮТСЯ В ОДНОИМЕННЫЕ, НО БЕЗ
    # ПРИПИСКИ temprorary (временный):
    self.temprorary_main_music_val = self.main_music_value
    self.temprorary_ingame_music_val = self.ingame_music_value
    # УСТАНОВКА СЛАЙДЕРОВ НА УСТАНОВЛЕННЫЕ НАСТРОЙКАМИ ПОЗИЦИИ:
    self.main_menu_music_slider.set_current_value(self.temprorary_main_music_val)
    self.game_music_slider.set_current_value(self.temprorary_ingame_music_val)

    self.status = "settings"  # УСТАНОВКА СТАТУСА ОКНА НАСТРОЕК
    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
