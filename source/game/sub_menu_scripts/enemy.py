import pygame

from data.settings import *

from source.game.sub_menu_scripts.entity import Entity


class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.sprite_type = "enemy"
        self.sprite_id = None

        self.import_graphics(monster_name)
        self.status = "idle"
        self.image = (pygame.image.load("data/images/sprites/monsters/Eye/idle/idle.png").
                      subsurface((0, 0, 48, 48)).convert_alpha())

        # движение
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)
        self.obstacle_sprites = obstacle_sprites

        # показатели монстра
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

        # взаимодействие с игроком
        self.can_attack = True

    def import_graphics(self, name):
        self.animations = {"idle": [], "move": [], "attack": []}

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

        if distance <= self.attack_radius and self.can_attack:
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

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed

        if self.monster_name == "Eye":
            if self.frame_index >= animation.height / 48:
                if self.status == "attack":
                    self.can_attack = False
                self.frame_index = 0

            self.image = animation.subsurface((0, int(self.frame_index) * 48, 48, 48))
            self.rect = self.image.get_rect(center=self.hitbox.center)

        if self.monster_name == "Bamboo":
            if self.frame_index >= animation.width / 186:
                if self.status == "attack":
                    self.can_attack = False
                self.frame_index = 0

            self.image = animation.subsurface((int(self.frame_index) * 186, 0, 186, 186))
            self.rect = self.image.get_rect(center=self.hitbox.center)

    def update(self):
        self.move(self.speed)
        self.animate()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)