import pygame


class Text_sprite(pygame.sprite.Sprite):
    def __init__(self, font: str, text: str, size: int, color: tuple[int, int, int],
                 position: tuple[int, int], background=None, shadow=True):
        super().__init__()
        self.font = pygame.font.Font(font, 10)
        text_white = self.font.render(text, False, color, background)
        size -= size % text_white.get_width()
        text_white = pygame.transform.scale(text_white,
                                            (size, round(size / text_white.get_width() * text_white.get_height())))
        if shadow:
            text_black = self.font.render(text, False, (0, 0, 0), background)
            text_black = pygame.transform.scale(text_black,
                                                (size, round(size / text_black.get_width() * text_black.get_height())))
            self.image = pygame.Surface((round(text_black.get_width() + 2), round(text_black.get_height() + 2)),
                                        pygame.SRCALPHA)
            self.image.blit(text_black, (2, 2))
        else:
            self.image = pygame.Surface((text_white.get_width(), text_white.get_height()), pygame.SRCALPHA)
        self.image.blit(text_white, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
