import pygame_gui
import pygame


def load_main_ui(self):
    """Подгрузка интерфейса окна главного меню"""

    self.manager = pygame_gui.UIManager(self.size, "data/theme.json")
    pygame.display.set_caption("ГЛАВНОЕ МЕНЮ")

    self.exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 5 // 6), (self.w // 3, self.h // 7)),
        text="ВЫХОД",
        manager=self.manager,
    )

    self.settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 4 // 6), (self.w // 3, self.h // 7)),
        text="НАСТРОЙКИ",
        manager=self.manager
    )

    self.load_game_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 3 // 6), (self.w // 3, self.h // 7)),
        text="ЗАГРУЗКА ИГРЫ",
        manager=self.manager
    )

    self.new_game_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 2 // 6), (self.w // 3, self.h // 7)),
        text="НОВАЯ ИГРА",
        manager=self.manager
    )

    self.statistics_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w - self.w // 5, self.h - self.h * 1 // 12), (self.w // 6, self.h // 14)),
        text="СТАТИСТИКА",
        manager=self.manager
    )

    self.back_button = None

    self.save_button = None

    image = pygame.image.load("data/images/main_images/game_label.png")
    self.game_label = pygame.transform.scale(image, (1360, 200))

    self.status = "main"
