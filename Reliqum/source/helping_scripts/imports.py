from csv import reader
from os import walk

import pygame

# ---------------------------------------------------------------------------------------------------------------------


def import_csv_layout(path) -> list:
    """
    Функция, обрабатывающая csv-файл с картой и преобразующая его в многомерноый список
    :param path: путь до файла с картой
    """
    terrain_map = []  # НУЖНЫЙ СПИСОК
    with open(path) as level_map:  # ОТКРЫТИЕ ФАЙЛА КАРТЫ
        layout = reader(level_map, delimiter=",")  # ЧИТАТЕЛЬ ФАЙЛА
        for row in layout:  # ДЛЯ КАЖДОЙ СТРОКИ В ФАЙЛЕ
            terrain_map.append(list(row))  # ДОБАВЛЯЕМ СТРОКУ В НУЖНЫЙ СПИСОК
    return terrain_map  # -> НУЖНЫЙ СПИСОК

# ---------------------------------------------------------------------------------------------------------------------


def import_graphics(path) -> dict:
    """
    Функция, импортирующая нужные эелементы графики
    :param path: путь до папки с графикой плиток
    """
    surface_dict = dict()  # СЛОВРЬ С ГРАФИКОЙ

    for _, __, img_files in walk(path):  # ПЕРЕБОР СПИСКОВ С КАРТИНКАМИ В ПОДПАПКАХ ПАПКИ
        for image in img_files:  # НАЗВАНИЕ КАРТИНОК
            full_path = path + "/" + image  # ПОЛНЫЙ ПУТЬ ДО ФАЙЛОВ С ГРАФИКОЙ
            image_surface = pygame.image.load(full_path).convert_alpha()  # ПРЕВРАЩЕНИЕ НУЖНОЙ КАРТИНКИ В СЛОЙ pygame
            surface_dict[image.split(".")[0]] = image_surface  # ПЕРЕДАЧА КАРТИНКИ С ГРАФИКОЙ В СЛОВРЬ
    return surface_dict  # -> СЛОВАРЬ С ГРАФИКОЙ

# ---------------------------------------------------------------------------------------------------------------------


def import_music_settings(self) -> None:
    """
    Функция, импортирующая показатели громкости музыки и записывающая их в атрибуты нужного объекта
    :param self: ОБЪЕКТ ГЛАВНОГО ПОТОКА
    """
    with open("data/sounds/music_volume.csv", newline="") as file:  # ОТКРЫТИЕ ФАЙЛА
        file_data = list(reader(file, delimiter=","))  # СЧИТЫВАНИЕ ФАЙЛ
        data = {file_data[0][i]: file_data[1][i] for i in range(len(file_data[0]))}  # ИЗМЕНЕНИЕ ФАЙЛА ПОД СВОИ НУЖДЫ

    self.main_music_value = int(data["main_music_value"])  # ГРОМКОСТЬ МУЗЫКИ В МЕНЮ
    self.ingame_music_value = int(data["ingame_music_value"])  # ГРОМКОСТЬ МУЗЫКИ В ИГРЕ


# ---------------------------------------------------------------------------------------------------------------------
