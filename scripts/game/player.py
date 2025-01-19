import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites, passable_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('../../data/images/spriites/main_hero/Idle.png').convert_alpha()

        self.image = self.image.subsurface(pygame.Rect(0, 0, 16, 16))
        self.image = pygame.transform.scale(self.image, (50, 50))

        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -6)  #  Фича для уменьшения хитбокса (может войдет в финальную версию программы)

        self.direction = pygame.math.Vector2()
        self.speed = 5

        self.obstacle_sprites = obstacle_sprites
        self.pass_sprites = passable_sprites

        self.sprite_type = "None"
        self.sprite_id = -1

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

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

    def update(self):
        self.input()
        self.move(self.speed)

