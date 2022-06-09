import pygame
from typing import Union
from map_functions import create_darker_image
from math_functions import positive


class Door(pygame.sprite.Sprite):
    def __init__(self, pos_up_and_down: Union[tuple, list], size_world: int, activated:bool):
        super().__init__()
        self.open = False
        self.horizontal = False
        self.img_size = round(size_world / 2)
        self.empty_surface = pygame.surface.Surface((self.img_size, self.img_size), pygame.SRCALPHA)
        self.names = {"top": "door_up", "mid": "door_mid", "bot": "door_up"}
        init_images = {"top": pygame.transform.scale(pygame.image.load(
            f"tiles/player/door_up.png").convert_alpha(), (self.img_size, self.img_size)),
                       "mid": pygame.transform.scale(pygame.image.load(
                           f"tiles/player/door_mid.png").convert_alpha(), (self.img_size, self.img_size)),
                       "bot": pygame.transform.scale(pygame.image.load(
                           f"tiles/player/door_up.png").convert_alpha(), (self.img_size, self.img_size))
                       }
        init_images["bot"] = pygame.transform.flip(init_images["bot"], False, True)
        self.pos_up = pos_up_and_down[0]
        self.pos_down = pos_up_and_down[1]
        if self.pos_up[0] == self.pos_down[0]:
            mids = int(abs(self.pos_up[1] - self.pos_down[1]) * 2 - 1)
            self.image = pygame.surface.Surface((self.img_size, self.img_size * (mids + 2)), pygame.SRCALPHA)
            self.image.blit(init_images["top"], (0, 0))
            for i in range(mids):
                self.image.blit(init_images["mid"], (0, self.img_size * (i + 1)))
            self.image.blit(init_images["bot"], (0, self.img_size * (mids + 1)))
        elif self.pos_up[1] == self.pos_down[1]:
            self.horizontal = True
            mids = int(abs(self.pos_up[0] - self.pos_down[0]) * 2 - 1)
            self.image = pygame.surface.Surface((self.img_size * (mids + 2),self.img_size), pygame.SRCALPHA)
            init_images["top"] = pygame.transform.rotate(init_images["top"],90)
            init_images["mid"] = pygame.transform.rotate(init_images["mid"],90)
            init_images["bot"] = pygame.transform.rotate(init_images["bot"],90)
            self.image.blit(init_images["top"], (0, 0))
            for i in range(mids):
                self.image.blit(init_images["mid"], (self.img_size * (i + 1),0))
            self.image.blit(init_images["bot"],(self.img_size * (mids + 1),0))
        self.images = {"player": {False: self.image.copy(),
                                  True: self.empty_surface},
                       "fantom": {False: create_darker_image(self.image.copy()),
                                  True: self.empty_surface}}
        self.rect = self.image.get_rect()
        self.open = not activated
        self.image = self.images["player"][self.open]
        if self.horizontal:
            self.rect.midleft = (min(self.pos_up[0],self.pos_down[0]) * size_world, self.pos_up[1] * size_world + self.img_size)
        else:
            self.rect.midtop = (self.pos_up[0] * size_world+self.img_size, min(self.pos_down[1],self.pos_up[1]) * size_world)
        self.mask = pygame.mask.from_surface(self.image)



    def activate(self, moving_character, player):
        self.open = not self.open
        self.change_image(moving_character)
        if self.rect.colliderect(player.rect):
            if self.horizontal:
                dist_up = positive(player.rect.centery - self.rect.y)
                dist_down = positive(self.rect.bottom - player.rect.centery)
                if dist_up >= dist_down:
                    player.rect.y = self.rect.bottom + 1
                else:
                    player.rect.bottom = self.rect.y - 1
                player.pos.x, player.pos.y = player.rect.x, player.rect.y
            else:
                dist_left = positive(player.rect.centerx-self.rect.x)
                dist_right = positive(self.rect.right - player.rect.centerx)
                if dist_left >= dist_right:
                    player.rect.x = self.rect.right+1
                else:
                    player.rect.right = self.rect.x-1
                player.pos.x, player.pos.y = player.rect.x, player.rect.y


    def change_image(self, moving_character):
        self.image = self.images[moving_character][self.open]
        self.mask = pygame.mask.from_surface(self.image)
