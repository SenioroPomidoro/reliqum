import pygame
from data.settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, passable_sprites, create_attack, destroy_attack, create_magic):
        super().__init__(groups)
        self.image = pygame.image.load('../../data/images/spriites/main_hero/down_idle/down_idle.png').convert_alpha()
        self.image = self.image.subsurface(pygame.Rect(0, 0, 50, 50))

        self.obstacle_sprites = obstacle_sprites
        self.sprite_type = "None"
        self.sprite_id = -1

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -6)  # Фича для уменьшения хитбокса

        # графика
        self.import_player_assets()
        self.status = "down"
        self.frame_index = 0
        self.animation_speed = 0.15

        # Ориентация
        self.direction = pygame.math.Vector2()
        self.attacking = False
        self.attack_cooldown = 400
        self.attack_time = None

        # Оружие
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.weapon_index = 0
        self.weapon = list(weapon_data.keys())[self.weapon_index]
        self.can_switch_weapon = True
        self.weapon_switch_time = None

        # Магия
        self.create_magic = create_magic
        self.magic_index = 0
        self.magic = list(magic_data.keys())[self.magic_index]
        self.can_switch_magic = True
        self.magic_switch_time = None

        self.switch_duration_cooldown = 500

        # Показатели персонажа
        # Урон = урон оружия + урон игрока
        self.stats = {"health": 100, "energy": 60, "attack": 10, "magic": 4, "speed": 6}
        self.health = self.stats["health"]
        self.energy = self.stats["energy"]
        self.speed = self.stats["speed"]
        self.exp = 123

    def import_player_assets(self):
        character_path = "../../data/images/spriites/main_hero/"
        self.animations = {"up": [], "down": [], "left": [], "right": [],
                           "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": [],
                           "up_attack": [], "down_attack": [], "left_attack": [], "right_attack": []}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = pygame.image.load(F"{full_path}/{animation}.png").convert_alpha()

    def input(self):
        if self.attacking:
            return

        keys = pygame.key.get_pressed()

        # Движение
        if keys[pygame.K_UP]:
            self.direction.y = -1
            self.status = "up"
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
            self.status = "down"
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
            self.status = "right"
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
            self.status = "left"
        else:
            self.direction.x = 0

        # Атака
        if keys[pygame.K_z]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.create_attack()

        # Магия
        if keys[pygame.K_x]:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()

            style = list(magic_data.keys())[self.magic_index]
            strength = list(magic_data.values())[self.magic_index]["strength"] + self.stats["magic"]
            cost = list(magic_data.values())[self.magic_index]["cost"]

            self.create_magic(style, strength, cost)

        if keys[pygame.K_q] and self.can_switch_weapon:  # СМЕНА ОРУЖИЯ
            self.can_switch_weapon = False
            self.weapon_switch_time = pygame.time.get_ticks()
            if self.weapon_index < len(list(weapon_data.keys())) - 1:
                self.weapon_index += 1  # Смена оружия
            else:
                self.weapon_index = 0
            self.weapon = list(weapon_data.keys())[self.weapon_index]

        if keys[pygame.K_e] and self.can_switch_magic:  # СМЕНА МАГИИ
            self.can_switch_magic = False
            self.magic_switch_time = pygame.time.get_ticks()
            if self.magic_index < len(list(magic_data.keys())) - 1:
                self.magic_index += 1  # Смена оружия
            else:
                self.magic_index = 0
            self.magic = list(magic_data.keys())[self.magic_index]

    def get_status(self):
        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if "idle" not in self.status and not "attack" in self.status:
                self.status = self.status + "_idle"

        if self.attacking:
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

    def collision(self, direction):
        if direction == "horizontal":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:  # движение вправо
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # движения влево
                        self.hitbox.left = sprite.hitbox.right

        if direction == "vertical":
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:  # движение вниз
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # движение вверх
                        self.hitbox.top = sprite.hitbox.bottom

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision("horizontal")

        self.hitbox.y += self.direction.y * speed
        self.collision("vertical")

        self.rect.center = self.hitbox.center

    def cooldowns(self):
        """Функция-таймер для отработки задержек между действиями"""
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False
                self.destroy_attack()

        if not self.can_switch_weapon:
            if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
                self.can_switch_weapon = True

        if not self.can_switch_magic:
            if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
                self.can_switch_magic = True

    def animate(self):
        animation = self.animations[self.status]
        if "idle" not in self.status and "attack" not in self.status:
            loop_count = 4
        else:
            loop_count = 0

        self.frame_index += self.animation_speed
        if self.frame_index >= loop_count:
            self.frame_index = 0

        # изображение
        self.image = animation.subsurface(pygame.Rect((0, int(self.frame_index) * 50 + 1, 50, 49)))
        self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)
