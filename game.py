import pygame
import json
from typing import Union

from player import Player
from map_functions import create_map
from enemy import Enemy


class Game:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        with open("level_objects.json", "r") as f:
            self.level_objects = json.load(f)
            f.close()
        self.w, self.h = self.window.get_width(), self.window.get_height()

        self.size_world = 64
        self.surface = pygame.Surface((self.w, self.h))

        self.map = create_map(1)
        self.sprites = pygame.sprite.Group()

        self.player: Player = Player(self.map, self.size_world, self.surface, self.sprites)
        self.camera_pos = pygame.Vector2(self.player.rect.centerx - self.w / 2, self.player.rect.centery - self.h / 2)

        self.bullets = pygame.sprite.Group()
        self.keys: dict = {}
        self.characters = ["player", "fantom"]
        self.characters_class: dict = {"player": self.player, "fantom": self.player.fantom}
        self.moving_character: str = self.characters[0]
        self.timer_characters: float = 0.0
        self.tiles = {
            "fantom": {"1": pygame.transform.scale(pygame.image.load("tiles/fantom/up.png").convert_alpha(),
                                                   (self.size_world, self.size_world)),
                       "2": pygame.transform.scale(pygame.image.load("tiles/fantom/mid.png").convert(),
                                                   (self.size_world, self.size_world)),
                       },
            "player": {"1": pygame.transform.scale(pygame.image.load("tiles/player/up.png").convert_alpha(),
                                                   (self.size_world, self.size_world)),
                       "2": pygame.transform.scale(pygame.image.load("tiles/player/mid.png").convert_alpha(),
                                                   (self.size_world, self.size_world)),
                       }
        }
        self.bg = {"player": (25, 78, 84), "fantom": (15, 52, 43)}
        self.enemies = pygame.sprite.Group()
        self.spawn_objects(1)

    def update(self, dt: float) -> None:
        """
        update the screen (central method)
        :param dt: difference of time with last frame
        :return:
        """
        self.surface.fill(self.bg[self.moving_character])
        self.window.fill((0, 0, 0, 0))
        scroll = pygame.Vector2(self.player.pos.x + self.player.rect.w / 2 - self.w / 2 - self.camera_pos.x,
                                self.player.pos.y + self.player.rect.h / 2 - self.h / 2 - self.camera_pos.y)
        scroll /= 10
        self.camera_pos += scroll
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
        for bullet in self.bullets:
            bullet.move(dt)
        for person in self.enemies:
            person.move(dt)
            for bullet in self.bullets:
                if pygame.sprite.collide_mask(person, bullet):
                    bullet.kill()
                    person.kill()
        movement = pygame.Vector2(0, 0)
        value = 0.8 * dt
        if self.keys.get(pygame.K_LEFT):
            movement.x -= value
        if self.keys.get(pygame.K_RIGHT):
            movement.x += value
        if self.moving_character == "fantom":
            if self.keys.get(pygame.K_UP):
                movement.y -= value
            if self.keys.get(pygame.K_DOWN):
                movement.y += value

        self.player.move(movement, self.characters_class[self.moving_character], dt, self.camera_pos)
        if self.moving_character == "fantom":
            self.player.move(pygame.Vector2(0, 0), self.characters_class["player"], dt, self.camera_pos)
        if self.timer_characters:
            self.change_character(dt)
        for sprite in self.sprites:
            self.surface.blit(sprite.image,
                              (sprite.rect.x - round(self.camera_pos.x), sprite.rect.y - round(self.camera_pos.y)))
        if self.moving_character == "player":
            self.player.fantom_replace(dt, self.camera_pos)
        self.window.blit(self.surface, (0, 0))

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
                    self.surface.blit(tiles[tile], (
                        column * self.size_world - round(self.camera_pos.x), row * self.size_world -
                        round(self.camera_pos.y)))

    def spawn_enemy(self, pos: Union[list, tuple]) -> None:
        """
        Spawns an enemy
        :param pos: Given position of spawn
        """
        Enemy(pygame.image.load("enemy.png").convert_alpha(),
              pygame.Vector2(pos[0] * self.size_world, pos[1] * self.size_world),
              True, 100, self.map, self.size_world, self.enemies, self.sprites)

    def spawn_objects(self, level: int) -> None:
        objects = self.level_objects[str(level)]
        for pos in objects["Enemies"]:
            self.spawn_enemy(pos)
