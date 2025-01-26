import pygame_gui
import pygame


def load_main_ui(self):
    """Подгрузка интерфейса окна главного меню"""
    self.manager = pygame_gui.UIManager(self.size, "data/theme.json")  # МЕНЕДЖЕР ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
    pygame.display.set_caption("ГЛАВНОЕ МЕНЮ")  # УСТАНОВКА НАЗВАНИЯ ОКНА

    # КНОПКА ВЫХОДА ИЗ ИГРЫ
    self.exit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 5 // 6), (self.w // 3, self.h // 7)),
        text="ВЫХОД",
        manager=self.manager,
    )

    # КНОПКА ПЕРЕХОДА В ОКНО НАСТРОЕК
    self.settings_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 4 // 6), (self.w // 3, self.h // 7)),
        text="НАСТРОЙКИ",
        manager=self.manager
    )

    # КНОПКА ПЕРЕХОДА В ОКНО ЗАГРУЗКИ ИГРЫ
    self.load_game_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 3 // 6), (self.w // 3, self.h // 7)),
        text="ЗАГРУЗКА ИГРЫ",
        manager=self.manager
    )

    # КНОПКА ПЕРЕХОДА В ОКНО СОЗДАНИЯ НОВОЙ ИГРЫ
    self.new_game_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 2 // 6), (self.w // 3, self.h // 7)),
        text="НОВАЯ ИГРА",
        manager=self.manager
    )

    # КНОПКИ, КОТОРЫХ НЕТ В ГЛАВНОМ МЕНЮ, НО НЕОБХОДИМОСТЬ ИХ ОПРЕДЕЛЕНИЯ ЗАКЛЮЧАЕТСЯ В ТОМ, ЧТО ОНИ ПРОВЕРЯЮТСЯ В
    # ЦИКЛЕ С СОБЫТИЯМИ:
    self.back_button = None
    self.save_button = None

    # УСТАНОВКА ИЗОБРАЖЕНИЯ С НАЗВАНИЕМ ИГРЫ
    image = pygame.image.load("data/images/main_images/game_label.png")
    self.game_label = pygame.transform.scale(image, (1360, 200))

    self.status = "main"  # УСТАНОВКА СТАТУСА ОКНА ГЛАВНОГО МЕНЮ
