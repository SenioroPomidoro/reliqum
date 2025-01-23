from source.menu.menu_windows.main_menu import MainMenu
from source.game.game_main import Game
# ФАЙЛ ДЛЯ УСТРАНЕНИЯ ПРОБЛЕМ С ЦИКЛИЧЕСКИМ ИМПОРТОМ, СОДЕРЖИТ ФУНКЦИИ, ВОЗВРАЩАЮЩИЕ ТЕ ИЛИ ИНЫЕ ОБЪЕКТЫ ОКОН


def main_menu(w, h, music=None):
    return MainMenu(w, h, music)


def game_window(w, h):
    return Game(w, h)
