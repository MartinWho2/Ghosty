import pygame
from typing import Union


class Door(pygame.sprite.Sprite):
    def __init__(self, image: str, pos: Union[tuple, list], moving_character: str, size_world: int):
        super().__init__()
        self.open = False
        self.img_size = round(size_world / 2)
        self.empty_surface = pygame.surface.Surface((self.img_size, self.img_size), pygame.SRCALPHA)
        self.names = {"top": "door_up", "mid": "door_mid", "bot": "door_up"}
        self.images = {"player": {False: pygame.transform.scale(pygame.image.load(
            f"tiles/player/{self.names[image]}.png").convert_alpha(), (self.img_size, self.img_size)),
                                  True: self.empty_surface},
                       "fantom": {False: pygame.transform.scale(pygame.image.load(
                           f"tiles/fantom/{self.names[image]}.png").convert_alpha(), (self.img_size, self.img_size)),
                                  True: self.empty_surface}}
        if image == "bot":
            self.images["player"][False] = pygame.transform.flip(self.images["player"][False], False, True)
            self.images["fantom"][False] = pygame.transform.flip(self.images["fantom"][False], False, True)
        self.image = self.images[moving_character][self.open]
        self.rect = self.image.get_rect()
        self.rect.midbottom = pos
        self.mask = pygame.mask.from_surface(self.image)

    def activate(self, moving_character):
        self.open = not self.open
        self.change_image(moving_character)

    def change_image(self, moving_character):
        self.image = self.images[moving_character][self.open]
        self.mask = pygame.mask.from_surface(self.image)
