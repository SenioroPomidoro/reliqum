import pygame_gui
import pygame


def new_game_menu_ui(self):
    """Подгрузка интерфейса окна создания новой игры"""
    self.manager = pygame_gui.UIManager(self.size, "data/theme.json")  # МЕНЕДЖЕР ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
    pygame.display.set_caption("НОВАЯ ИГРА")  # УСТАНОВКА НАЗВАНИЯ ОКНА

    # КНОПКА ВОЗВРАЩЕНИЯ В ГЛАВНОЕ МЕНЮ
    self.back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 90, self.h * 5 // 6), (self.w // 3, self.h // 7)),
        text="В ГЛАВНОЕ МЕНЮ",
        manager=self.manager,
    )

    self.status = "new_game"  # УСТАНОВКА СТАТУСА ОКНА СОЗДАНИЯ НОВОЙ ИГРЫ
