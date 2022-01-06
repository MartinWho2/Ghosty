import pygame


class Text_sprite(pygame.sprite.Sprite):
    def __init__(self, font: str, text: str, size: int, color: tuple[int, int, int],
                 position: tuple[int, int], background=None):
        super().__init__()
        self.font = pygame.font.Font(font, 10)
        self.image = self.font.render(text, False, color, background)
        size -= size % self.image.get_width()
        self.image = pygame.transform.scale(self.image, (size, round(size/self.image.get_width()*self.image.get_height())))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
