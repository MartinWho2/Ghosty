import pygame
from map_functions import collide_with_rects, check_area_around
from button import Button
from enemy import Enemy
from door import Door
from moving_platform import Moving_platform
import player


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, speed: pygame.Vector2, collision_objects: list[pygame.sprite.Group],
                 size_world: int, plan: list[list[str]], image="media/bullet.png") -> None:
        super().__init__()
        self.map = plan
        self.map_size = [len(self.map), len(self.map[0])]
        self.size_world = size_world
        self.image = pygame.image.load(image).convert_alpha()
        if speed.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (round(self.size_world/4.27), round(self.size_world/4.27)))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos.x, pos.y
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)
        self.collisions_objects = collision_objects
        self.approximate_size = [round(self.rect.w / self.size_world) + 2, round(self.rect.h / self.size_world) + 2]

    def move(self, dt):
        self.pos.x += self.speed.x * dt
        self.pos.y += self.speed.y * dt
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        if self.pos.x < -1000 or self.pos.x > 5000:
            self.kill()

    def collide(self, sprite: pygame.sprite.Sprite):
        if pygame.sprite.collide_mask(self, sprite):
            return True
        return False

    def move_and_collide(self, moving_character, dt):
        self.move(dt)
        for group in self.collisions_objects:
            for sprite in group:
                if self.collide(sprite):
                    if sprite.__class__ == Button:
                        sprite: Button
                        sprite.activate(moving_character)
                        self.kill()
                    elif sprite.__class__ == Enemy:
                        sprite: Enemy
                        sprite.die()
                        self.kill()
                    elif sprite.__class__ in {Door, Moving_platform}:
                        sprite: Door
                        self.kill()
                    else:
                        try:
                            sprite: player.Player
                            sprite.die()
                        except:
                            print("The bullet collided with something unknown...")
                            raise WindowsError
        sprite_pos = [round(self.rect.x / self.size_world), round(self.rect.y / self.size_world)]
        rows, columns = check_area_around(sprite_pos, self.approximate_size, self.map_size)
        for row in range(rows[0], rows[1]):
            for column in range(columns[0], columns[1]):
                if self.map[row][column] != 0:
                    if collide_with_rects((self.rect.x, self.rect.y, self.rect.w, self.rect.h),
                                          (column * self.size_world, row * self.size_world, self.size_world,
                                           self.size_world)):
                        self.kill()
