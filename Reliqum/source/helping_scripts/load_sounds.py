import pygame


# ---------------------------------------------------------------------------------------------------------------------
def load_music(self) -> None:
    """
    Функция, подгружающая музыку
    :param self: объект главного потока (куда будет загружаться музыка)
    """
    self.click = pygame.mixer.Sound("data/sounds/menu_sounds/click.mp3")  # ЗВУК КЛИКА

    self.main_music = pygame.mixer.Sound("data/sounds/menu_sounds/main_music.mp3")  # МУЗЫКА В ГЛАВНО МЕНЮ

    self.game_music = pygame.mixer.Sound("data/sounds/game_sounds/game_music.ogg")  # ИГРОВАЯ МУЗЫКА (до битвы с боссом)
    self.is_game_music_playing = False

    self.boss_music = pygame.mixer.Sound("data/sounds/game_sounds/boss_music.ogg")  # МУЗЫКА БИТВЫ С БОССОМ
    self.is_boss_music_playing = False

    self.win_music = pygame.mixer.Sound("data/sounds/game_sounds/end/win.ogg")  # МУЗЫКА ПОБЕДЫ
    self.is_win_music_playing = False

    self.lose_music = pygame.mixer.Sound("data/sounds/game_sounds/end/lose.ogg")  # МУЗЫКА ПОРАЖЕНИЯ
    self.is_lose_music_playing = False


# ---------------------------------------------------------------------------------------------------------------------
def load_player_sounds(self) -> None:
    """Функция, подгружающая звуки игрока"""
    # ЗВУК ПОЛУЧЕНИЯ УРОНА
    self.oof = pygame.mixer.Sound("data/sounds/game_sounds/entities/player/oof.mp3")

    # ЗВУК ГРАВИТАЦИОННОЙ АТАКИ ПО ИГРОКУ
    self.gravity_oof = pygame.mixer.Sound("data/sounds/game_sounds/entities/player/gravity_oof.mp3")

    # ЗВУК ИСПОЛЬЗОВАНИЯ ЗАКЛИНАНИЯ ЛЕЧЕНИЯ
    self.heal_sound = pygame.mixer.Sound("data/sounds/game_sounds/entities/player/heal.wav")

    # ЗВУК ИСПОЛЬЗОВАНИЯ ОГНЕННОГО ЗАКЛИНАНИЯ
    self.fire_sound = pygame.mixer.Sound("data/sounds/game_sounds/entities/player/fire.wav")

    # ЗВУК ВЗМАХА ОРУЖИЕМ
    self.slash_sound = pygame.mixer.Sound("data/sounds/game_sounds/entities/player/slash.wav")


# ---------------------------------------------------------------------------------------------------------------------
def load_enemies_sounds(self) -> None:
    """Функция, подгружающая звуки врагов"""

    # ЗВУК ПОЛУЧЕНИЯ УРОНА
    self.hit_sound = pygame.mixer.Sound("data/sounds/game_sounds/entities/enemies/hit.wav")

    # ЗВУК СМЕРТИ ВРАГА
    self.death_sound = pygame.mixer.Sound("data/sounds/game_sounds/entities/enemies/monster_death.wav")


# ---------------------------------------------------------------------------------------------------------------------
def off_all_game_music(self) -> None:
    """
    Функция, завершающая проигрывание всей игровой музыки
    :param self: объект главного потока (куда будет загружаться музыка)
    """

    self.game_music.stop()  # ОСТАНОВКА ИГРОВОЙ МУЗЫКИ НА ГЛАВНОМ УРОВНЕ
    self.is_game_music_playing = False

    self.boss_music.stop()  # ОСТАНОВКА ИГРОВОЙ МУЗЫКИ НА УРОВНЕ С БОССОМ
    self.is_boss_music_playing = False

    self.win_music.stop()  # ОСТАНОВКА ПОБЕДНОЙ МУЗЫКИ
    self.is_win_music_playing = False

    self.lose_music.stop()  # ОСТАНОВКА МУЗЫКИ ПОРАЖЕНИЯ
    self.is_lose_music_playing = False

# ---------------------------------------------------------------------------------------------------------------------
