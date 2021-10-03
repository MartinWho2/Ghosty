import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self,pos,speed):
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert_alpha()
        self.image = pygame.transform.scale(self.image,(15,15))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = pos.x,pos.y
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def move(self,dt):
        self.pos.x += self.speed.x * dt
        self.pos.y += self.speed.y * dt
        self.rect.x,self.rect.y = self.pos.x,self.pos.y
