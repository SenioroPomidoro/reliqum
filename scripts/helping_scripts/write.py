from csv import writer


def write_settings_csv(self):

    headers = ["main_music_value", "ingame_music_value"]
    data = [self.temprorary_main_music_val, self.temprorary_ingame_music_val]

    with open("data/settings.csv", "w") as settings_file:
        writer_obj = writer(settings_file, delimiter=",")
        writer_obj.writerow(headers)
        writer_obj.writerow(data)

    self.main_music_val = self.temprorary_main_music_val
    self.ingame_music_val = self.temprorary_ingame_music_val
