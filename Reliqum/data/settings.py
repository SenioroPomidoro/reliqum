# ОСНОВНЫЕ ИГРОВЫЕ НАСТРОЙКИ
BG_COLOR = "#483c32"  # ЦВЕТ ФОНА
SCREEN_SIZE = (1280, 720)  # РАЗМЕРЫ ЭКРАНА В ПИКСЕЛЯХ
TILESIZE = 64  # РАЗМЕРЫ ИГРОВОЙ ПЛИТКИ В ПИКСЕЛЯХ
FPS = 60  # ЧАСТОТА ОБНОВЛЕНИЯ ЭКРАНА


# ID СПРАЙТОВ НА КОТОРЫХ ИГРОК МОЖЕТ ОТРИСОВЫВАТЬСЯ, ТО ЕСТЬ НЕ БУДЕТ ПРЯТАТЬСЯ ПОД НИМИ.
# КОНФЛИКТОВ МЕЖДУ СПРАЙТАМИ С ОДИНАКОВЫМИ ID НЕ ВОЗНИКНЕТ, Т.К. ВСЕГО В ИГРЕ ИХ НЕ ТАК МНОГО
PASSABLE_IDS = [139, 140, 141, 155, 156, 157, 171, 172, 173, 240, 241, 242, 243, 244, 245, 247, 248, 249]

# ----------------------------------------------------------------------------------------------------------------------
# ДАННЫЕ ОБ ОРУЖИИ
"""
    :param cooldown: время перезарядки оружия в миллисекундах 
    :param damage: урон оружия в очках здоровья
    :param graphic: путь до папки с графикой оружия 
"""
weapon_data = {
    "axe": {"cooldown": 100, "damage": 15, "graphic": "data/images/sprites/weapons/axe/full.png"},
    "lance": {"cooldown": -50, "damage": 4, "graphic": "data/images/sprites/weapons/lance/full.png"}
}


# ----------------------------------------------------------------------------------------------------------------------
# ДАННЫЕ О МАГИИ
"""
    :param strength: показатель урона магии или любого другого магического действя, которое она оказывает
    :param cost: стоимость магии в очках энергии
    :param graphic: путь до папки с графикой оружия
"""
magic_data = {
    "flame": {"strength": 5, "cost": 20, "graphic": "data/images/sprites/magic/flame/fire.png"},
    "heal": {"strength": 20, "cost": 10, "graphic": "data/images/sprites/magic/heal/heal.png"}
}
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
# ДАННЫЕ О ВРАГАХ
"""
    :param health: уровень здоровья монстра
    :param damage: урон монстра
    :param attack_type: тип атаки монстра (используется для отрисовки визуального эффекта)
    :param speed: скорость врага
    :param resistance: показатель того, насколько сильно будет отбрасываться враг при ударе по нему
    :param attack_radius: радиус, в котором враг может атаковать игрока
    :param notice_radius: радиус, в котором враг начинает сближаться с игроком
"""
monster_data = {
    "Eye": {"health": 75, "damage": 15, "attack_type": "slash",
            "speed": 3.5, "resistance": 2, "attack_radius": 50, "notice_radius": 500},
    "Bamboo": {"health": 700, "damage": 25, "attack_type": "bamboo",
               "speed": 3, "resistance": 0.5, "attack_radius": 160, "notice_radius": 2000},
    "Spirit": {"health": 150, "damage": 7, "attack_type": "spirit",
               "speed": 6, "resistance": 1, "attack_radius": 50, "notice_radius": 400},
    "Owl": {"health": 400, "damage": 3, "attack_type": "gravity",
            "speed": 4, "resistance": 1, "attack_radius": 70, "notice_radius": 2000},
    "Flam": {"health": 250, "damage": 20, "attack_type": "flame",
             "speed": 4, "resistance": 1, "attack_radius": 70, "notice_radius": 400}
}

# ----------------------------------------------------------------------------------------------------------------------
