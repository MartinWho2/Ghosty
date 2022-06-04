import pygame
from moving_sprite import Moving_sprite


class Enemy(Moving_sprite):
    def __init__(self, image: pygame.Surface, pos: pygame.Vector2, move_bool: bool, limit: int, tiles: list,
                 tile_factor: int, groups: list[pygame.sprite.Group], elements) -> None:
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
        super().__init__(pos, image, round(tile_factor*1.094), tiles, tile_factor, elements, groups)
        self.move_bool = move_bool
        self.speed = pygame.Vector2(tile_factor/64, 0)
        self.limit = limit
        self.counter = 0.0
        self.speeds = {True: tile_factor/64, False: -tile_factor/64}
        self.heading_right = True
        self.limit_fall = len(self.tiles)*self.tile_factor+300
        self.dead = True

    def move(self, dt):
        if self.move_bool:
            if self.flip_mask:
                self.flip_mask += dt
                if self.flip_mask > 5:
                    self.mask = self.masks[self.heading_right]
                    self.flip_mask = 0
            self.counter += round(abs(self.speed.x * dt), 5)
            hits = self.check_collision(dt)
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
        if self.pos.y > self.limit_fall:
            self.kill()

    def die(self):
        if self.dead:
            self.kill()
        self.dead = True
        self.image = pygame.transform.scale(pygame.image.load("media/enemy-fantome.png").convert_alpha(),
                                            (round(self.image.get_width()*11/14),round(self.image.get_height()*8/7)))
        self.image.set_alpha(150)
        self.images = {True: self.image, False: pygame.transform.flip(self.image, True, False)}
