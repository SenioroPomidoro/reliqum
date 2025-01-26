import pygame
import pygame_gui
from data.settings import *


# КЛАСС, КОТОРЫЙ ОТВЕЧАЕТ ЗА ТЕ ИЛИ ИНЫЕ ЭЛЕМЕНТЫ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА ИГРОВОГО ОКНА
class GameUI:
    def __init__(self) -> None:
        """Инициализация объекта графической части игрового окна"""

        # ---
        self.display_surface = pygame.display.get_surface()  # ПОЛУЧЕНИЕ ТЕКУЩЕГО СЛОЯ ДЛЯ РИСОВАНИЯ
        self.font = pygame.font.Font("data/fonts/base_font.ttf", 30)  # ПОЛУЧЕНИЕ КАСТОМНОГО ШРИФТА

        # ---
        self.health_bar_rect = pygame.Rect(600, 800, 200, 30)  # ОБЛАСТЬ ЭКРАНА ДЛЯ ПОЛОСЫ ЗДОРОВЬЯ
        self.energy_bar_rect = pygame.Rect(600, 834, 140, 30)  # ОБЛАСТЬ ЭКРАНА ДЛЯ ПОЛОСЫ ЭНЕРГИИ

        # --- ЗАГРУЗКА ИКОНОК ОРУЖИЯ И МАГИИ
        self.weapon_graphics = [pygame.image.load(weapon["graphic"]).convert_alpha() for weapon in weapon_data.values()]
        self.magic_graphics = [pygame.image.load(magic["graphic"]).convert_alpha() for magic in magic_data.values()]

    def show_exp(self, exp) -> None:
        """
        Функция для отрисовки показателя полученого опыта
        :param exp: количество опыта, которое имеет игрок
        """

        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20

        text_surf = self.font.render(F"EXP: {int(exp)}", False, "black")  # ТЕКСТ EXP
        text_rect = text_surf.get_rect(bottomright=(x, y))  # РАСПОЛОЖЕНИЯ ТЕКСТА НА ОКНЕ

        pygame.draw.rect(self.display_surface, "orange", text_rect.inflate(20, 20))  # ОТРИСОВКА ФОНА ОКНА С ОПЫТОМ
        self.display_surface.blit(text_surf, text_rect)  # ОТРИСВОКА ПОКАЗАТЕЛЯ ОПЫТА
        pygame.draw.rect(self.display_surface, "black", text_rect.inflate(20, 20), 3)  # ОТРИСОВКА ПИКСЕЛЕЙ ГРАНИЦЫ

    def show_bar(self, current: int, max_amount: int, bg_rect: pygame.Rect, color: str) -> None:
        """
        Функция отрисовки
        :param current: количественный показатель данной полосы
        :param max_amount: максимальное значение полосы
        :param bg_rect: область экрана этой полосы
        :param color: цвет заполнения полосы
        """
        pygame.draw.rect(self.display_surface, "black", bg_rect)  # ОТРИСОВКА ФОНА ПОЛОСОК

        ratio = current / max_amount  # ОТНОШЕНИЕ ТЕКУЩЕГО ПОКАЗТЕЛЯ К МАКСИМАЛЬНОМУ
        current_width = bg_rect.width * ratio  # ТЕКУЩАЯ СТЕПЕНЬ ЗАПОЛНЕНОСТИ ПОЛОСКИ
        current_rect = bg_rect.copy()  # КОПИЯ ОБЪЕКТА ЧЕТЫРЕХУГОЛЬНИКА ОБЛАСТИ ЭКРАНА
        current_rect.width = current_width  # УСТАНОВКА НУЖНОЙ ШИРИНЫ ДЛЯ НОВОЙ ОБЛАСТИ ПОЛОСКИ

        pygame.draw.rect(self.display_surface, color, current_rect)  # ОТРИСОВКА ПОЛОСКИ
        pygame.draw.rect(self.display_surface, "black", bg_rect, 4)  # ОТРИСОВКА ФОНА У ПОЛОСКИ

    def selection_box(self, left: int, top: int, has_switched: bool) -> pygame.Rect:
        """
        Часть окна, изображающая выбранное оружие/магию
        :param left: левая верхняя координата по иксам
        :param top: левая верхняя координата по игрикам
        :param has_switched: показатель того, можно ли в данный момент сменить оружие (существует кулдаун между сменой
        оружия)
        :return объект четырехугольника области экрана, в котором находится часть окна, изображающая выбранное оружие/
        магию
        """
        bg_rect = pygame.Rect(left, top, 60, 60)  # ФОН ОКОШКА ДЛЯ РАСПОЛОЖЕНИЯ ОРУЖИЯ / МАГИИ
        pygame.draw.rect(self.display_surface, "black", bg_rect)  # ОТРИСОВКА ФОНА
        if has_switched:  # ЕСЛИ МОЖНО СМЕНИТЬ ОРУЖИЕ, ТО ГРАНИЦА ФОНА ОКРШИВАЕТСЯ В ЗОЛОТОЙ
            pygame.draw.rect(self.display_surface, "gold", bg_rect, 4)
        else:  # ЕСЛИ НЕЛЬЗЯ СМЕНИТЬ ОРУЖИЕ, ГРАНИЦА ФОНА ОКРАЖИВАЕТСЯ В КОРИЧНЕВЫЙ
            pygame.draw.rect(self.display_surface, "brown", bg_rect, 4)
        return bg_rect

    def weapon_overlay(self, weapon_index: int, has_switched: bool) -> None:
        """
        Изображение оружия
        :param weapon_index: индекс выбранного оружия
        :param has_switched: показатель того, можно ли сменить оружие в данный момет
        """
        bg_rect = self.selection_box(520, 800, has_switched)  # ОКОШКО ДЛЯ ИЗОБРАЖЕНИЯ ОРУЖИЯ
        weapon_surf = self.weapon_graphics[weapon_index]  # ИЗОБРАЖЕНИЕ ВЫБРАННОГО ОРУЖИЯ, ВЗЯТОГО ПО ИНДЕКСУ
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)  # ОБЛАСТЬ ЭКРАНА, В КОТОРОМ НАХОДИТСЯ ЭТО ОРУЖИЕ,
        # ОРИЕНТИРОВАНИЕ ПРОИСХОДИТ ПО ЦЕНТРУ ОКОШКА ДЛЯ ЕГО ИЗОБРАЖЕНИЯ

        self.display_surface.blit(weapon_surf, weapon_rect)  # РАЗМЕЩЕНИЕ ИЗОБРАЖЕНИЯ ОРУЖИЯ В ОКОШКЕ ДЛЯ НЕГО

    def magic_overlay(self, magic_index: int, has_switched: bool) -> None:
        """
        Изображение магии
        :param magic_index: индекс выбранной магии
        :param has_switched: показатель того, можно ли сменить магию в данный момент
        """
        bg_rect = self.selection_box(810, 800, has_switched)  # ОКОШКО ДЛЯ ИЗОБРАЖЕНИЯ МАГИИ
        magic_surf = self.magic_graphics[magic_index]  # ИЗОБРАЖЕНИЕ ВЫБРАННОГО ОРУЖИЯ, ВЗЯТОГО ПО ИНДЕКСУ
        magic_rect = magic_surf.get_rect(center=bg_rect.center)  # ОБЛАСТЬ ЭКРАНА, В КОТОРОМ НАХОДИТСЯ ЭТО ОРУЖИЕ,
        # ОРИЕНТИРОВАНИЕ ПРОИСХОДИТ ПО ЦЕНТРУ ОКОШКА ДЛЯ ЕГО ИЗОБРАЖЕНИЯ

        self.display_surface.blit(magic_surf, magic_rect)  # РАЗМЕЩЕНИЕ ИЗОБРАЖЕНИЯ МАГИИ В ОКОШКЕ ДЛЯ НЕЁ

    def display(self, player) -> None:
        """
        Функция для отобюражения всего, что описано в этом классе
        :param player: объект игрока
        """
        # ОТОЮРАЖЕНИЕ ПОЛОСОК СО ЗДОРОЬВЕМ, ЭНЕРГИЕЙ СООТВЕТСТВЕННО
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, "red")
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, "blue")

        # ОТОБРАЖЕНИЕ ДАННЫХ ОБ ОПЫТЕ
        self.show_exp(player.exp)

        # ОТОБРАЖЕНИЕ ИЗОБРАЖЕНИЙ ВЫБРАННЫХ ОРУЖИЯ И МАГИИ СООТВЕТСВЕННО
        self.weapon_overlay(player.weapon_index, player.can_switch_weapon)
        self.magic_overlay(player.magic_index, player.can_switch_magic)


def load_pause_ui(self):
    """Подгрузка интерфейса во время паузы"""
    self.manager = pygame_gui.UIManager(self.size, "data/theme.json")  # МЕНЕДЖЕР ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
    pygame.display.set_caption("Reliqum")  # УСТАНОВКА НАЗВАНИЯ ОКНА

    # КНОПКА ВОЗВРАЩЕНИЯ В ГЛАВНОЕ МЕНЮ
    self.save_and_quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 3 / 4), (self.w // 3, self.h // 7)),
        text="СОХРАНИТЬ И ВЫЙТИ",
        manager=self.manager
    )

    self.status = "pause"
