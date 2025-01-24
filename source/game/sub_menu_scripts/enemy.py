import pygame

from data.settings import *

from source.game.sub_menu_scripts.entity import Entity


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = "enemy"
        self.sprite_id = None

        self.import_graphics(monster_name)
        self.status = "down"
        self.image = pygame.image.load("data/images/sprites/monsters/Eye/down_idle/down_idle.png").convert_alpha()

        # движение
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # stats
        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.health = monster_info["health"]
        self.exp = monster_info["exp"]
        self.speed = monster_info["speed"]
        self.attack_damage = monster_info["damage"]
        self.resistance = monster_info["resistance"]
        self.attack_radius = monster_info["attack_radius"]
        self.notice_radius = monster_info["notice_radius"]
        self.attack_type = monster_info["attack_type"]

    def import_graphics(self, name):
        self.animations = {"up": [], "down": [], "left": [], "right": [],
                           "up_idle": [], "down_idle": [], "left_idle": [], "right_idle": [],
                           "attack": []}

        main_path = F"data/images/sprites/monsters/{name}/"
        for animation in self.animations.keys():
            full_path = main_path + animation
            self.animations[animation] = pygame.image.load(F"{full_path}/{animation}.png").convert_alpha()

    def get_player_distance_direction(self, player):
        enemy_vector = pygame.math.Vector2(self.rect.center)
        player_vector = pygame.math.Vector2(player.rect.center)

        distance = (player_vector - enemy_vector).magnitude()  # получение длины вектора

        if distance > 0:
            direction = (player_vector - enemy_vector).normalize()
        else:
            direction = pygame.math.Vector2(0, 0)

        return distance, direction

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius:
            self.status = "attack"
        elif distance <= self.notice_radius:
            self.status = "move"
        else:
            self.status = "idle"

    def actions(self, player):
        if self.status == "attack":
            print("attack")
        elif self.status == "move":
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def update(self):
        self.move(self.speed)

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)