import pygame_gui
import pygame


def load_statistics_menu_ui(self):
    """Подгрузка интерфейса окна статистики"""

    self.manager = pygame_gui.UIManager(self.size, "data/theme.json")
    pygame.display.set_caption("СТАТИСТИКА")

    self.back_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 90, self.h * 5 // 6), (self.w // 3, self.h // 7)),
        text="В ГЛАВНОЕ МЕНЮ",
        manager=self.manager,
    )

    self.status = "statistics"
