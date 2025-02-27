import pygame
import pygame_gui

from data.settings import *

from source.helping_scripts.load_sounds import off_all_game_music
# ---------------------------------------------------------------------------------------------------------------------


# КЛАСС, КОТОРЫЙ ОТВЕЧАЕТ ЗА ТЕ ИЛИ ИНЫЕ ЭЛЕМЕНТЫ ГРАФИЧЕСКОГО ИНТЕРФЕЙСА ИГРОВОГО ОКНА
class GameUI:
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self) -> None:
        """Инициализация объекта графической части игрового окна"""
        self.display_surface = pygame.display.get_surface()  # ПОЛУЧЕНИЕ ТЕКУЩЕГО СЛОЯ ДЛЯ РИСОВАНИЯ
        self.font = pygame.font.Font("data/fonts/base_font.ttf", 30)  # ПОЛУЧЕНИЕ КАСТОМНОГО ШРИФТА

        self.health_bar_rect = pygame.Rect(550, 600, 200, 30)  # ОБЛАСТЬ ЭКРАНА ДЛЯ ПОЛОСЫ ЗДОРОВЬЯ
        self.energy_bar_rect = pygame.Rect(550, 634, 140, 30)  # ОБЛАСТЬ ЭКРАНА ДЛЯ ПОЛОСЫ ЭНЕРГИИ

        # ЗАГРУЗКА ИКОНОК ОРУЖИЯ И МАГИИ
        self.weapon_graphics = [pygame.image.load(weapon["graphic"]).convert_alpha() for weapon in weapon_data.values()]
        self.magic_graphics = [pygame.image.load(magic["graphic"]).convert_alpha() for magic in magic_data.values()]

        # ТЕКСТ ОБ ОТКРЫТИИ / ЗАКРЫТИИ ОКНА ПАЗУЫ
        self.pause_text = self.font.render("ESC - ПАУЗА", 1, (0, 0, 0))

    # -----------------------------------------------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------------------------------------------
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

    # -----------------------------------------------------------------------------------------------------------------
    def weapon_overlay(self, weapon_index: int, has_switched: bool) -> None:
        """
        Изображение оружия
        :param weapon_index: индекс выбранного оружия
        :param has_switched: показатель того, можно ли сменить оружие в данный момет
        """
        bg_rect = self.selection_box(470, 620, has_switched)  # ОКОШКО ДЛЯ ИЗОБРАЖЕНИЯ ОРУЖИЯ
        weapon_surf = self.weapon_graphics[weapon_index]  # ИЗОБРАЖЕНИЕ ВЫБРАННОГО ОРУЖИЯ, ВЗЯТОГО ПО ИНДЕКСУ
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)  # ОБЛАСТЬ ЭКРАНА, В КОТОРОМ НАХОДИТСЯ ЭТО ОРУЖИЕ,
        # ОРИЕНТИРОВАНИЕ ПРОИСХОДИТ ПО ЦЕНТРУ ОКОШКА ДЛЯ ЕГО ИЗОБРАЖЕНИЯ

        self.display_surface.blit(weapon_surf, weapon_rect)  # РАЗМЕЩЕНИЕ ИЗОБРАЖЕНИЯ ОРУЖИЯ В ОКОШКЕ ДЛЯ НЕГО

    # -----------------------------------------------------------------------------------------------------------------
    def magic_overlay(self, magic_index: int, has_switched: bool) -> None:
        """
        Изображение магии
        :param magic_index: индекс выбранной магии
        :param has_switched: показатель того, можно ли сменить магию в данный момент
        """
        bg_rect = self.selection_box(760, 620, has_switched)  # ОКОШКО ДЛЯ ИЗОБРАЖЕНИЯ МАГИИ
        magic_surf = self.magic_graphics[magic_index]  # ИЗОБРАЖЕНИЕ ВЫБРАННОГО ОРУЖИЯ, ВЗЯТОГО ПО ИНДЕКСУ
        magic_rect = magic_surf.get_rect(center=bg_rect.center)  # ОБЛАСТЬ ЭКРАНА, В КОТОРОМ НАХОДИТСЯ ЭТО ОРУЖИЕ,
        # ОРИЕНТИРОВАНИЕ ПРОИСХОДИТ ПО ЦЕНТРУ ОКОШКА ДЛЯ ЕГО ИЗОБРАЖЕНИЯ

        self.display_surface.blit(magic_surf, magic_rect)  # РАЗМЕЩЕНИЕ ИЗОБРАЖЕНИЯ МАГИИ В ОКОШКЕ ДЛЯ НЕЁ

    # -----------------------------------------------------------------------------------------------------------------
    def show_kills_and_tp_and_time(self, kills, need_to_kill, player, time) -> None:
        """
        Метод, отображающий окно количства убитых монстров и некоторой
        :param player: объект игрока
        :param time: время, которое игрок пребывает на текущем уровне
        :param kills: количество убитых на данный момент монстров
        :param need_to_kill: количество монстров, которых нужно убить для продвижения на следующий уровень (с 1 на 2)
        """
        x = self.display_surface.get_size()[0] - 20  # РАСПОЛОЖЕНИЕ ОКНА ПО ИКСАМ
        y = self.display_surface.get_size()[1] - 20  # РАСПОЛОЖЕНИЕ ОКНА ПО ИГРИКАМ

        seconds = str(int(time) % 60).rjust(2, "0")  # КОЛИЧЕСТВО СЕКУНД
        minutes = str(int(time) // 60).rjust(2, "0")  # КОЛИЧЕСТВО МИНУТ
        str_time = F"{minutes}:{seconds}"  # ПРЕОБРАЗОВАНИЕ КОЛ-ВА СЕКУНД В ФОРМАТЕ MM:SS

        #  В СЛУЧАЕ ВЫПОЛНЕНИЕ ОПРЕДЕЛЕННЫХ УСЛОВИЙ
        if kills == need_to_kill - 3 and 3250 <= player.rect.x <= 3500 and 850 <= player.rect.y <= 950:
            text = F"T - ВОЙТИ | {str_time}"  # ОТОБРАЖЕНИЕ НАДПИСИ ТОГО, ЧТО ИГРОК МОЖЕТ ВОЙТИ В ЛОКАЦИЮ С БОССОМ
            player.can_change = True  # СТАВИМ ВОЗМОЖНЫМ ПЕРЕМЕЩЕНИЕ В ЛОКАЦИЮ С БОССОМ
        else:  # ИНАЧЕ
            text = F"{kills} / {need_to_kill} | {str_time}"  # ОТОБРАЖЕНИЕ КОЛ-ВА УБИТЫХ ВРАГОВ И ВРЕМЕНИ
            player.can_change = False  # ИГРОК НЕ МОЖЕТ ПЕРЕЙТИ В ЛОКАЦИЮ С БОССОМ
        text_surf = self.font.render(text, False, "black")  # УБИТЫЕ ВРАГИ
        text_rect = text_surf.get_rect(bottomright=(x, y))  # РАСПОЛОЖЕНИЯ ТЕКСТА НА ОКНЕ

        pygame.draw.rect(self.display_surface, "orange", text_rect.inflate(20, 20))  # ОТРИСОВКА ФОНА ОКНА С ПОДСЧЕТОМ
        self.display_surface.blit(text_surf, text_rect)  # ОТРИСВОКА ПОКАЗАТЕЛЯ УБИЙСТВ
        pygame.draw.rect(self.display_surface, "black", text_rect.inflate(20, 20), 3)  # ОТРИСОВКА ПИКСЕЛЕЙ ГРАНИЦЫ

    # -----------------------------------------------------------------------------------------------------------------
    def display(self, player, time) -> None:
        """
        Функция для отобюражения всего, что описано в этом классе
        :param time: время, которое игрок пребывает на текущем уровне
        :param player: объект игрока
        """
        # ОТОЮРАЖЕНИЕ ПОЛОСОК СО ЗДОРОЬВЕМ, ЭНЕРГИЕЙ СООТВЕТСТВЕННО
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, "red")
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, "blue")

        # ОТОБРАЖЕНИЕ ДАННЫХ ИНФОРМАЦИОННОМ ОКНЕ
        self.show_kills_and_tp_and_time(player.kill_counter, player.need_to_kill, player, time)

        # ОТОБРАЖЕНИЕ ИЗОБРАЖЕНИЙ ВЫБРАННЫХ ОРУЖИЯ И МАГИИ СООТВЕТСВЕННО
        self.weapon_overlay(player.weapon_index, player.can_switch_weapon)
        self.magic_overlay(player.magic_index, player.can_switch_magic)

        # ОТОБРАЖЕНИЕ НАДПИСИ О ПАУЗЕ
        x, y = self.display_surface.get_size()
        self.display_surface.blit(self.pause_text, (20, y - 50))

    # -----------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------------------------------------

def load_pause_ui(self) -> None:
    """Функция подгрузки интерфейса во время паузы"""
    self.manager = pygame_gui.UIManager(self.size, "data/theme.json")  # МЕНЕДЖЕР ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
    pygame.display.set_caption("Reliqum")  # УСТАНОВКА НАЗВАНИЯ ОКНА
    font = pygame.font.Font("data/fonts/base_font.ttf", 30)  # ВРЕМЕННАЯ ПЕРЕМЕННАЯ ШРИФТА
    display_surface = pygame.display.get_surface()

    # КНОПКА ВОЗВРАЩЕНИЯ В ГЛАВНОЕ МЕНЮ
    self.quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 3 / 4), (self.w // 3, self.h // 7)),
        text="В ГЛАВНОЕ МЕНЮ",
        manager=self.manager
    )

    self.status = "pause"  # СТАТУС ОКНА - ПАУЗА

# ---------------------------------------------------------------------------------------------------------------------


def load_end_ui(self, is_win=True) -> None:
    """
    Функция подгрузки интерфейса окончания игры
    :param self: объект главного игрового потока
    :param is_win: выйграл игрок или же проиграл
    """
    self.manager = pygame_gui.UIManager(self.size, "data/theme.json")  # МЕНЕДЖЕР ГРАФИЧЕСКОГО ИНТЕРФЕЙСА
    pygame.display.set_caption("Reliqum")  # УСТАНОВКА НАЗВАНИЯ ОКНА

    # КНОПКА ВОЗВРАЩЕНИЯ В ГЛАВНОЕ МЕНЮ
    self.quit_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((self.w // 3, self.h * 3 / 4), (self.w // 3, self.h // 7)),
        text="СОХРАНИТЬ И ВЫЙТИ",
        manager=self.manager
    )

    off_all_game_music(self)  # ВЫКЛЮЧЕНИЕ ВСЕЙ ИГРОВОЙ МУЗЫКИ

    if is_win:  # ЕСЛИ ИГРОК ВЫЙГРАЛ
        self.status = "end"  # СТАТУС ОКНА - КОНЕЦ (победа)
        self.win_music.play(100)  # ПРОИГРЫВАНИЕ МУЗЫКИ ПОБЕДЫ
        self.win_music.set_volume(self.ingame_music_value / 100)  # УСТАНОВКА ГРОМКОСТИ МУЗЫКИ
        self.is_win_music_playing = True  # МУЗЫКА ПОБЕДЫ ИГРАЕТ (параметр для дебага)
    else:  # ИНАЧЕ
        self.status = "end_loser"  # СТАТУС ОКНА - КОНЕЦ (поражение)
        self.lose_music.play(100)  # ПРОИГРЫВАНИЕ МУЗЫКИ ПОРАЖЕНИЯ
        self.lose_music.set_volume(self.ingame_music_value / 100)  # УСТАНОВКА ГРОМКОСТИ МУЗЫКИ
        self.is_lose_music_playing = True  # МУЗЫКА ПОРАЖЕНИЯ ИГРАЕТ (параметр для дебага)

# ---------------------------------------------------------------------------------------------------------------------
