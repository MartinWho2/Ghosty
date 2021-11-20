import pygame
from moving_sprite import Moving_sprite


class Enemy(Moving_sprite):
    def __init__(self, image: pygame.Surface, pos: pygame.Vector2, move_bool: bool, limit: int, tiles: list,
                 tile_factor: int, groups: list[pygame.sprite.Group],elements) -> None:
        """
        Init the class
        :param image: Image of the enemy
        :param pos: Position of the enemy
        :param move_bool: Bool to tell if the enemy can move
        :param limit: Limit of movement until he turns around
        :param tiles: The map
        :param tile_factor: The size of the tiles
        :param groups: His sprite group(s)
        """
        super().__init__(pos, image, 70, tiles, tile_factor, elements, groups)
        self.move_bool = move_bool
        self.speed = pygame.Vector2(1, 0)
        self.limit = limit
        self.counter = 0.0
        self.speeds = {True: 1, False: -1}
        self.heading_right = True

    def move(self, dt):
        if self.flip_mask:
            self.flip_mask += dt
            if self.flip_mask > 10:
                self.mask = self.masks[self.heading_right]
                self.flip_mask = 0
        self.counter += round(abs(self.speed.x * dt), 5)
        hits = self.check_collision()
        if self.counter >= self.limit or hits:
            if hits:
                self.collide(hits, False)
            self.heading_right = not self.heading_right
            self.speed.x = self.speeds[self.heading_right]
            self.image = self.images[self.heading_right]
            self.flip_mask = 1
            self.counter = 0.0
        self.pos.x += self.speed.x * dt
        self.rect.x = round(self.pos.x)
        self.fall(pygame.Vector2(0, 0), dt)
        if self.pos.y > 2000:
            self.kill()
