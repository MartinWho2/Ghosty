import pygame
from player import Player
from map_functions import create_map


class Game:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.surface = pygame.Surface((self.window.get_width(), self.window.get_height()))
        self.scroll = [0,0]
        self.map = create_map("map.txt")

        self.player = Player(self.map, 64, self.surface)
        self.sprites = pygame.sprite.Group(self.player, self.player.fantom)

        self.keys = {}
        self.characters = ["player", "fantom"]
        self.characters_class = {"player": self.player, "fantom": self.player.fantom}
        self.moving_character = self.characters[0]
        self.timer_characters = 0.0
        self.tiles = {
            "fantom": {"1": pygame.transform.scale(pygame.image.load("tiles/fantom/up.png").convert(), (64, 64)),
                       "2": pygame.transform.scale(pygame.image.load("tiles/fantom/mid.png").convert(), (64, 64)),
                       "3": pygame.transform.scale(pygame.image.load("tiles/fantom/button.png").convert_alpha(),
                                                   (64, 64))},
            "player": {"1": pygame.transform.scale(pygame.image.load("tiles/player/up.png").convert(), (64, 64)),
                       "2": pygame.transform.scale(pygame.image.load("tiles/player/mid.png").convert(), (64, 64)),
                       "3": pygame.transform.scale(pygame.image.load("tiles/player/button.png").convert_alpha(),
                                                   (64, 64))}
        }
        self.bg = {"player": (25, 78, 84), "fantom": (15, 52, 43)}

    def update(self, dt: float) -> None:
        self.surface.fill(self.bg[self.moving_character])
        self.window.fill((0,0,0,0))
        self.draw_map()
        for index, particle in reversed(list(enumerate(self.player.fantom.particles))):
            particle.size -= 0.1
            if particle.size <= 0:
                self.player.fantom.particles.pop(index)
            else:
                particle.pos.x += particle.speed.x
                particle.pos.y += particle.speed.y
                size = round(particle.size)
                particle.image = pygame.transform.scale(particle.image_copy, (size, size))
                self.surface.blit(particle.image, particle.pos)
        move = pygame.Vector2(0, 0)
        value = 0.5 * dt

        if self.keys.get(pygame.K_LEFT):
            move.x -= value
        if self.keys.get(pygame.K_RIGHT):
            move.x += value
        if self.moving_character == "fantom":
            if self.keys.get(pygame.K_UP):
                move.y -= value
            if self.keys.get(pygame.K_DOWN):
                move.y += value
        self.player.move(move, self.moving_character, dt)
        if self.moving_character == "fantom":
            self.player.move(pygame.Vector2(0, 0), "player", dt)
        if self.timer_characters:
            self.change_character(dt)
        self.sprites.draw(self.surface)
        if self.moving_character == "player":
            self.player.fantom_replace(dt)
        self.window.blit(self.surface, (0,0))
        
    def change_character(self, dt: float) -> None:
        """
        Makes the selected character blink
        """
        self.timer_characters += dt
        character = self.characters_class[self.moving_character]
        if 0 < self.timer_characters < 10 or 18 < self.timer_characters < 27:
            character.image = character.empty_image
        else:
            character.image = character.image_copy
        if self.timer_characters > 27:
            self.timer_characters = 0

    def draw_map(self) -> None:
        tiles = self.tiles[self.moving_character]
        for row in range(len(self.map)):
            for column in range(len(self.map[row])):
                tile = self.map[row][column]
                if tile != "0":
                    self.surface.blit(tiles[tile], (column * 64, row * 64))
