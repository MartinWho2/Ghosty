import pygame
# import pygame.camera
import json
import math
from typing import Union

from player import Player
from map_functions import create_map, collide_with_rects
from enemy import Enemy
from button import Button
from door import Door
from text_sprites import Text_sprite
from auto_tower import Auto_Tower

class Game:
    def __init__(self, window: pygame.Surface) -> None:
        # pygame.camera.init()
        self.window = window
        with open("level_objects.json", "r") as f:
            self.level_objects = json.load(f)
            f.close()
        self.w, self.h = self.window.get_width(), self.window.get_height()

        self.size_world = 64
        self.surface = pygame.Surface((self.w, self.h))

        self.map = create_map(1)
        self.object_sprites = pygame.sprite.Group()
        self.doors_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()

        self.press_w_text = Text_sprite("pixel-font.ttf", "Press W to shoot a bullet", self.size_world * 4, (0, 0, 0),
                                         (0, 550))
        self.press_q_text = Text_sprite("pixel-font.ttf", "Press Q to switch between the player and the ghost",
                                    self.size_world * 10, (0, 0, 0), (600, 50))
        self.use_arrows_text = Text_sprite("pixel-font.ttf", "Use the arrows left-right to move",
                                    self.size_world * 5, (0, 0, 0), (-150, -100))
        self.use_space_text = Text_sprite("pixel-font.ttf", "Use the space bar to jump",
                                           self.size_world * 5, (0, 0, 0), (-150, 0))
        self.open_doors_text = Text_sprite("pixel-font.ttf", "Use buttons to open or close doors",
                                           self.size_world * 5, (0, 0, 0), (500, 600))
        self.texts.add(self.press_w_text, self.press_q_text, self.use_arrows_text, self.use_space_text, self.open_doors_text)

        self.player: Player = Player(self.map, self.size_world, self.surface, [self.player_sprite],
                                     [self.doors_sprites, self.towers], [self.enemies])
        self.camera_pos = pygame.Vector2(self.player.rect.centerx - self.w / 2, self.player.rect.centery - self.h / 2)

        self.can_push_button = False
        self.keys: dict = {}
        self.characters = ["player", "fantom"]
        self.characters_class: dict = {"player": self.player, "fantom": self.player.fantom}
        self.moving_character: str = self.characters[0]
        self.timer_characters: float = 0.0
        self.tiles: dict = {
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
        self.bg: dict = {"player": (25, 78, 84), "fantom": (15, 52, 43)}
        self.a_img = pygame.transform.scale(pygame.image.load("key_a.png").convert(), (16, 16))
        self.spawn_objects(1)
        # self.camera = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        # self.camera.start()

    def update(self, dt: float) -> None:
        """
        update the screen (central method)
        :param dt: difference of time with last frame
        :return:
        """
        self.surface.fill(self.bg[self.moving_character])
        # self.window.fill((0, 0, 0, 0))
        scroll = pygame.Vector2(self.player.pos.x + self.player.rect.w / 2 - self.w / 2 - self.camera_pos.x,
                                self.player.pos.y + self.player.rect.h / 2 - self.h / 2 - self.camera_pos.y)
        scroll /= 10
        self.camera_pos += scroll
        self.draw_map()
        self.deal_with_particles()
        for bullet in self.bullets:
            bullet.move_and_collide(self.moving_character, dt)
        for person in self.enemies:
            person.move(dt)
        for tower in self.towers:
            tower.waiting(dt)
        self.player.move(self.get_input_for_movement(dt), self.characters_class[self.moving_character], dt,
                         self.camera_pos)
        if self.player.pos.y > 2000:
            # pygame.image.save(self.camera.get_image(), "ITS_YOU.png")
            self.player.die()
            scroll = pygame.Vector2(self.player.pos.x + self.player.rect.w / 2 - self.w / 2 - self.camera_pos.x,
                                    self.player.pos.y + self.player.rect.h / 2 - self.h / 2 - self.camera_pos.y)
            self.camera_pos += scroll
            self.change_character(dt)
        if self.moving_character == "fantom":
            self.player.move(pygame.Vector2(0, 0), self.characters_class["player"], dt, self.camera_pos)
            for button in self.object_sprites:
                ray = pygame.Vector2(self.player.fantom.rect.centerx - button.rect.centerx,
                                     self.player.fantom.rect.centery - button.rect.centery)
                if ray.length() < self.size_world * 0.7:
                    self.can_push_button = button
                else:
                    self.can_push_button = False
        else:
            self.player.fantom_replace(dt, self.camera_pos)
        if self.timer_characters:
            self.change_character(dt)
        self.blit_everything()


    def blit_sprite(self, sprite: pygame.sprite.Sprite):
        self.surface.blit(sprite.image,
                          (sprite.rect.x - round(self.camera_pos.x), sprite.rect.y - round(self.camera_pos.y)))

    def blit_everything(self):
        groups = [self.object_sprites, self.doors_sprites,self.towers, self.enemies, self.bullets, self.texts, self.player_sprite]

        # mask_sprite = self.player.mask.to_surface()
        # self.surface.blit(mask_sprite,
        # (self.player.rect.x - round(self.camera_pos.x), self.player.rect.y - round(self.camera_pos.y)))
        for group in groups:
            for sprite in group:
                self.blit_sprite(sprite)

        if self.can_push_button:
            self.surface.blit(self.a_img, (self.player.fantom.rect.centerx - self.a_img.get_width() / 2 -
                                           round(self.camera_pos.x),
                                           self.player.fantom.rect.y - 5 - self.a_img.get_height() - round(
                                               self.camera_pos.y)))
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

    def deal_with_particles(self):
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

    def get_input_for_movement(self, dt: float) -> pygame.Vector2:
        value = 0.8 * dt
        movement = pygame.Vector2(0, 0)
        if self.keys.get(pygame.K_LEFT):
            movement.x -= value
        if self.keys.get(pygame.K_RIGHT):
            movement.x += value
        if self.moving_character == "fantom":
            if self.keys.get(pygame.K_UP):
                movement.y -= value
            if self.keys.get(pygame.K_DOWN):
                movement.y += value
        return movement

    def spawn_enemy(self, pos: Union[list, tuple]) -> None:
        """
        Spawns an enemy
        :param pos: Given position of spawn
        """
        Enemy(pygame.image.load("enemy.png").convert_alpha(),
              pygame.Vector2(pos[0] * self.size_world, pos[1] * self.size_world),
              True, 100, self.map, self.size_world, [self.enemies], [self.doors_sprites, self.object_sprites])

    def spawn_button(self, button_pos: Union[list, tuple], doors: list[Union[tuple, list]]) -> pygame.sprite:
        pos = [round((button_pos[0] + 0.5) * self.size_world), (button_pos[1] + 1) * self.size_world]
        button = Button(pos, doors, self.size_world)
        button.add(self.object_sprites)
        return button

    def spawn_door(self, door):
        pos = [round((door[0][0] + 0.5) * self.size_world), (door[0][1] + 1) * self.size_world]
        door = Door(door[1], pos, self.moving_character, self.size_world)
        door.add(self.doors_sprites)
        return door

    def spawn_tower(self, pos, orientation):
        pos = [round((pos[0] + 0.5) * self.size_world), (pos[1] + 1) * self.size_world]
        tower = Auto_Tower(pos, self.size_world, self.map, "fantome.png", [64, 64], 10, 0.5, [self.player_sprite, self.enemies], self.bullets, orientation)
        tower.add(self.towers)

    def spawn_objects(self, level: int) -> None:
        objects = self.level_objects[str(level)]
        for pos in objects["Enemies"]:
            self.spawn_enemy(pos)
        for pos in objects["Buttons"]:
            button_pos = pos[0]
            doors = pos[1]
            doors_class = []
            for door in doors:
                doors_class.append(self.spawn_door(door))
            self.spawn_button(button_pos, doors_class)
        for tower in objects["Towers"]:
            pos = tower[0]
            orientation = tower[1]
            self.spawn_tower(pos, orientation)
