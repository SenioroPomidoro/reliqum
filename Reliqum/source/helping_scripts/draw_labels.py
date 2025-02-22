import pygame

from data.settings import BG_COLOR


# ---------------------------------------------------------------------------------------------------------------------


def draw_labels(self) -> None:
    """Функция отрисовки текстовых элементов в тех или иных окнах в меню"""
    # -----------------------------------------------------------------------------------------------------------------
    if self.status is None:  # ЕСЛИ СТАТУС СОСТОЯНИЯ ИГРЫ НЕОПРЕДЕЛЕН - НИЧЕГО НЕ РИСУЕТСЯ
        return

    # -----------------------------------------------------------------------------------------------------------------
    if self.status == "main":  # ОТРИСОВКА ТЕКСТОВЫХ ЭЛЕМЕНТОВ ОКНА ГЛАВНОГО МЕНЮ
        label = self.custom_font.render("F4 - ПОЛНЫЙ ЭКРАН", 1, (0, 0, 0))  # УКАЗАНИЕ О ПОЛНОЭКРАННОМ РЕЖИМЕ
        self.window_surface.blit(label, (self.w // 90, self.h - self.custom_font.get_height()))  # УСТАНОВКА НАДПИСИ
        self.window_surface.blit(self.game_label, (20, 20))  # УСТАНОВКА ИЗОБРАЖЕНИЯ С НАЗВАНИЕМ ИГРЫВ В ГЛ. МЕНЮ

    # -----------------------------------------------------------------------------------------------------------------
    elif self.status == "settings":  # ОТРИСОВКА ТЕКСТОВЫХ ЭЛЕМЕНТОВ ОКНА НАСТРОЕК
        main_label = self.custom_font.render("МУЗЫКА В МЕНЮ", 1, (0, 0, 0))  # НАДПИСЬ "МУЗЫКА В МЕНЮ"
        game_label = self.custom_font.render("МУЗЫКА В ИГРЕ", 1, (0, 0, 0))  # НАДПИСЬ "МУЗЫКА В ИГРЕ"

        # НАДПИСИ ЧИСЛОВЫХ ЗНАЧНЕИЙ МУЗЫКИ В МЕНЮ И В ИГРЕ СООТВЕТСВЕННО
        main_music_val_label = self.custom_font.render(str(self.temprorary_main_music_val), 1, (0, 0, 0))
        game_music_val_label = self.custom_font.render(str(self.temprorary_ingame_music_val), 1, (0, 0, 0))

        self.window_surface.blit(main_music_val_label, (450, 100))  # РАЗМЕЩЕНИЕ ЧИСЛОВОГО ЗНАЧЕНИЯ МУЗЫКИ В МЕНЮ
        self.window_surface.blit(game_music_val_label, (450, 360))  # РАЗМЕЩЕНИЕ ЧИСЛОВОГО ЗНАЧЕНИЯ МУЗЫКИ В ИГРЕ

        self.window_surface.blit(main_label, (self.w // 90, 60))  # РАЗМЕЩЕНИЕ НАДПИСИ "МУЗЫКА В МЕНЮ"
        self.window_surface.blit(game_label, (self.w // 90, 310))  # РАЗМЕЩЕНИЕ НАДПИСИ "МУЗЫКА В ИГРЕ"

    # -----------------------------------------------------------------------------------------------------------------
    elif self.status == "statistics":  # ОТРИСОВКА ТЕСТОВЫХ ЭЛЕМЕНТОВ ОКНА СТАТИСТИКИ
        label = self.custom_font.render("ТОП 5 ЛУЧШИХ ЗАБЕГОВ: ", 1, (0, 0, 0))  # НАДПИСЬ "ТОП 5 ЛУЧШИХ ЗАБЕГОВ:"
        self.window_surface.blit(label, (self.w // 45, self.h // 90))  # РАЗМЕЩЕНИЕ НАДПИСИ "ТОП 5 ЛУЧШИХ ЗАБЕГОВ:"

        pos_x, start_pos_y = 20, 200  # СТАРТОВАЯ ПОЗИЦИЯ ОТРИСОВКИ ТОПА ЗАБЕГОВ
        for race in range(5):  # ПЕРЕБОР 5 ЛУЧШИХ ЗАБЕГОВ
            if race + 1 <= len(self.best_races):  # ЕСЛИ ТЕКУЩЕЕ КОЛИЧЕСТВО ПЕРЕБЕРАЕМОЕ КОЛ-ВО ЗАБЕГОВ <= ОБЩЕМУ
                text = "; ".join([" ".join(list(i)) for i in self.best_races[race].items()])  # ТЕКСТ С ДАННЫМИ О ЗАБЕГЕ
                current_result = self.custom_font.render(F"{race + 1}. {text}", 1, (0, 0, 0))  # СТРОКА ТОПА
            else:  # ИНАЧЕ (если >= по пред. условию)
                current_result = self.custom_font.render(F"{race + 1}. ПУСТО", 1, (0, 0, 0))  # ОСТАЁТСЯ НАДПИСЬ "ПУСТО"
            self.window_surface.blit(current_result, (pos_x, start_pos_y + 70 * race))  # РАЗМЕЩЕНИЕ ДАННЫХ В ТОПЕ

    # -----------------------------------------------------------------------------------------------------------------
    elif self.status == "pause":  # ОТРИСОВКА ОКНА ПАУЗЫ
        background = pygame.surface.Surface((self.w // 2, self.h * 4 // 5))  # ФОН ПАУЗЫ
        background.fill(BG_COLOR)  # ЗАПОЛНЕНИЕ ФОНА ЦВЕТОМ ДЛЯ ФОНА
        self.window_surface.blit(background, (self.w // 4, self.h // 7))  # РАЗМЕЩЕНИЕ ФОНА НА ОСНОВНОМ ХОЛСТЕ ИГРЫ

        pause_text = "ПАУЗА"
        pause_label = self.custom_font.render(pause_text, 1, (0, 0, 0))  # НАДПИСЬ "ПАУЗА"
        self.window_surface.blit(pause_label, (self.w // 4 + 265, self.h // 7 + 10))  # РАЗМЕЩЕНИЕ НАДПИСИ "ПАУЗА"

        text = "Z - Атака оружием\nQ - Смена оружия\nX - Использование магии\nE - Смена магии\nСтрелочки - перемещение"
        help_label_1 = self.custom_font.render(text, 1, (0, 0, 0))  # ТЕКСТ С ОПИСАНИЕМ УПРАВЛЕНИЯ
        self.window_surface.blit(help_label_1, (self.w // 3 - 80, self.h // 7 + 50))  # РАЗМЕЩЕНИЕ ТЕКСТА С ПОДСКАЗКОЙ

        # ПОДСКАЗКИ О ДЕЙСТВИЯХ ИГРОКА ДЛЯ ПОБЕДЫ
        text = ("Уничтожьте всех 16 врагов на первой локации\n"
                " и направляйтесь в самый верх карты за дверь\n"
                " - на бой с боссом!")
        help_label_2 = self.custom_font_small.render(text, 1, (0, 0, 0))  # ТЕКСТ С ОПИСАНИЕМ НУЖНЫХ ДЛЯ ИГРОКА ДЕЙСТВИЙ
        self.window_surface.blit(help_label_2, (self.w // 3 - 90, self.h // 7 + 320))  # РАЗМЕЩЕНИЕ ТЕКСТА С ПОДСКАЗКОЙ

        # МИНИ-НАДПИСЬ О ЗКАРЫТИИ ОКНА ПАУЗЫ
        pause_exit_text = "ESC - НАЗАД К ИГРЕ"
        pause_exit_label = self.custom_font_small.render(pause_exit_text, 1, (0, 0, 0))
        self.window_surface.blit(pause_exit_label, (self.w // 3 - 80, self.h // 2 + 285))
    # -----------------------------------------------------------------------------------------------------------------
    elif self.status == "end":  # ОТРИСОВКА ОКНА ОКОНЧАНИЯ ИГРЫ (в случае победы)
        background = pygame.surface.Surface((self.w // 2, self.h * 4 // 5))  # ФОН ОКНА ОКАНЧАНИЯ
        background.fill(BG_COLOR)  # ЗАПОЛНЕНИЕ ФОНА ЦВЕТОМ ДЛЯ ФОНА
        self.window_surface.blit(background, (self.w // 4, self.h // 7))  # РАЗМЕЩЕНИЕ ФОНА НА ХОЛСТЕ ИГРЫ

        type_label = self.custom_font.render("ПОБЕДА", 1, (0, 0, 0))  # ТИП ОКОНЧАНИЯ ИГРЫ - ПОБЕДА
        self.window_surface.blit(type_label, (self.w // 4 + 200, self.h // 7 + 50))  # РАЗМЕЩЕНИЕ ТИПА ОКОНЧАНИЯ ИГРЫ

        t = int(self.play_time)  # ИГРОВОЕ ВРЕМЯ
        # ПРЕОБРАЗОВАНИЕ ИГРОВОГО ВРЕМЕНИ В СТРОКУ ФОРМАТА MM:SS
        time_label = self.custom_font.render(F"ВРЕМЯ ИГРЫ: {str(t // 60).rjust(2, "0")}:"
                                             F"{str(t % 60).rjust(2, "0")}", 1, (0, 0, 0))
        self.window_surface.blit(time_label, (self.w // 4 + 20, self.h // 2))  # РАЗМЕЩЕНИЕ ИГРОВОГО ВРЕМЕНИ

        kill_label = self.custom_font.render(F"ВРАГОВ ПОБЕЖДЕНО: 17 / 17", 1, (0, 0, 0))  # ПОБЕЖДЕННЫЕ ВРАГИ
        self.window_surface.blit(kill_label, (self.w // 4 + 20, self.h // 2 - 100))  # РАЗМЕЩЕНИЕ ИХ НА ЭКРАНЕ

    # -----------------------------------------------------------------------------------------------------------------
    elif self.status == "end_loser":  # ОТРИСОВКА ОКНА ОКОНЧАНИЯ ИГРЫ (в случае поражения)
        background = pygame.surface.Surface((self.w // 2, self.h * 4 // 5))  # ФОН ОКНА ОКАНЧАНИЯ
        background.fill(BG_COLOR)  # ЗАПОЛНЕНИЕ ФОНА ЦВЕТОМ ДЛЯ ФОНА
        self.window_surface.blit(background, (self.w // 4, self.h // 7))  # РАЗМЕЩЕНИЕ ФОНА НА ХОЛСТЕ ИГРЫ

        type_label = self.custom_font.render("ПОРАЖЕНИЕ", 1, (0, 0, 0))  # ТИП ОКОНЧАНИЯ ИГРЫ - ПОРАЖЕНИЕ
        self.window_surface.blit(type_label, (self.w // 4 + 200, self.h // 7 + 50))  # РАЗМЕЩЕНИЕ ТИПА ОКОНЧАНИЯ ИГРЫ

        t = int(self.play_time)  # ИГРОВОЕ ВРЕМЯ
        # ПРЕОБРАЗОВАНИЕ ИГРОВОГО ВРЕМЕНИ В СТРОКУ ФОРМАТА MM:SS
        time_label = self.custom_font.render(F"ВРЕМЯ ИГРЫ: {str(t // 60).rjust(2, "0")}:"
                                             F"{str(t % 60).rjust(2, "0")}", 1, (0, 0, 0))
        self.window_surface.blit(time_label, (self.w // 4 + 20, self.h // 2))  # РАЗМЕЩЕНИЕ ИГРОВОГО ВРЕМЕНИ

        kill_label = self.custom_font.render(F"ВРАГОВ ПОБЕЖДЕНО: {self.killed} / 17", 1, (0, 0, 0))  # ПОБЕЖДЕННЫЕ ВРАГИ
        self.window_surface.blit(kill_label, (self.w // 4 + 20, self.h // 2 - 100))  # РАЗМЕЩЕНИЕ ИХ НА ЭКРАНЕ

    # -----------------------------------------------------------------------------------------------------------------
    # p.s.: два последних условия не объеденены в одно, т.к. со стороны разработчика целесообразнее вносить изменения в
    # них по отдельности
# ---------------------------------------------------------------------------------------------------------------------
