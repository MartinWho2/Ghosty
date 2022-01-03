import pygame
from bullet import Bullet


class Auto_Tower(pygame.sprite.Sprite):
    def __init__(self, pos, size_world, map, image: str, size: tuple[int, int], period: int, shoot_height: float,
                 collision_groups:list[pygame.sprite.Group], bullets:pygame.sprite.Group, direction="left"):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (size[0], size[1]))
        self.direction = direction
        if self.direction == "left":
            pygame.transform.flip(self.image, True, False)
        self.period = period
        self.now = 0
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.shoot_height = self.rect.h * shoot_height
        self.collisions = collision_groups
        self.size_world = size_world
        self.map = map
        self.bullets = bullets

    def waiting(self, dt):
        self.now += dt
        if self.now > self.period:
            self.shoot()
            self.now = 0

    def shoot(self):
        speed = pygame.Vector2(10, 0)
        x_pos = self.rect.right
        if self.direction == "left":
            speed.x = -10
            x_pos = self.rect.left - 10

        bullet = Bullet(
            pygame.Vector2(x_pos, self.rect.y+self.shoot_height-5), speed, self.collisions, self.size_world, self.map, image="bullet.png"
        )
        self.bullets.add(bullet)
