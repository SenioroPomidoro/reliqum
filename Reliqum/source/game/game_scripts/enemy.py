import pygame

from data.settings import *

from source.game.game_scripts.entity import Entity

from source.helping_scripts.load_sounds import load_enemies_sounds

from random import choice
# ---------------------------------------------------------------------------------------------------------------------


# КЛАСС ВРАГА
class Enemy(Entity):
    # -----------------------------------------------------------------------------------------------------------------
    def __init__(self, monster_name: str, pos: tuple, groups, obstacle_sprites, damage_player, death_particles) -> None:
        """
        Конструктор класса врага
        :param monster_name: имя врага
        :param pos: позиция врага на карте
        :param groups: группы спрайтов, в которых находится враг
        :param obstacle_sprites: спрайты, через которые враг не может пройти
        :param damage_player: урон, наносимый врагом игрокау
        :param death_particles: анимация смерти врага
        """
        # =============================
        super().__init__(groups)  # ВЫЗВОВ КОНСТРУКТОРА РОДИТЕЛЬСКОГО КЛАССА
        self.sprite_type = "enemy"  # ЗАПИСЬ ТИАП СПРАЙТА В АТРИБУТЫ
        self.sprite_id = None  # ЗАПИСЬ ID СПРАЙТА В АТРИБУТЫ
        # =============================
        self.import_graphics(monster_name)  # ПОДГРУЗКА ГРАФИКИ ВРАГА
        self.status = "idle"  # ЗАПИСЬ ИЗНАЧАЛЬНОГО СТАТУСА МОНСТРА В АТРИБУТЫ - СТОЙКА НА МЕСТЕ
        self.image = (pygame.image.load(f"data/images/sprites/monsters/{monster_name}/idle/idle.png").
                      subsurface((0, 0, 48, 48)).convert_alpha())  # ЗАГРУЗКА НАЧАЛЬНОГО ИЗОБРАЖЕНИЯ ВРАГА
        # =============================
        # ДВИЖЕНИЕ
        self.rect = self.image.get_rect(topleft=pos)  # ОПРЕДЕЛЕНИЕ НАЧАЛЬНОГО ПОЛОЖЕНИЯ ВРАГА В ПРОСТРАНСТВЕ
        self.hitbox = self.rect.inflate(0, -10)  # ОПРЕДЕЛЕНИЕ ХИТБОКСА ВРАГА (сверху и снизу -5 пикселей)
        self.obstacle_sprites = obstacle_sprites  # ЗАПИСЬ СПРАЙТОВ, ЧЕРЕЗ КОТОРЫЕ ВРАГ НЕ МОЖЕТ ПРОЙТИ В АТРИБУТЫ
        # =============================
        # ПОКАЗАТЕЛИ ВРАГА
        self.monster_name = monster_name  # ЗАПИСЬ ИМЕНИ ВРАГА
        monster_info = monster_data[self.monster_name]  # ИНФОРМАЦИЯ О ВРАГЕ В ВИДЕ СЛОВАРЯ
        self.health = monster_info["health"]  # ЗАПИСЬ ЗДОРОВЬЯ ВРАГА
        self.speed = monster_info["speed"]  # ЗАПИСЬ СКОРОСТИ ВРАГА
        self.attack_damage = monster_info["damage"]  # ЗАПИСЬ УРОНА ВРАГА
        self.resistance = monster_info["resistance"]  # ЗАПИСЬ ТОГО, НАСКОЛЬКО СИЛЬНО ВРАГ ОТКИДЫВАЕТСЯ ПОСЛЕ УРОНА
        self.attack_radius = monster_info["attack_radius"]  # ЗАПИСЬ РАДИУСА АТАКИ ВРАГА
        self.notice_radius = monster_info["notice_radius"]  # ЗАПИСЬ РАДИУСА ОБНАРУЖЕНИЯ ВРАГА
        self.attack_type = monster_info["attack_type"]  # ЗАПИСЬ ТИПА АТАКИ ВРАГА
        self.is_awaken = False  # ПАРАМЕТР, ОПРЕДЕЛЯЮЩИЙ ПРОБУЖДЁН ВРАГ ИЛИ НЕТ (меняются его статы)
        # =============================
        # ВЗАИМОДЕЙСТВИЕ ВРАГА С ИГРОКОМ
        self.can_attack = True  # МОЖЕТ ЛИ ВРАГ АТАКОВАТЬ ВРАГА
        self.hit_counter = 0  # КОЛИЧЕСТВО УДАРОВ, КОТОРЫЕ ПРИНЯЛ НА СЕБЯ ВРАГ
        self.attack_time = None  # МОМЕНТ ВРЕМЕНИ В КОТОРЫЙ ВРАГ НАНЁС УРОН
        self.attack_cooldown = 400  # КУЛДАУН МЕЖДУ УДАРАМИ ВРАГА
        self.damage_player = damage_player  # ФУНКЦИЯ, ОБРАБАТЫВАЮЩАЯ НАНЕСЕНИЕ УРОНА ИГРОКУ
        self.trigger_death_particles = death_particles  # КАДРЫ СМЕРТИ ВРАГА
        # =============================
        # ТАЙМЕР БЕССМЕРТИЯ
        self.vulnerable = True  # МОЖЕТ ЛИ ВРАГ ПОЛУЧАТЬ УРОН
        self.hit_time = None  # МОМЕНТ ВРЕМЕНИ, В КОТОРЫЙ ВРАГ ПОЛУЧИЛ УРОН
        self.invincibility_duration = 200  # ДЛИТЕЛЬНОСТЬ НЕУЯЗВИМОСТИ ВРАГА ПОСЛЕ ПОЛУЧЕНИЯ УРОНА
        # =============================
        load_enemies_sounds(self)  # ЗАГРУЗКА ЗВУКОВ МОНСТРОВ
        # =============================

    # -----------------------------------------------------------------------------------------------------------------
    def import_graphics(self, name: str) -> None:
        """
        Функция подгрузки графики врага
        :param name: имя монстра
        """
        self.animations = {"idle": [], "move": [], "attack": []}  # СЛОВАРЬ С АНИМАЦИИ ВРАГА ПО ЕГО ДЕЙСТВИЮ

        main_path = F"data/images/sprites/monsters/{name}/"  # ПУТЬ ДО ПАПКИ С ДАННЫМИ О МОНСТРЕ
        for animation in self.animations.keys():  # ЗАПОЛНЕНИЯ СЛОВАРЯ self.animations
            full_path = main_path + animation
            self.animations[animation] = pygame.image.load(F"{full_path}/{animation}.png").convert_alpha()

    # -----------------------------------------------------------------------------------------------------------------
    def get_player_distance_direction(self, player) -> tuple:
        """
        Метод, расчитывающий дистанциую от игрока и возвращающий эту дистанцию вместе с вектором движения, на
        который должен двигаться враг, чтобы добраться до игрока
        :param player: объект игрока
        """
        enemy_vector = pygame.math.Vector2(self.rect.center)  # ВЕКТОР ДВИЖЕНИЯ ВРАГА
        player_vector = pygame.math.Vector2(player.rect.center)  # ВЕКТОР ДВИЖЕНИЯ ИГРОКА

        distance = (player_vector - enemy_vector).magnitude()  # ПОЛУЧЕНИЕ ДЛИНЫ ВЕКТОРА МЕЖДУ ИГРОКОМ И ВРАГОМ

        if distance > 0:  # ЕСЛИ ВЕКТОР СУЩЕСТВУЕТ (его длина ненулевая)
            direction = (player_vector - enemy_vector).normalize()  # ПРОИЗВОДИТСЯ ЕГО ОБЯЗАТЕЛЬНАЯ НОРМАЛИЗАЦИЯ
        else:  # ИНАЧЕ
            direction = pygame.math.Vector2(0, 0)  # ВЕКТОР НУЛЕВОЙ

        return distance, direction

    # -----------------------------------------------------------------------------------------------------------------
    def get_status(self, player) -> None:
        """
        Метод, определяющий тип поведения врага
        :param player: объект игрока
        """
        distance = self.get_player_distance_direction(player)[0]  # ДИСТАНЦИЯ МЕЖДУ ИГРОКОМ И ВРАГОМ

        if distance <= self.attack_radius and self.can_attack:  # ЕСЛИ ДИСТАНЦИЯ ДОСТАТОЧНА ДЛЯ АТАКИ
            if self.status != "attack":  # ЕСЛИ ВРАГ НЕ АТАКОВАЛ
                self.frame_index = 0  # СТАВИТСЯ ПЕРВЫЙ КАДР (для обновления покадровой анимации)
            self.status = "attack"  # СТАТУС ВРАГА ЯВЛЯЕТСЯ АТАКОЙ
        elif distance <= self.notice_radius:  # ЕСЛИ ДИСТАНЦИЯ ДОСТАТОЧНА ДЛЯ ОБНАРУЖЕНИЯ
            self.status = "move"  # ВРАГ СЛЕДУЕТ ЗА ИГРОКОМ
        else:  # ИНАЧЕ
            self.status = "idle"  # ВРАГ СТОИТ

    # -----------------------------------------------------------------------------------------------------------------
    def actions(self, player) -> None:
        """
        Метод, реализующий действия врагов
        :param player: объект игрока
        """
        if self.status == "attack":  # ЕСЛИ СТАТУС ВРАГА - АТАКА
            self.attack_time = pygame.time.get_ticks()  # ПОЛУЧАЕМ ВРЕМЯ В МОМЕНТ АТАКИ
            self.damage_player(self.attack_damage, self.attack_type)  # НАНОСИМ УРОН ИГРОКУ
        elif self.status == "move":  # ЕСЛИ СТАТУС ВРАГА - ДВИЖЕНИЕ
            self.direction = self.get_player_distance_direction(player)[1]  # ПОЛУЧАЕМ ВЕКТОР ДВИЖ. К ИГРОКУ
        else:  # ИНАЧЕ
            self.direction = pygame.math.Vector2()  # ВЕКТОР НУЛЕВОЙ (игрок стоит, self.status == "idle")

    # -----------------------------------------------------------------------------------------------------------------
    def animate(self) -> None:
        """Функция анмации врагов"""
        animation = self.animations[self.status]  # НАБОР С АНИМАЦИИ ДЛЯ ТЕКУЩЕГО ВРАГА
        self.frame_index += self.animation_speed  # ПРИБАВЛЯЕМ НЕКОТОРОЕ ЗНАЧЕНИЕ К ПОКАДРОВОЙ АНИМАЦИИ

        if self.monster_name == "Eye" or self.monster_name == "Spirit":  # ЕСЛИ ВРАГ - ГЛАЗ ИЛИ ЛЕТУЧАЯ ДУША:
            if self.frame_index >= animation.height / 48:  # ЕСЛИ ЦИКЛ АНИМАЦИИ ТЕКУЩЕГО ДЕЙСТВИЯ ЗАВЕРШЕН
                if self.status == "attack":  # ЕСЛИ ВРАГ АТАКОВАЛ
                    self.can_attack = False  # ВРАГ АТАКОВАТЬ БОЛЬШЕ НЕ МОЖЕТ
                self.frame_index = 0  # ПОКАДРОВАЯ АНИМАЦИЯ НАЧИНАЕТСЯ С НУЛЕВОГО КАДРА

            self.image = animation.subsurface((0, int(self.frame_index) * 48 + 1, 48, 47))  # ПОЛУЧЕНИЕ НУЖНОГО КАДРА
            self.rect = self.image.get_rect(center=self.hitbox.center)  # ПОЛУЧЕНИЕ РАСПОЛОЖЕНИЯ ТЕКУЩЕГО КАДРА

        if self.monster_name == "Owl" or self.monster_name == "Flam":
            if self.frame_index >= animation.height / 64:  # ЕСЛИ ЦИКЛ АНИМАЦИИ ТЕКУЩЕГО ДЕЙСТВИЯ ЗАВЕРШЕН
                if self.status == "attack":  # ЕСЛИ ВРАГ АТАКОВАЛ
                    self.can_attack = False  # ВРАГ АТАКОВАТЬ БОЛЬШЕ НЕ МОЖЕТ
                self.frame_index = 0  # ПОКАДРОВАЯ АНИМАЦИЯ НАЧИНАЕТСЯ С НУЛЕВОГО КАДРА

            self.image = animation.subsurface((0, int(self.frame_index) * 64 + 2, 64, 62))  # ПОЛУЧЕНИЕ НУЖНОГО КАДРА
            self.rect = self.image.get_rect(center=self.hitbox.center)  # ПОЛУЧЕНИЕ РАСПОЛОЖЕНИЯ ТЕКУЩЕГО КАДРА

        if self.monster_name == "Bamboo":  # ЕСЛИ ВРАГ - БОСС-БАМБУК
            if self.frame_index >= animation.width / 186:  # ЕСЛИ ЦИКЛ АНИМАЦИИ ТЕКУЩЕГО ДЕЙСТВИЯ ЗАВЕРШЕН
                if self.status == "attack":  # ЕСЛИ ВРАГ АТАКОВАЛ
                    self.can_attack = False  # ВРАГ АТАКОВАТЬ БОЛЬШЕ НЕ МОЖЕТ
                self.frame_index = 0   # ПОКАДРОВАЯ АНИМАЦИЯ НАЧИНАЕТСЯ С НУЛЕВОГО КАДРА

            self.image = animation.subsurface((int(self.frame_index) * 186, 0, 186, 186))  # ПОЛУЧЕНИЕ НУЖНОГО КАДРА

            self.rect = self.image.get_rect(center=self.hitbox.center)  # ПОЛУЧЕНИЕ РАСПОЛОЖЕНИЯ ТЕКУЩЕГО КАДРА

        if not self.vulnerable:  # ЕСЛИ ВРАГ НЕУЯЗВИМ
            alpha = self.wave_value()  # ПОЛУЧАЕМ ЗНАЧЕНИЕ ПРОЗРАЧНОСТИ ЕГО СПРАЙТА В СООТВЕТСВИИ С СИНУСОИДОЙ
            self.image.set_alpha(alpha)  # УСТАНАВЛИВАЕМ НУЖНОЕ ЗНАЧЕНИЕ ПРОЗРАЧНОСТИ
        else:  # ИНАЧЕ
            self.image.set_alpha(255)  # СПРАЙТ ВРАГА НЕ ПРОЗРАЧЕН

    # -----------------------------------------------------------------------------------------------------------------
    def cooldowns(self) -> None:
        """Метод, обрабатывающий перезарядки врагов"""
        current_time = pygame.time.get_ticks()  # ТЕКУЩИЙ МОМЕНТ ВРЕМЕНИ

        if not self.can_attack:  # ЕСЛИ ВРАГ НЕ МОЖЕТ АТАКОВАТЬ
            if current_time - self.attack_time >= self.attack_cooldown:  # ЕСЛИ ВРЕМЯ ПЕРЕЗАРЯДКИ УДАРА ПРОШЛО
                self.can_attack = True  # ВРАГ МОЖЕТ АТАКОВАТЬ

        if not self.vulnerable:  # ЕСЛИ ВРАГ НЕУЯЗВИМ
            if current_time - self.hit_time >= self.invincibility_duration:  # ЕСЛИ ВРЕМЯ НЕУЯЗВИМОСТИ ПРОШЛО
                self.vulnerable = True  # ВРАГ УЯЗВИМ

    # -----------------------------------------------------------------------------------------------------------------
    def get_damage(self, player, attack_type) -> None:
        """
        Метод, обрабатывающий урон по врагу
        :param player: объект игрока
        :param attack_type: тип атаки по врагу
        """
        if self.vulnerable:  # ЕСЛИ ВРАГ УЯЗВИМ
            self.direction = self.get_player_distance_direction(player)[1]  # ПОЛУЧАЕМ НАПРАВЛЕНИЕ ДВИЖЕНИЯ ВРАГА
            if attack_type == "Weapon":  # ЕСЛИ УДАРИЛИ ОРУЖИЕМ
                self.health -= player.get_full_weapon_damage()  # ОТНИМАЕМ ПОЛНЫЙ УРОН ОТ ОРУЖИЯ ПО ВРАГУ
            else:
                if self.monster_name in ["Flam", "Owl"]:  # МАГИЧЕСКИЙ УРОН (урон от огня) НЕ ПРОХОДИТ ПО ОГОНЬКУ И СОВЕ
                    return
                self.health -= player.get_full_magic_damage()  # ОТНИМАЕМ ЗДОРОВЬЕ У ВРАГА НА ПОЛНЫЙ МАГ. УРОНА ИГРОКА
            self.hit_counter += 1
            self.hit_time = pygame.time.get_ticks()  # ВРЕМЯ, В КОТОРОЕ ВРАГА АТКОВАЛИ
            self.vulnerable = False  # ВРАГ СТАНОВИТСЯ НЕУЯЗВИМ НА НЕКОТОРОЕ ВРЕМЯ
            self.hit_sound.play()  # ПРОИГРЫВАНИЕ ЗВУКА ПОЛУЧЕНИЯ УРОНА

    # -----------------------------------------------------------------------------------------------------------------
    def check_death(self, player) -> None:
        """
        Метод, проверяющий жив ли враг
        :param player: объект игрока
        """
        if self.health <= 0:  # ЕСЛИ ХП ВРАГА МЕНЬШЕ 0
            self.trigger_death_particles(self.rect.center)  # АНИМАЦИЯ СМЕРТИ ВРАГА
            self.kill()  # ВРАГ УМИРАЕТ (его спрайт, а соответсвенно и объект уничтожается)
            player.kill_counter += 1  # КОЛИЧЕСТВО ПОБЕЖДЕННЫХ ВРАГОВ СТАНОВИТСЯ БОЛЬШИМ НА ЕДЕНИЦУ

            if player.kill_counter == 39:  # ЕСЛИ ИГРОК УНИЧТОЖИЛ ВСЕХ ВРАГОВ
                player.is_player_win = True  # ПОБЕДИЛ ИГРОК

            self.death_sound.play()  # ПРОИГРЫВАНИЕ ЗВУКА СМЕРТИ ВРАГА

    # -----------------------------------------------------------------------------------------------------------------
    def hit_reaction(self) -> None:
        """Метод, обрабатывающий реакцию врага на удар"""
        if not self.vulnerable:  # ЕСЛИ ВРАГ НЕУЯЗВИМ
            self.direction *= -self.resistance  # ВРАГ ДВИГАЕТСЯ НАЗАД НА НЕКОТОРОЕ РАССТОЯНИЕ НЕКОТОРОЕ ВРЕМЯ

    # -----------------------------------------------------------------------------------------------------------------

    def hp_reaction(self) -> None:
        """Метод, обрабатывающий количество очков здоровья у врагов"""
        if self.monster_name == "Bamboo":  # ОБРАБОТКА ХП У БОССА
            if not self.is_awaken and self.health < 300:  # ЕСЛИ ХП БОССА МЕНЬШЕ 300 И БОСС ЕЩЁ НЕ ПРОБУЖДЁН
                self.speed = 4  # СКОРОСТЬ БОССА УВЕЛИЧИВАЕТСЯ С 3 ДО 4
                self.damage = 30  # УРОН БОССА УВЕЛИЧИВАЕТСЯ С 25 ДО 30
                self.is_awaken = True  # РЕЖИМ ПРОБУЖДЕНИЯ ВКЛЮЧАЕТСЯ (теперь босс проходит сквозь препятствия)
                self.boss_awaken_sound.play()  # ИГРАЕТ ЗВУК ПРОБУЖДЕНИЯ ГЛАЗА КТУХЛУ ИЗ ТЕРРАРИИ
                self.import_graphics("Bamboo_awaken")  # ЗАГРУЖАЮТСЯ НОВЫЕ СПРАЙТЫ АНИМАЦИИ БОССА

    # -----------------------------------------------------------------------------------------------------------------

    def hit_process(self, player) -> None:
        """Метод, обрабатывающий количество полученных ударов врагом"""
        if self.monster_name in ["Owl", "Flam"]:
            # ОБРАБОТКА ДЛЯ СОВЫ И ОГОНЬКА(каждый третий удар сова и огонёк появляется за спиной игрока)
            if self.hit_counter != 0 and self.hit_counter % 3 == 0:  # КАЖДЫЙ ТРЕТИЙ УДАР
                self.hit_counter = 0  # ОБНУЛЕНИЕ КОЛИЧЕСТВА ПРИНЯТЫХ УДАРОВ ВРАГОМ
                direction = player.status.split("_")[0]  # НАПРАВЛЕНИЕ ДВИЖЕНИЯ ИГРОКА
                poses = {"down": (0, -115), "up": (0, 115), "left": (115, 0), "right": (-115, 0)}
                new_pos = poses[direction]  # НОВАЯ ПОЗИЦИЯ ВРАГА
                x, y = int(player.rect.x), int(player.rect.y)  # ПОЗИЦИЯ ИГРОКА

                # ПЕРЕМЕЩЕНИЕ ХИТБОКСА ВРАГА ЗА СПИНУ ИГРОКА
                self.hitbox.x = x + new_pos[0]
                self.hitbox.y = y + new_pos[1]

                # ЗАМЕНА РАМКИ В КОТОРОЙ НАХОДИТСЯ МОНСТР НА ЕГО ХИТБОКС
                self.rect.center = self.hitbox.center

                self.owl_step_sound.play()  # ЗВУК ПЕРЕМЕЩЕНИЯ СОВЫ

    # -----------------------------------------------------------------------------------------------------------------

    def check_awaken(self, player) -> None:
        """
        Метод, осуществляющий проверку того, находится ли враг в пробуждённом состоянии и записывающий результат в атри-
        буты врага
        :param player: объект игрока
        """
        if self.is_awaken and not player.is_boss_awaken:
            player.is_boss_awaken = True

    # -----------------------------------------------------------------------------------------------------------------

    def update(self) -> None:
        """Метод, обновляющий врага как объект"""
        self.hit_reaction()  # РЕАКЦИЯ ВРАГА НА УДАР
        self.hp_reaction()  # РЕАКЦИЯ НА КОЛИЧЕСТВО ЗДОРОВЬЯ У ВРАГОВ
        self.move(self.speed, is_god=self.monster_name in ["Spirit", "Flam", "Owl"] or self.is_awaken)  # ДВИЖЕНИЕ ВРАГА
        self.animate()  # АНИМАЦИЯ ВРАГА
        self.cooldowns()  # ПЕРЕЗАРЯДКИ ВРАГА

    # -----------------------------------------------------------------------------------------------------------------

    def enemy_update(self, player) -> None:
        """
        Метод обновляющий врага относительно игрока
        :param player: объект игрока
        """
        self.get_status(player)  # ПОЛУЧЕНИЯ СТАТУСА ДЕЙСТВИЯ ВРАГА
        self.actions(player)  # ОБРАБОТКА СТАТУСА ДЕЙСТВИЯ ВРАГА
        self.check_death(player)  # ПРОВЕРКА СМЕРТИ ВРАГА
        self.hit_process(player)  # ОБРАБОТКА СОБЫТИЙ КАСАЮЩИХСЯ КОЛИЧЕСТВА ПОЛУЧЕННЫХ УДАРОВ ВРАГОМ
        self.check_awaken(player)  # ПРОВЕРКА НА ПРОБУЖДЕНИЕ

    # -----------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------
