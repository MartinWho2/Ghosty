import pygame
from typing import Union
from map_functions import create_darker_image


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: Union[tuple, list, pygame.Vector2], related: list, size_world: int, lever=False):
        """
        Inits a button
        :param pos: Position of the button with left and bottom coordinates
        :param related: Position of the objects related to the button (platform or door)
        :param size_world: Scale of things (should be 64)
        """
        super().__init__()
        img_size = round(size_world * 3 / 4)
        self.lever = [lever, 0]
        self.images = {}
        if lever:
            image = pygame.image.load("media/lever.png").convert_alpha()
            self.images["player"] = {0: pygame.transform.scale(image.copy(),
                                                               (img_size, img_size)),
                                     1: pygame.transform.flip(pygame.transform.scale(image.copy(),
                                                                                     (img_size, img_size)), True,
                                                              False)}
            self.images["fantom"] = {0: create_darker_image(self.images["player"][0].copy()),
                                     1: create_darker_image(self.images["player"][1].copy())}
            self.image = self.images["player"][0]
        else:
            self.images = {
                "player": pygame.transform.scale(pygame.image.load("tiles/player/button.png").convert_alpha(),
                                                 (img_size, img_size))
                , "fantom": pygame.transform.scale(pygame.image.load("tiles/fantom/button.png").convert_alpha(),
                                                   (img_size, img_size))}
            self.image = self.images["player"]

        self.rect = self.image.get_rect()
        if pos.__class__ != pygame.Vector2:
            self.rect.centerx, self.rect.bottom = pos[0], pos[1]
        else:
            self.rect.centerx, self.rect.bottom = pos.x, pos.y
        self.related = related
        self.mask = pygame.mask.from_surface(self.image)

    def change_image(self, key: str) -> None:
        if self.lever[0]:
            self.image = self.images[key][self.lever[1]]
        else:
            self.image = self.images[key]

    def activate(self, moving_character) -> None:
        if self.lever[0]:
            self.lever[1] = (self.lever[1] + 1) % 2
        self.change_image(moving_character)
        for related in self.related:
            related.activate(moving_character)
