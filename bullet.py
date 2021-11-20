import pygame
from map_functions import collide_with_rects
from button import Button
from enemy import Enemy
class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, speed: pygame.Vector2, collision_objects: list[pygame.sprite.Group],
                 size_world: int, map: list[list[str]]) -> None:
        super().__init__()
        self.map = map
        self.size_world = size_world
        self.image = pygame.image.load("bullet.png").convert_alpha()
        if speed.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos.x, pos.y
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.colisions_objects = collision_objects

    def move(self, dt):
        self.pos.x += self.speed.x * dt
        self.pos.y += self.speed.y * dt
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        if abs(self.pos.x) > 1000:
            self.kill()

    def collide(self, sprite: pygame.sprite.Sprite):
        if pygame.sprite.collide_mask(self, sprite):
            self.kill()
            return True
        return False

    def move_and_collide(self, moving_character, dt):
        self.move(dt)
        for group in self.colisions_objects:
            for object in group:
                if self.collide(object):
                    if object.__class__ == Button:
                        object.activate(moving_character)
                    elif object.__class__ == Enemy:
                        object.kill()

        for row in range(len(self.map)):
            for column in range(len(self.map[row])):
                tile = self.map[row][column]
                if tile != "0":
                    if collide_with_rects((self.rect.x, self.rect.y, self.rect.w, self.rect.h),
                                          (column * self.size_world, row * self.size_world, self.size_world,
                                           self.size_world)):
                        self.kill()
