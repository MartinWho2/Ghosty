import pygame
from typing import Union


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: Union["centerx","bottom"], door):
        super().__init__()
        self.images = {
            "player": pygame.transform.scale(pygame.image.load("tiles/player/button.png").convert_alpha(), (48, 48))
            , "fantom": pygame.transform.scale(pygame.image.load("tiles/fantom/button.png").convert_alpha(), (48, 48))}
        self.image = self.images["player"]
        self.rect = self.image.get_rect()
        self.rect.centerx,self.rect.bottom = pos[0],pos[1]
        self.door = door

    def activate(self):
        pass
        # self.door.activate()
