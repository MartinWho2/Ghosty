import pygame
from typing import Union


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: Union[tuple, list, pygame.Vector2], door: list, size_world: int):
        """
        Inits a button
        :param pos: Position of the button with left and bottom coordinates
        :param door: Position of the door relative to the button
        :param size_world: Scale of things (should be 64)
        """
        super().__init__()
        img_size = round(size_world * 3 / 4)
        self.images = {
            "player": pygame.transform.scale(pygame.image.load("tiles/player/button.png").convert_alpha(),
                                             (img_size, img_size))
            , "fantom": pygame.transform.scale(pygame.image.load("tiles/fantom/button.png").convert_alpha(),
                                               (img_size, img_size))}
        self.image = self.images["player"]
        self.rect = self.image.get_rect()
        if pos.__class__ != pygame.Vector2:
            self.rect.centerx, self.rect.bottom = pos[0] , pos[1]
        else:
            self.rect.centerx, self.rect.bottom = pos.x, pos.y
        self.door = door
        self.mask = pygame.mask.from_surface(self.image)

    def change_image(self, key: str) -> None:
        self.image = self.images[key]

    def activate(self, moving_character) -> None:
        for door in self.door:
            door.activate(moving_character)
