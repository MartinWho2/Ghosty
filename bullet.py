import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, speed: pygame.Vector2) -> None:
        super().__init__()
        self.image = pygame.image.load("bullet.png").convert_alpha()
        if speed.x < 0:
            self.image = pygame.transform.flip(self.image, True, False)
        self.image = pygame.transform.scale(self.image, (15, 15))
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos.x, pos.y
        self.speed = speed
        self.mask = pygame.mask.from_surface(self.image)

    def move(self, dt):
        self.pos.x += self.speed.x * dt
        self.pos.y += self.speed.y * dt
        self.rect.x, self.rect.y = self.pos.x, self.pos.y
        if abs(self.pos.x) > 1000:
            self.kill()

    def collide(self, sprite: pygame.sprite.Sprite):
        if pygame.sprite.collide_mask(self, sprite):
            self.kill()
            return True
        return False
