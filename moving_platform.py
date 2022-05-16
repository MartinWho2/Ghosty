import pygame
from map_functions import create_darker_image


class Moving_platform(pygame.sprite.Sprite):
    def __init__(self, start_pos: tuple, end_pos: tuple, size_world: int, always_moving=False):
        """
        :param start_pos: Position of start given bottomleft
        :param end_pos: Position of end given bottomleft
        :param size_world: Size of a tile
        :param always_moving: If it needs a lever (true for yes)
        """
        super().__init__()
        self.tile_size = size_world
        image = pygame.image.load("media/platform.png").convert_alpha()
        image = pygame.transform.scale(image, (size_world, round(size_world / image.get_width() * image.get_height())))
        self.images = {"fantom": create_darker_image(image.copy()), "player": image}
        self.image = self.images["player"]
        self.mask = pygame.mask.from_surface(self.image)
        self.pos = pygame.Vector2(start_pos[0], start_pos[1])
        self.rect = self.image.get_rect()
        self.rect.bottomleft = start_pos
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.velocity = size_world/64
        self.always_moving = always_moving
        self.activated = always_moving
        self.heading_to_end = True
        self.moving = pygame.Vector2(0, 0)

    def move(self, dt, get_move=False):
        if self.activated:
            toward = self.end_pos
            if not self.heading_to_end:
                toward = self.start_pos
            self.moving.x, self.moving.y = toward[0] - self.rect.x, toward[1] - self.rect.bottom
            if self.moving.length() <= self.velocity*dt:
                if not get_move:
                    self.rect.bottomleft = toward
                    if not self.always_moving:
                        self.activated = False
                    self.heading_to_end = not self.heading_to_end
            else:
                self.moving.scale_to_length(self.velocity*dt)
                if not get_move:
                    print(f"platform moving : {self.moving.x}",end=", ")
                    self.pos.x += self.moving.x
                    self.pos.y += self.moving.y
                    self.rect.x, self.rect.bottom = round(self.pos.x), round(self.pos.y)
                else:
                    print(f"player moving : {self.moving.x}")
        else:
            self.moving.x, self.moving.y = 0, 0
        if get_move:
            return self.moving

    def activate(self, moving_player):
        self.change_image(moving_player)
        if not self.activated:
            self.activated = True
        else:
            self.heading_to_end = not self.heading_to_end

    def change_image(self, moving_character):
        self.image = self.images[moving_character]
        self.mask = pygame.mask.from_surface(self.image)
