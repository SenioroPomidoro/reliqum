import pygame_gui
import pygame

from scripts.helping_scripts.imports import import_settings


def load_settings_ui(self):
    """Подгрузка интерфейса окна настроек"""
    self.manager = pygame_gui.UIManager(self.size, "data/theme.json")
    pygame.display.set_caption("НАСТРОЙКИ")
    import_settings(self)

    self.back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 90, self.h * 5 / 6), (self.w // 3, self.h // 7)),
        text="В ГЛАВНОЕ МЕНЮ",
        manager=self.manager
    )

    self.main_menu_music_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((self.w // 90, self.h // 6), (self.w // 3, self.h // 20)),
        value_range=(0, 100),
        start_value=0,
        manager=self.manager

    )

    self.game_music_slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((self.w // 90, self. h // 2), (self.w // 3, self.h // 20)),
        value_range=(0, 100),
        start_value=0,
        manager=self.manager
    )

    self.save_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 2, self.h * 5 // 6), (self.w // 3, self.h // 7)),
        text="СОХРАНИТЬ",
        manager=self.manager
    )

    self.temprorary_main_music_val = self.main_music_value
    self.temprorary_ingame_music_val = self.ingame_music_value

    self.main_menu_music_slider.set_current_value(self.temprorary_main_music_val)
    self.game_music_slider.set_current_value(self.temprorary_ingame_music_val)

    self.status = "settings"
