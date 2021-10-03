import pygame
from moving_sprite import Moving_sprite

class Ennemy(Moving_sprite):
    def __init__(self, image, pos,move_bool,limit,tiles,tile_factor):
        super().__init__(pos,image,70,tiles,tile_factor)
        self.move_bool = move_bool
        self.speed = pygame.Vector2(1, 0)
        self.limit = limit
        self.counter = 0.0
        self.speeds = {-1:1,1:-1}

    def move(self,dt):
        self.counter += round(abs(self.speed.x * dt), 5)
        if self.counter >= self.limit:
            self.speed.x = self.speeds[self.speed.x]
            self.image = pygame.transform.flip(self.image,True,False)
            self.counter = 0.0
        self.pos.x += self.speed.x * dt
        hits = self.check_collision()
        if hits:
            self.counter = self.limit
            speed_x = self.speed.x
            self.collide(hits,False)
            self.speed.x = speed_x
        self.fall(pygame.Vector2(0,0),dt)



