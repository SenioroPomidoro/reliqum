from csv import writer
import pygame
import pygame_gui


def write_settings_csv(self):
    """Функция сохранения настроек в файл с настройками"""
    headers = ["main_music_value", "ingame_music_value"]  # ЗАГОЛОВКИ СТОЛБЦОВ В ФАЙЛЕ С НАСТРОЙКАМИ
    data = [self.temprorary_main_music_val, self.temprorary_ingame_music_val]  # ДАННЫЕ С НАСТРОЙКАМИ

    with open("data/settings.csv", "w") as settings_file:  # ЗАПИСЬ ДАННЫХ В ФАЙЛ settings.csv
        writer_obj = writer(settings_file, delimiter=",")  # ОПРЕДЕЛЕНИЯ ОБЪЕКТА С ФАЙЛОМ НАСТРОЕК
        writer_obj.writerow(headers)  # ЗАПИСЬ СТРОКИ С ЗАГОЛОВКАМИ
        writer_obj.writerow(data)  # ЗАПИСЬ СТРОКИ С ДАННЫМИ

    # ВРЕМЕННЫЕ ЗНАЧЕНИЯ ГРОМКОСТИ СТАНОВЯТСЯ НЕ ВРЕМЕННЫМИ
    self.main_music_val = self.temprorary_main_music_val
    self.ingame_music_val = self.temprorary_ingame_music_val


def slider_moved_process(self, event):
    if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:  # ОБРАБОТКА СДВИГА СЛАЙДЕРА
        if event.ui_element == self.main_menu_music_slider:  # ИЗМЕНЕНИЕ ГРОМКОСТИ МУЗЫКИ В МЕНЮ
            self.temprorary_main_music_val = self.main_menu_music_slider.get_current_value()
        if event.ui_element == self.game_music_slider:  # ИЗМЕНЕНИЕ ГРОМКОСТИ МУЗЫКИ В ИГРЕ
            self.temprorary_ingame_music_val = self.game_music_slider.get_current_value()
