import pygame
from typing import Union


class Particle:
    def __init__(self, image: pygame.Surface, size: int, pos: Union[pygame.Vector2, tuple[int, int], list[int, int]],
                 speed: Union[pygame.Vector2, tuple[int, int], list[int, int]]):

        if pos.__class__ == pygame.Vector2:
            self.pos = pos
        else:
            self.pos = pygame.Vector2(pos[0], pos[1])

        if speed.__class__ == pygame.Vector2:
            self.speed = speed
        else:
            self.speed = pygame.Vector2(speed[0], speed[1])

        self.image_copy = image.copy()
        self.image = pygame.transform.scale(image, (size, size))
        self.size = size
