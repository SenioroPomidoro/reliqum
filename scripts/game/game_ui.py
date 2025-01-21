import pygame
from data.settings import *


class GameUI:
    def __init__(self):

        # ---
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font("../../data/fonts/base_font.ttf", 30)

        # ---
        self.health_bar_rect = pygame.Rect(600, 800, 200, 30)
        self.energy_bar_rect = pygame.Rect(600, 834, 140, 30)

        # ---
        self.weapon_graphics = [pygame.image.load(weapon["graphic"]).convert_alpha() for weapon in weapon_data.values()]
        self.magic_graphics = [pygame.image.load(magic["graphic"]).convert_alpha() for magic in magic_data.values()]

    def show_exp(self, exp):
        text_surf = self.font.render(F"EXP: {int(exp)}", False, "black")
        x = self.display_surface.get_size()[0] - 20
        y = self.display_surface.get_size()[1] - 20
        text_rect = text_surf.get_rect(bottomright=(x, y))

        pygame.draw.rect(self.display_surface, "orange", text_rect.inflate(20, 20))  # фон
        self.display_surface.blit(text_surf, text_rect)  # сам опыт
        pygame.draw.rect(self.display_surface, "black", text_rect.inflate(20, 20), 3)  # границы

    def show_bar(self, current, max_amount, bg_rect, color):
        # отрисовка фона решёток
        pygame.draw.rect(self.display_surface, "black", bg_rect)

        # перевод показателей в пиксели
        ratio = current / max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        # отрисовка заполненности значений у решёток
        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, "black", bg_rect, 4)

    def selection_box(self, left, top, has_switched):
        """Часть окна, изображающая выбранное оружие/магию"""
        bg_rect = pygame.Rect(left, top, 60, 60)
        pygame.draw.rect(self.display_surface, "black", bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface, "gold", bg_rect, 4)
        else:
            pygame.draw.rect(self.display_surface, "brown", bg_rect, 4)
        return bg_rect

    def weapon_overlay(self, weapon_index, has_switched):
        bg_rect = self.selection_box(520, 800, has_switched)  # оружие
        weapon_surf = self.weapon_graphics[weapon_index]
        weapon_rect = weapon_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self, magic_index, has_switched):
        bg_rect = self.selection_box(810, 800, has_switched)  # оружие
        magic_surf = self.magic_graphics[magic_index]
        magic_rect = magic_surf.get_rect(center=bg_rect.center)

        self.display_surface.blit(magic_surf, magic_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats["health"], self.health_bar_rect, "red")
        self.show_bar(player.energy, player.stats["energy"], self.energy_bar_rect, "blue")

        self.show_exp(player.exp)

        self.weapon_overlay(player.weapon_index, player.can_switch_weapon)
        self.magic_overlay(player.magic_index, player.can_switch_magic)
