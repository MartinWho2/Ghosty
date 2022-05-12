import pygame
from bullet import Bullet
from map_functions import create_darker_image


class Auto_Tower(pygame.sprite.Sprite):
    def __init__(self, pos, size_world, plan, image: str, size: tuple[int, int], period: int, shoot_height: float,
                 collision_groups: list[pygame.sprite.Group], bullets: pygame.sprite.Group, direction="left"):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (size[0], size[1]))
        self.direction = direction
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)
        self.images = {"player": self.image, "fantom": create_darker_image(self.image.copy())}
        self.mask = pygame.mask.from_surface(self.image)
        self.period = period
        self.now = 0
        self.rect = self.image.get_rect(bottomleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.shoot_height = self.rect.h * shoot_height
        self.collisions = collision_groups
        self.size_world = size_world
        self.map = plan
        self.bullets = bullets
        self.activated = True

    def waiting(self, dt):
        if self.activated:
            self.now += dt
            if self.now > self.period:
                self.shoot()
                self.now = 0

    def shoot(self):
        speed = pygame.Vector2(self.size_world/6.4, 0)
        x_pos = self.rect.right
        if self.direction == "left":
            speed.x = -speed.x
            x_pos = self.rect.left - self.size_world/6.4

        bullet = Bullet(
            pygame.Vector2(x_pos, self.rect.y + self.shoot_height - 5), speed, self.collisions, self.size_world,
            self.map, image="media/bullet.png"
        )
        self.bullets.add(bullet)

    def activate(self, key):
        self.activated = not self.activated

    def change_image(self, moving_character):
        self.image = self.images[moving_character]
        self.mask = pygame.mask.from_surface(self.image)
