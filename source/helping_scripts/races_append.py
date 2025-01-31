from csv import DictReader, DictWriter

# ---------------------------------------------------------------------------------------------------------------------


def append_result(time: int, kills: int) -> None:
    """
    Функция, добавляющая результат забега в общий список забегов
    :param time: игровое время забега
    :param kills: количветсво поверженых врагов (из 17 возможных)
    """
    with open("data/best_races/best_races.csv", "r", newline="") as file:  # ОТКРЫТИЕ csv ФАЙЛА С ЗАБЕГАМИ
        headers = [{"time": "time", "monsters_killed": "monsters_killed"}]  # ЗАГОЛОВКИ csv ФАЙЛА
        reader = DictReader(file, delimiter=";")  # ЧИТАТЕЛЬ csv ФАЙЛА
        data = [row for row in reader]  # ДАННЫЕ ФАЙЛА
        data.append(dict(time=int(time), monsters_killed=kills))  # ДОБАВЛЯЕМ В СПИСОК С ДАННЫМИ ФАЙЛА НОВЫЕ ЗНАЧЕНИЯ
        data.sort(key=lambda x: [int(x["monsters_killed"]), int(float(x["time"]))])  # СОРТИРУЕМ ДАННЫЕ

    with open("data/best_races/best_races.csv", "w", newline="") as file:  # ОТКРЫТИЕ csv ФАЙЛА С ЗАБЕГАМИ НА ЗАПИСЬ
        writer = DictWriter(file, delimiter=";", fieldnames=headers[0].keys())  # ЗАПИСЫВАЮЩИЙ ОБЪЕКТ В csv ФАЙЛ
        writer.writerows(headers + list(reversed(data)))  # ЗАПИСЬ ОТОБРАННЫХ ДАННЫХ С ЗАГОЛОВКАМИ В ФАЙЛ

# ---------------------------------------------------------------------------------------------------------------------
