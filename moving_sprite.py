import pygame
from map_functions import collide_with_rects


class Moving_sprite(pygame.sprite.Sprite):
    def __init__(self,pos,image,resize,tiles,tile_factor):
        super().__init__()
        self.tiles = tiles
        self.tile_factor = tile_factor
        self.pos = pos
        self.image = pygame.transform.scale(image,(resize,resize))
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = pos.x,pos.y
        self.speed = pygame.Vector2(0,0)
        self.gravity, self.friction = 0.3, -0.2
        self.mask = pygame.mask.from_surface(self.image)

    def check_collision(self):
        get_hits = []
        for row in range(len(self.tiles)):
            for column in range(len(self.tiles[row])):
                if self.tiles[row][column] != '0':
                    rect = (column*self.tile_factor, row*self.tile_factor, self.tile_factor, self.tile_factor)
                    player_rect = (self.pos.x,self.pos.y,self.rect.w,self.rect.h)
                    if collide_with_rects(rect, player_rect):
                        get_hits.append(rect)
        return get_hits

    def collide(self, hits:list, axis:bool):
        for rect in hits:
            if axis:
                if self.speed.y > 0:
                    self.pos.y = rect[1] - self.rect.h
                    self.is_jumping = False
                elif self.speed.y < 0:
                    self.pos.y = rect[1]+rect[3]
                self.speed.y = 0
                self.rect.y = self.pos.y

            else:
                if self.speed.x > 0:
                    self.pos.x = rect[0] - self.rect.w
                elif self.speed.x < 0:
                    self.pos.x = rect[0] + rect[2]
                self.speed.x = 0
                self.rect.x = self.pos.x

    def fall(self,acceleration,dt):
        self.speed.y += (acceleration.y + self.gravity) * dt
        # self.speed.y = limit_speed(self.speed.y,10)
        self.pos.y += self.speed.y * dt
        self.rect.y = round(self.pos.y)
        hits = self.check_collision()
        self.collide(hits, True)
        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)