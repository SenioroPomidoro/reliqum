import pygame
from data.settings import *
from source.game.sub_menu_scripts.entity import Entity


class Player(Entity):
    def __init__(self, pos: tuple, groups: list, obstacle_sprites: pygame.sprite.Group,
                 create_attack, destroy_attack, create_magic):
        """
        Инициализация объекта игрока
        :param pos: позиция игрока на карте
        :param groups: группы спрайтов, в которые помещается игрок
        :param obstacle_sprites: набор спрайтов, через которые игрок пройти не может
        :param create_attack: функция, создающая атаку
        :param destroy_attack: функция, удаляющая атаку
        :param create_magic: функция, создающая магию
        """
        super().__init__(groups)  # ВЫЗОВ РОДИТЕЛЬСКОЙ ФУНКЦИИ ИНИЦИАЛИЗАЦИИ ДЛЯ ЗАПИСИ СПРАЙТА В ГРУППЫ ИЗ groups

        # ПОДГРУЗКА И РАСПОЛОЖЕНИЕ ИГРОКА В СТАНДАРТНОЙ ПОЗИЦИИ - СТОИТ И СМОТРИТ ВНИЗ
        self.image = pygame.image.load('data/images/sprites/main_hero/down_idle/down_idle.png').convert_alpha()
        self.image = self.image.subsurface(pygame.Rect(0, 0, 50, 50))  # ВЫРЕЗКА ЧЕЛОВЕЧЕКА 50 НА 50 ПИКСЕЛЕЙ

        self.obstacle_sprites = obstacle_sprites  # ЗАПИСЬ ГРУППЫ СПРАЙТОВ, ЧЕРЕЗ КОТОРЫЕ
        # ИГРОК НЕ МОЖЕТ ПРОЙТИ В АТРИБУТЫ ОБЪЕКТА ИГРОКА
        self.sprite_type = "None"  # ТИП СПРАЙТА - None
        self.sprite_id = -1  # УНИКАЛЬНЫЙ НОМЕР СПРАЙТА -1 (ничего не значит)

        self.rect = self.image.get_rect(topleft=pos)  # ПОЛУЧЕНИЕ ЧЕТЫРЕХУГОЛЬНИКА, В КОТОРОМ НАХОДИТСЯ ИЗОБРАЖЕНИЕ
        self.hitbox = self.rect.inflate(0, -6)  # УМЕНЬШЕНИЕ ХИТБОКСА НА 3 ПИКСЕЛЯ СВЕРХУ И СНИЗУ (для более гармо-
        # ничного пересечения спрайтов)

        # ГРАФИКА
        self.import_player_assets()  # ЗАГРУЗКА СПРАЙТОВ ИГРОКА
        self.status = "down"  # СТАТУС ИГРОКА, ОПРЕДЕЛЯЮЩИЙ НАПРАВЛЕНИЕ И ХАРАКТЕР ДВИЖЕНИЯ, ИЗНАЧАЛЬНО ДВИЖЕТСЯ ВНИЗ.

        # ОРИЕНТАЦИЯ ИГРОКА
        self.attacking = False  # АТАКУЕТ ЛИ ИГРОК. ИЗНАЧАЛЬНО - НЕТ
        self.attack_cooldown = 200  # ПРОМЕЖУТОК МЕЖДУ АТАКАМИ ИГРОКА
        self.attack_time = None  # ВРЕМЯ АТАКИ

        # ОРУЖИЕ
        self.create_attack = create_attack  # ЗАПИСЬ ФУНКЦИИ, СОЗДАЮЩЕЙ АТАКУ В АТРИБУТЫ ОБЪЕКТА
        self.destroy_attack = destroy_attack  # ЗАПИСЬ ФУНКЦИИ, УНИЧТОЖАЮЩЕЙ АТАКУ В АТРИБУТЫ ОБЪЕКТА
        self.weapon_index = 0  # ИНДЕКС ВЫБРАННОГО ОРУЖИЯ, ПО УМОЛЧАНИЮ - 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]  # НАЗВАНИЕ ОРУЖИЯ
        self.weapon_data = weapon_data
        self.can_switch_weapon = True  # МОЖЕТ ЛИ ИГРОК СМЕНИТЬ ОРУЖИЕ. ПО УМОЛЧАНИЮ - ДА
        self.weapon_switch_time = None  # ВРЕМЯ, КОТОРОЕ ИГРОК МЕНЯЕТ ОРУЖИЕ

        # МАГИЯ
        self.create_magic = create_magic  # ЗАПИСЬ ФУНКЦИИ, СОЗДАЮЩЕЙ МАГИЧЕСКУ АТАКУ В АТРИБУТЫ ОБЪЕКТА
        self.magic_index = 0  # ИНДЕКС ВЫБРАННОЙ МАГИИ, ПО УМОЛЧАНИЮ - 0
        self.magic = list(magic_data.keys())[self.magic_index]  # СПИСОК ДАННЫХ ОБ ОРУЖИИ
        self.can_switch_magic = True  # МОЖЕТ ЛИ ИГРОК СМЕНИТЬ МАГИЮ. ПО УМОЛЧАННИЮ - ДА
        self.magic_switch_time = None  # ВРЕМЯ, КОТОРОЕ ИГРОК МЕНЯЕТ МАГИЮ

        self.switch_duration_cooldown = 500  # ВРЕМЯ МЕЖДУ СМЕНОЙ ОРУЖИЯ И МАГИИ

        # ЗАПИСЬ ПОКАЗАТЕЛЕЙ ПЕРСОНАЖА В АТРИБУТЫ ОБЪЕКТА ПЕРСОНАЖА
        # УРОН = УРОН ОРУЖИЯ + УРОН ИГРОКА / АНАЛОГИЧНО С МАГИЕЙ
        self.stats = {"health": 100, "energy": 60, "attack": 0, "magic": 4, "speed": 6}
        self.health = self.stats["health"]  # ЗАПИСЬ ЗДОРОВЬЯ ПЕРСОНАЖА
        self.energy = self.stats["energy"]  # ЗАПИСЬ ЭНЕРГИИ ПЕРСОНАЖА
        self.speed = self.stats["speed"]  # ЗАПИСЬ СКОРОСТИ ПЕРСОНАЖА
        self.exp = 123  # ЗАПИСЬ ОПЫТА ПЕРСОНАЖА

        self.vulnerable = True
        self.hurt_time = None
        self.invulnerability_duration = 500

    def import_player_assets(self) -> None:
        """Функция для импорта спрайтов игрока"""
        character_path = "data/images/sprites/main_hero/"  # ПУТЬ ДО ПАПКИ С ПАПКАМИ СПРАЙТОВ ИГРОКА

        # СЛОАВРЬ С ИЗОБРАЖЕНИЯМИ СПРАЙТОВ
        self.animations = {"up": [], "down": [], "left": [], "right": [],
                           "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": [],
                           "up_attack": [], "down_attack": [], "left_attack": [], "right_attack": []}

        for animation in self.animations.keys():  # ЗАБОР СПРАЙТОВ В СЛОВАРЬ СО СПРАЙТАМИ
            full_path = character_path + animation
            self.animations[animation] = pygame.image.load(F"{full_path}/{animation}.png").convert_alpha()

    def input(self) -> None:
        """Функция обработки нажатий на клавишы"""
        if self.attacking:  # ЕСЛИ ИГРОК В ДАННЫЙ МОМЕНТ АТАКУЕТ - НИЧЕГО НЕ ПРОИСХОДИТ
            return

        keys = pygame.key.get_pressed()  # СЛОВРЬ С НАЖАТЫМИ В ДАННЫЙ МОМЕНТ КЛАВИШАМИ

        # ДВИЖЕНИЕ
        if keys[pygame.K_UP]:  # ДВИЖЕНИЕ ВВЕРХ
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:  # ДВИЖЕНИЕ ВНИЗ
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:  # ДВИЖЕНИЕ ВПРАВО
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT]:  # ДВИЖЕНИЕ ВЛЕВО
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0

        # АТАКА
        if keys[pygame.K_z]:  # УДАР ОРУЖИЯ
            self.attacking = True  # ИЗМЕНЕНИЯ СОСТОЯНИЯ ИГРОКА НА АТАКУЮЩЕЕ
            self.attack_time = pygame.time.get_ticks()  # ФИКСАЦИЯ МОМЕНТА ВРЕМЕНИ, В КОТОРЫЙ ИГРОК АТАКОВАЛ
            self.create_attack()  # СОЗДАНИЕ СПРАЙТА АТАКИ

        if keys[pygame.K_x]:  # ИСПОЛЬЗОВАНИЕ МАГИИ
            self.attacking = True  # ИЗМЕНЕНИЯ СОСТОЯНИЯ ИГРОКА НА АТАКУЮЩЕЕ
            self.attack_time = pygame.time.get_ticks()  # ФИКСАЦИЯ МОМЕНТА ВРЕМЕНИ, В КОТОРЫЙ ИГРОК ИСПОЛЬЗОВАЛ МАГИЮ

            style = list(magic_data.keys())[self.magic_index]  # ТИП МАГИИ
            strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]  # УРОН МАГИИ
            cost = list(magic_data.values())[self.magic_index]["cost"]  # ЦЕНА ЭНЕРГИИ ЗА ИСПОЛЬЗОВАНИЕ МАГИИ
            self.create_magic(style, strength, cost)  # СОЗДАНИЕ МАГИИ

        if keys[pygame.K_q] and self.can_switch_weapon:  # СМЕНА ОРУЖИЯ
            self.can_switch_weapon = False  # ИГРОК НЕ МОЖЕТ МЕНЯТЬ ОРУЖИЕ
            self.weapon_switch_time = pygame.time.get_ticks()  # ФИКСАЦИЯ МОМЕНТА ВРЕМЕНИ, В КОТОРЫЙ ПРОИЗОШЛА СМЕНА
            self.weapon_index = (self.weapon_index + 1) % len(list(weapon_data.keys()))  # ПОЛУЧЕНИЕ НОВОГО ИНДЕКСА
            self.weapon = list(weapon_data.keys())[self.weapon_index]  # ВЫБОР СЛЕДУЮЩЕГО ОРУЖИЯ

        if keys[pygame.K_e] and self.can_switch_magic:  # СМЕНА МАГИИ
            self.can_switch_magic = False  # ИГРОК НЕ МОЖЕТ МЕНЯТЬ МАГИЮ
            self.magic_switch_time = pygame.time.get_ticks()  # ФИКСАЦИЯ МОМЕНТА ВРЕМЕНИ, В КОТОРЫЙ ПРОИЗОШЛА СМЕНА
            self.magic_index = (self.magic_index + 1) % len(list(magic_data.keys()))  # ПОЛУЧЕНИЕ НОВОГО ИНДЕКСА
            self.magic = list(magic_data.keys())[self.magic_index]  # ВЫБОР СЛЕДУЮЩЕЙ МАГИИ

    def get_status(self) -> None:
        """Функция для получения текущего статуса игрока"""
        if self.direction.x == 0 and self.direction.y == 0:  # ЕСЛИ ИГРОК СТОИТ И НЕ ДЕЛАЕТ НИКАКИХ ДЕЙСТВИЙ, ТО
            # ЕГО СТАТУС СТАНОВИТСЯ РАВНЫМ направлениедвижения_idle
            if "idle" not in self.status and "attack" not in self.status:
                self.status = self.status + "_idle"

        if self.attacking:  # ЕСЛИ ИГРОК АТАКУЕТ, ТО ЕГО ДВИЖЕНИЕ ПРЕКРАЩАЕТСЯ И СТАТУС СТАНОВИТСЯ
            # направлениедвижение_attack
            self.direction.x = 0
            self.direction.y = 0
            if "attack" not in self.status:
                if "idle" in self.status:
                    self.status = self.status.replace("_idle", "_attack")
                else:
                    self.status = self.status + "_attack"
        else:
            if "attack" in self.status:
                self.status = self.status.replace("_attack", "")

    def cooldowns(self) -> None:
        """Функция-таймер для отработки задержек между действиями"""
        current_time = pygame.time.get_ticks()  # ТЕКУЩИЙ МОМЕНТ ВРЕМЕНИ

        if self.attacking:  # ЕСЛИ ИГРОК АТАКУЕТ
            if current_time - self.attack_time >= self.attack_cooldown + self.weapon_data[self.weapon]["cooldown"]:  # ЕСЛИ ВРЕМЯ АТАКИ ИСТЕКЛО
                self.attacking = False  # ИГРОК НЕ АТАКУЕТ
                self.destroy_attack()  # СПРАЙТ ОРУЖИЯ / МАГИИ УНИЧТОЖАЕТСЯ

        if not self.can_switch_weapon:  # ЕСЛИ ИГРОК НЕ МОЖЕТ СМЕНИТЬ ОРУЖИЕ
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:  # ЕСЛИ КУЛДАУН СМЕНЫ ИСТЕК
                self.can_switch_weapon = True  # МЕНЯТЬ ОРУЖИЕ МОЖНО

        if not self.can_switch_magic:  # ЕСЛИ ИГРОК НЕ МОЖЕТ СМЕНИТЬ МАГИЮ
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:  # ЕСЛИ КУЛДАУН СМЕНЫ ИСТЕК
                self.can_switch_magic = True  # МЕНЯТЬ МАГИЮ МОЖНО

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def animate(self) -> None:
        """Функция, осуществляющая анимацию движения игрока"""
        animation = self.animations[self.status]  # ПОЛУЧЕНИЕ НУЖНО ИЗОБРАЖЕНИЯ ДЛЯ АНИМАЦИИ
        if "idle" not in self.status and "attack" not in self.status:
            loop_count = 4  # ЕСЛИ ИГРОК ПЕРЕДВИГАЕТСЯ, ТО КОЛИЧЕСТВО ИТЕРАЦИЙ ПО КАРТИНКЕ БУДЕТ РАВНО 4,
            # (движение разбито по 4 кадра на 4 направления)
        else:
            loop_count = 0

        self.frame_index += self.animation_speed  # СМЕНА КАДРА (если есть необходимость)
        if self.frame_index >= loop_count:
            self.frame_index = 0

        # ОТРИСОВКА ИЗОБРАЖЕНИЯ
        self.image = animation.subsurface(pygame.Rect((0, int(self.frame_index) * 50 + 1, 50, 49)))
        self.rect = self.image.get_rect(center=self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def get_full_weapon_damage(self) -> int:
        base_damage = self.stats["attack"]
        weapon_damage = self.weapon_data[self.weapon]["damage"]
        return base_damage + weapon_damage

    def update(self) -> None:
        """Функция для обновления игрока"""
        self.input()  # ОБРАБОТКА КЛАВИШ
        self.cooldowns()  # ОБРАБОТКА КУЛДАУНОВ (ЗАДЕРЖЕК)
        self.get_status()  # ОБНОВЛЕНИЕ СТАТУСА ИГРОКА
        self.animate()  # АНИМАЦИЯ ИГРОКА
        self.move(self.speed)  # ПЕРЕДВИЖЕНИЕ ИРОКА
