TILESIZE = 64
FPS = 60


# ID спрайтов НА которых игрок может отрисовываться (не будет прятаться под ними)
# Конфликтов между спрайтами с одинаковыми ID не возникнет, т.к. всего в игре их не так много
PASSABLE_IDS = [139, 140, 141, 155, 156, 157, 171, 172, 173, 240, 241, 242, 243, 244, 245, 247, 248, 249]


weapon_data = {
    "axe": {"cooldown": 300, "damage": 30, "graphic": "images/spriites/weapons/axe/full.png"},
    "lance": {"cooldown": 50, "damage": 8, "graphic": "images/spriites/weapons/stick/full.png"}
}