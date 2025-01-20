def draw_labels(self):
    if self.status is None:
        return

    if self.status == "main":
        label = self.custom_font.render("F4 - ПОЛНЫЙ ЭКРАН", 1, (0, 0, 0))
        self.window_surface.blit(label, (self.w // 90, self.h - self.custom_font.get_height()))
        self.window_surface.blit(self.game_label, (20, 20))

    elif self.status == "settings":

        main_label = self.custom_font.render("МУЗЫКА В МЕНЮ", 1, (0, 0, 0))
        game_label = self.custom_font.render("МУЗЫКА В ИГРЕ", 1, (0, 0, 0))

        main_music_val_label = self.custom_font.render(str(self.temprorary_main_music_val), 1, (0, 0, 0))
        game_music_val_label = self.custom_font.render(str(self.temprorary_ingame_music_val), 1, (0, 0, 0))

        self.window_surface.blit(main_music_val_label, (500, 140))
        self.window_surface.blit(game_music_val_label, (500, 440))

        self.window_surface.blit(main_label, (self.w // 90, 100))
        self.window_surface.blit(game_label, (self.w // 90, 400))
