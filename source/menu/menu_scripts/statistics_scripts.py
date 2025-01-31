from csv import DictReader

# ---------------------------------------------------------------------------------------------------------------------


def grab_best_races() -> list:
    """Функция, возвращающая забеги"""
    with open("data/races/races.csv", "r") as file:  # ОТКРЫТИЯ ФАЙЛА С ЗАБЕГАМИ
        reader = DictReader(file, delimiter=";")  # ОБЪЕКТ-ЧИТАТЕЛЬ ДЛЯ ФАЙЛА С ЗАБЕГАМИ
        rows = [item.values() for item in reader]  # СПИСОК КОРТЕЖЕЙ ЗНАЧЕНИЯ СТРОК С ЗАБЕГАМИ
        data = [{"ЗАТРАЧЕННОЕ ВРЕМЯ:":
                F"{str(int(time) // 60).rjust(2, "0")}:{str(int(time) % 60).rjust(2, "0")}",
                 "ПОВЕРЖЕНО ВРАГОВ:": F"{kills} / 17"
                 } for time, kills in rows]  # ОТБОР ДАННЫХ В НЕОБХОДИМОМ ФОРМАТЕ
        return data  # ВОЗВРАЩЕНИЕ СПИСКА С НУЖНЫМИ ДАННЫМИ

# ---------------------------------------------------------------------------------------------------------------------
