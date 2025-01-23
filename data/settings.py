# ОСНОВНЫЕ ИГРОВЫЕ НАСТРОЙКИ
SCREEN_SIZE = (1400, 900)
TILESIZE = 64
FPS = 60


# ID СПРАЙТОВ НА КОТОРЫХ ИГРОК МОЖЕТ ОТРИСОВЫВАТЬСЯ, ТО ЕСТЬ НЕ БУДЕТ ПРЯТАТЬСЯ ПОД НИМИ.
# КОНФЛИКТОВ МЕЖДУ СПРАЙТАМИ С ОДИНАКОВЫМИ ID НЕ ВОЗНИКНЕТ, Т.К. ВСЕГО В ИГРЕ ИХ НЕ ТАК МНОГО
PASSABLE_IDS = [139, 140, 141, 155, 156, 157, 171, 172, 173, 240, 241, 242, 243, 244, 245, 247, 248, 249]


# ДАННЫЕ О СУЩЕСТВУЮЩЕМ В ИГРЕ ОРУЖИИ
weapon_data = {
    "axe": {"cooldown": 300, "damage": 30, "graphic": "data/images/spriites/weapons/axe/full.png"},
    "lance": {"cooldown": 50, "damage": 8, "graphic": "data/images/spriites/weapons/lance/full.png"}
}

# ДАННЫЕ О СУЩЕСТВУЮЩЕЙ В ИГРЕ МАГИИ
magic_data = {
    "flame": {"strength": 5, "cost": 20, "graphic": "data/images/spriites/magic/flame/fire.png"},
    "heal": {"strength": 20, "cost": 10, "graphic": "data/images/spriites/magic/heal/heal.png"}
}