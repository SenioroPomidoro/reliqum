from csv import DictReader, DictWriter

# ---------------------------------------------------------------------------------------------------------------------


def append_result(time: int, kills: int) -> None:
    """
    Функция, добавляющая результат забега в общий список забегов
    :param time: игровое время забега
    :param kills: количветсво поверженых врагов (из 39 возможных)
    """
    with open("data/races/races.csv", "r", newline="") as file:  # ОТКРЫТИЕ csv ФАЙЛА С ЗАБЕГАМИ
        headers = [{"time": "time", "monsters_killed": "monsters_killed"}]  # ЗАГОЛОВКИ csv ФАЙЛА
        reader = DictReader(file, delimiter=";")  # ЧИТАТЕЛЬ csv ФАЙЛА
        data = [row for row in reader]  # ДАННЫЕ ФАЙЛА
        data.append(dict(time=int(time), monsters_killed=kills))  # ДОБАВЛЯЕМ В СПИСОК С ДАННЫМИ ФАЙЛА НОВЫЕ ЗНАЧЕНИЯ
        data = custom_sort(data)

    with open("data/races/races.csv", "w", newline="") as file:  # ОТКРЫТИЕ csv ФАЙЛА С ЗАБЕГАМИ НА ЗАПИСЬ
        writer = DictWriter(file, delimiter=";", fieldnames=headers[0].keys())  # ЗАПИСЫВАЮЩИЙ ОБЪЕКТ В csv ФАЙЛ
        writer.writerows(headers + list(reversed(data)))  # ЗАПИСЬ ОТОБРАННЫХ ДАННЫХ С ЗАГОЛОВКАМИ В ФАЙЛ

# ---------------------------------------------------------------------------------------------------------------------


def custom_sort(list_: list) -> list:
    """
    Функция осуществляющая пузырьковую сортировку списка словарей со следующим критерием: максимум побежденных врагов
    и минимум затраченного времени
    :param list_: список словарей с данными о забегах
    """
    new_list = list_.copy()  # КОПИЯ ИСХОДНОГО СПИСКА
    for i in range(len(new_list) - 1):  # ПЕРЕБОР ВСЕХ СЛОВАРЕЙ ДО ПОСЛЕДНЕГО
        for j in range(len(new_list) - 1 - i):  # ПЕРЕБОР ВСЕХ СЛОВАРЕЙ ДО ОТСОРТИРОВАННОЙ ЧАСТИ
            time_1, kills_1 = int(new_list[j]["time"]), int(new_list[j]["monsters_killed"])  # ПЕРВЫЙ СЛОВАРЬ
            time_2, kills_2 = int(new_list[j + 1]["time"]), int(new_list[j + 1]["monsters_killed"])  # ВТОРОЙ СЛОВАРЬ

            if kills_1 > kills_2:  # УСЛОВИЕ МАКСИМУМА ПО ВРАГАМ
                new_list[j], new_list[j + 1] = new_list[j + 1], new_list[j]  # МЕНЯЕМ МЕСТАМИ СЛОВАРИ

            elif kills_1 == kills_2:  # ЕСЛИ ОДИНАКОВОЕ КОЛ-ВО ВРАГОВ
                if time_1 < time_2:  # УСЛОВИЕ МИНИМУМА ПО ВРЕМЕНИ
                    new_list[j], new_list[j + 1] = new_list[j + 1], new_list[j]  # МЕНЯЕМ МЕСТАМИ СЛОВАРИ

    return new_list  # -> ОТСОРТИРОВАННЫЙ СПИСОК СО СЛОВАРЯМИ

# ---------------------------------------------------------------------------------------------------------------------
