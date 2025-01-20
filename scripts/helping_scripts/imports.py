from csv import reader
from os import walk

import pygame


def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter=",")
        for row in layout:
            terrain_map.append(list(row))
    return terrain_map


def import_graphics(path):
    surface_dict = dict()

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + "/" + image
            image_surface = pygame.image.load(full_path).convert_alpha()
            surface_dict[image.split(".")[0]] = image_surface

    return surface_dict


def import_settings(self):
    with open("data/settings.csv") as file:
        file_data = list(reader(file, delimiter=","))
        data = {file_data[0][i]: file_data[1][i] for i in range(len(file_data[0]))}

    self.main_music_value = int(data["main_music_value"])
    self.ingame_music_value = int(data["ingame_music_value"])


