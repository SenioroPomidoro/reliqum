from csv import writer


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
