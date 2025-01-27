import pygame
from data.settings import BG_COLOR


def draw_labels(self):
    """Функция отрисовки текстовых элементов в тех или иных окнах в меню"""
    if self.status is None:
        return

    if self.status == "main":  # ОТРИСОВКА ТЕКСТОВЫХ ЭЛЕМЕНТОВ ОКНА ГЛАВНОГО МЕНЮ
        label = self.custom_font.render("F4 - ПОЛНЫЙ ЭКРАН", 1, (0, 0, 0))
        self.window_surface.blit(label, (self.w // 90, self.h - self.custom_font.get_height()))
        self.window_surface.blit(self.game_label, (20, 20))

    elif self.status == "settings":  # ОТРИСОВКА ТЕКСТОВЫХ ЭЛЕМЕНТОВ ОКНА НАСТРОЕК
        main_label = self.custom_font.render("МУЗЫКА В МЕНЮ", 1, (0, 0, 0))
        game_label = self.custom_font.render("МУЗЫКА В ИГРЕ", 1, (0, 0, 0))

        main_music_val_label = self.custom_font.render(str(self.temprorary_main_music_val), 1, (0, 0, 0))
        game_music_val_label = self.custom_font.render(str(self.temprorary_ingame_music_val), 1, (0, 0, 0))

        self.window_surface.blit(main_music_val_label, (500, 140))
        self.window_surface.blit(game_music_val_label, (500, 440))

        self.window_surface.blit(main_label, (self.w // 90, 100))
        self.window_surface.blit(game_label, (self.w // 90, 400))

    elif self.status == "pause":
        background = pygame.surface.Surface((self.w // 2, self.h * 4 // 5))
        background.fill(BG_COLOR)
        self.window_surface.blit(background, (self.w // 4, self.h // 7))

        pause_label = self.custom_font.render("ПАУЗА", 1, (0, 0, 0))
        self.window_surface.blit(pause_label, (self.w // 4 + 300, self. h // 7 + 50))

    elif self.status == "end":
        background = pygame.surface.Surface((self.w // 2, self.h * 4 // 5))
        background.fill(BG_COLOR)
        self.window_surface.blit(background, (self.w // 4, self.h // 7))

        type_label = self.custom_font.render("ПОБЕДА", 1, (0, 0, 0))
        self.window_surface.blit(type_label, (self.w // 4 + 200, self.h // 7 + 50))

        t = int(self.play_time)
        time_label = self.custom_font.render(F"ВРЕМЯ ИГРЫ: {str(t // 60).rjust(2, "0")}:"
                                             F"{str(t % 60).rjust(2, "0")}", 1, (0, 0, 0))
        self.window_surface.blit(time_label, (self.w // 4 + 20, self.h // 2))

        kill_label = self.custom_font.render(F"ВРАГОВ ПОБЕЖДЕНО: 17 / 17", 1, (0, 0, 0))
        self.window_surface.blit(kill_label, (self.w // 4 + 20, self.h // 2 - 100))

    elif self.status == "end_loser":
        background = pygame.surface.Surface((self.w // 2, self.h * 4 // 5))
        background.fill(BG_COLOR)
        self.window_surface.blit(background, (self.w // 4, self.h // 7))

        type_label = self.custom_font.render("ПОРАЖЕНИЕ", 1, (0, 0, 0))
        self.window_surface.blit(type_label, (self.w // 4 + 200, self.h // 7 + 50))

        t = int(self.play_time)
        time_label = self.custom_font.render(F"ВРЕМЯ ИГРЫ: {str(t // 60).rjust(2, "0")}:"
                                             F"{str(t % 60).rjust(2, "0")}", 1, (0, 0, 0))
        self.window_surface.blit(time_label, (self.w // 4 + 20, self.h // 2))

        kill_label = self.custom_font.render(F"ВРАГОВ ПОБЕЖДЕНО: {self.killed} / 17", 1, (0, 0, 0))
        self.window_surface.blit(kill_label, (self.w // 4 + 20, self.h // 2 - 100))
