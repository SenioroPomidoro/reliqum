from csv import DictReader, DictWriter


def append_result(time: int, kills: int) -> None:
    with open("data/best_races/best_races.csv", "r", newline="") as file:
        headers = [{"time": "time", "monsters_killed": "monsters_killed"}]
        reader = DictReader(file, delimiter=";")
        data = [row for row in reader]
        data.append(dict(time=int(time), monsters_killed=kills))
        data.sort(key=lambda x: [int(x["monsters_killed"]), int(float(x["time"]))])

    with open("data/best_races/best_races.csv", "w", newline="") as file:
        writer = DictWriter(file, delimiter=";", fieldnames=headers[0].keys())
        writer.writerows(headers + list(reversed(data)))
