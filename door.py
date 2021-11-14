import pygame
from typing import Union


class Door(pygame.sprite.Sprite):
    def __init__(self, image: pygame.surface.Surface, pos: Union[tuple, list], moving_character: str, size_world: int):
        super().__init__()
        self.open = False
        self.img_size = round(size_world / 2)
        self.names = {"top": "door_up", "mid": "door_mid", "bot": "door_up"}
        self.images = {"player": pygame.transform.scale(pygame.image.load(
            f"tiles/player/{self.names[image]}.png").convert_alpha(), (self.img_size, self.img_size)),
                       "fantom": pygame.transform.scale(pygame.image.load(
            f"tiles/fantom/{self.names[image]}.png").convert_alpha(), (self.img_size, self.img_size))}
        self.image = self.images[moving_character]
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.mask = pygame.mask.from_surface(self.image)

    def activate(self):
        self.open = not self.open
        self.kill()

    def change_image(self, moving_character):
        self.image = self.images[moving_character]
