import pygame
# import pygame.camera
import json
import math
from typing import Union

from player import Player
from map_functions import create_map, load_tile_set
from enemy import Enemy
from button import Button
from door import Door
from text_sprites import Text_sprite
from auto_tower import Auto_Tower
from moving_platform import Moving_platform


class Game:
    def __init__(self, window: pygame.Surface) -> None:
        self.game_not_started = True
        self.pause_menu = False

        # Variables related to the menu
        self.timer = 0
        self.title_font = pygame.font.Font("media/fonts/title.TTF", 30)
        self.text_white = self.title_font.render("Press space to start", True, "white")
        self.text_dark = self.title_font.render("Press space to start", True, "black")

        # pygame.camera.init()
        self.window = window
        with open("level_objects.json", "r") as f:
            self.level_objects = json.load(f)
            f.close()
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.level = 1
        self.size_world = 64
        self.surface = pygame.Surface((self.w, self.h))

        self.map = create_map(self.level)
        self.cups = pygame.sprite.Group()
        self.object_sprites = pygame.sprite.Group()
        self.doors_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()

        press_w_text = Text_sprite("media/pixel-font.ttf", "Press SPACE to shoot a bullet", self.size_world * 4,
                                   (255, 255, 255), (256, 550))
        press_q_text = Text_sprite("media/pixel-font.ttf", "Press Q to switch between",
                                   self.size_world * 7, (255, 255, 255), (756, 100))
        press_q_text_2 = Text_sprite("media/pixel-font.ttf", "the player and the ghost",
                                     self.size_world * 5, (255, 255, 255), (766, 130))

        use_arrows_text = Text_sprite("media/pixel-font.ttf", "Use the keys A-D to move left-right",
                                      self.size_world * 5, (255, 255, 255), (406, 0))
        use_space_text = Text_sprite("media/pixel-font.ttf", "Use the key W to jump",
                                     self.size_world * 5, (255, 255, 255), (406, 50))
        open_doors_text = Text_sprite("media/pixel-font.ttf", "Use levers to open or close doors",
                                      self.size_world * 5, (255, 255, 255), (771, 650))
        use_bullets_text = Text_sprite("media/pixel-font.ttf", "Bullets can also activate levers",
                                       self.size_world * 5, (255, 255, 255), (240, 600))
        use_platforms_text = Text_sprite("media/pixel-font.ttf", "Flying platforms are great",
                                         self.size_world * 6, (255, 255, 255), (650, 1050))
        lever_platforms_text = Text_sprite("media/pixel-font.ttf", "Use buttons to activate some platforms",
                                           self.size_world * 7, (255, 255, 255), (1150, 1050))
        be_careful_text = Text_sprite("media/pixel-font.ttf", "Be careful against enemies",
                                      self.size_world * 7, (255, 255, 255), (1500, 100))
        turrets_text = Text_sprite("media/pixel-font.ttf", "Use levers to deactivate turrets",
                                   self.size_world * 7, (255, 255, 255), (1700, 200))
        won_text = Text_sprite("media/pixel-font.ttf", "WELL",
                               self.size_world * 3, (255, 255, 255), (2350, 350))
        won_text_2 = Text_sprite("media/pixel-font.ttf", "DONE",
                                 self.size_world * 3, (255, 255, 255), (2350, 440))
        self.texts.add(press_w_text, press_q_text, press_q_text_2, use_arrows_text,
                       use_space_text, open_doors_text, use_bullets_text, use_platforms_text,
                       lever_platforms_text, be_careful_text, turrets_text, won_text, won_text_2)

        self.player: Player = Player(self.map, self.size_world, self.surface, [self.player_sprite],
                                     [self.doors_sprites, self.platform_sprites, self.towers], [self.enemies],
                                     self.level_objects[str(self.level)]["Spawn"])
        self.camera_pos = pygame.Vector2(self.player.rect.centerx - self.w / 2, self.player.rect.centery - self.h / 2)

        self.can_push_button = False
        self.buttons_pushable = {}
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
        tiles_file = "media/grass-tileset.png"
        tiles_file = "media/dirt-tileset.png"
        self.tiles = {"fantom": load_tile_set(tiles_file, 64, dark=True), "player": load_tile_set(tiles_file, 64)}
        self.bg: dict = {"player": (25, 78, 84), "fantom": (15, 52, 43)}
        self.a_img = pygame.transform.scale(pygame.image.load("media/key_space.png").convert(), (16, 16))
        self.spawn_objects(self.level)
        # self.camera = pygame.camera.Camera(pygame.camera.list_cameras()[0])
        # self.camera.start()
        self.shot = 0

    def menu(self, dt: float) -> None:
        self.timer += dt
        self.timer %= 60
        self.window.fill("dark green")
        self.window.blit(pygame.transform.scale(self.player.image, (256, 256)), (130, 130))
        if self.timer < 40:
            self.window.blit(self.text_dark, (85, 195))
            self.window.blit(self.text_white, (80, 190))

    def change_dt(self, dt: float) -> float:
        """
        Readjusts the value of dt if the game needs to be slowed or accelerated
        :param dt:
        :return:
        """
        if self.shot:
            dt /= 3
            self.shot += dt
            if self.shot > 10:
                self.shot = 0
        return dt

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
        for platform in self.platform_sprites:
            platform.move()
        for bullet in self.bullets:
            bullet.move_and_collide(self.moving_character, dt)
        for person in self.enemies:
            person.move(dt)
        for tower in self.towers:
            tower.waiting(dt)
        fall = True
        if self.moving_character == "fantom":
            fall = False
        self.player.move(self.get_input_for_movement(), self.characters_class[self.moving_character], dt,
                         self.camera_pos, fall=fall)
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
                    self.buttons_pushable[button] = True
                    self.can_push_button = button
                else:
                    self.buttons_pushable[button] = False
        else:
            self.player.fantom_replace(dt, self.camera_pos)
        if self.timer_characters:
            self.change_character(dt)
        self.blit_everything()

    def blit_sprite(self, sprite: pygame.sprite.Sprite):
        self.surface.blit(sprite.image,
                          (sprite.rect.x - round(self.camera_pos.x), sprite.rect.y - round(self.camera_pos.y)))

    def blit_everything(self):
        groups = [self.object_sprites, self.doors_sprites, self.towers, self.enemies,
                  self.bullets, self.texts, self.platform_sprites, self.player_sprite, self.cups]

        # mask_sprite = self.player.mask.to_surface()
        # self.surface.blit(mask_sprite,
        # (self.player.rect.x - round(self.camera_pos.x), self.player.rect.y - round(self.camera_pos.y)))
        for group in groups:
            for sprite in group:
                self.blit_sprite(sprite)
        for item in self.buttons_pushable.items():
            if item[1]:
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

    def get_input_for_movement(self) -> pygame.Vector2:
        value = 0.8
        movement = pygame.Vector2(0, 0)
        if self.keys.get(pygame.K_a):
            movement.x -= value
        if self.keys.get(pygame.K_d):
            movement.x += value
        if self.moving_character == "fantom":
            if self.keys.get(pygame.K_w):
                movement.y -= value
            if self.keys.get(pygame.K_s):
                movement.y += value
        return movement

    def spawn_enemy(self, pos: Union[list, tuple]) -> None:
        """
        Spawns an enemy
        :param pos: Given position of spawn
        """
        move = True
        if pos[-1] == "stay":
            move = False
        Enemy(pygame.image.load("media/enemy.png").convert_alpha(),
              pygame.Vector2(pos[0] * self.size_world, pos[1] * self.size_world),
              move, 100, self.map, self.size_world, [self.enemies],
              [self.doors_sprites, self.object_sprites, self.platform_sprites])

    def spawn_button(self, button_pos: Union[list, tuple], doors: list[Union[Door, Moving_platform, Auto_Tower]],
                     lever=False) -> pygame.sprite:
        pos = [round((button_pos[0] + 0.5) * self.size_world), (button_pos[1] + 1) * self.size_world]
        button = Button(pos, doors, self.size_world, lever=lever)
        button.add(self.object_sprites)
        return button

    def spawn_door(self, door):
        pos = [round((door[0][0] + 0.5) * self.size_world), (door[0][1] + 1) * self.size_world]
        door = Door(door[1], pos, self.moving_character, self.size_world)
        door.add(self.doors_sprites)
        return door

    def spawn_tower(self, pos, orientation, lever):
        pos = [round((pos[0] + 0.5) * self.size_world), (pos[1] + 1) * self.size_world]
        tower = Auto_Tower(pos, self.size_world, self.map, "media/turret.png", (64, 64), 20, 0.5,
                           [self.player_sprite, self.enemies], self.bullets, orientation)
        tower.add(self.towers)
        self.spawn_button(lever, [tower], lever=True)

    def spawn_platforms(self, platform):
        start_pos = ((int(platform[0][0]) + 1) * self.size_world, (int(platform[0][1]) + 1) * self.size_world)
        end_pos = ((int(platform[1][0]) + 1) * self.size_world, (int(platform[1][1]) + 1) * self.size_world)
        platform_sprite = Moving_platform(start_pos, end_pos, self.size_world,
                                          always_moving=True if platform[-1] == "lever" else False)
        self.platform_sprites.add(platform_sprite)
        if platform[-1] == "lever":
            self.spawn_button(platform[-2], [platform_sprite])

    def spawn_cup(self, pos):
        cup = pygame.sprite.Sprite(self.cups)
        size = round(self.size_world / 2)
        cup.image = pygame.transform.scale(pygame.image.load("media/cup.png").convert_alpha(), (size, size))
        cup.rect = cup.image.get_rect()
        cup.rect.topleft = (int(pos[0]) * self.size_world, int(pos[1]) * self.size_world)

    def spawn_objects(self, level: int) -> None:
        objects = self.level_objects[str(level)]
        for pos in objects["Enemies"]:
            self.spawn_enemy(pos)
        for pos in objects["Doors"]:
            button_pos = pos[0]
            doors = pos[1]
            doors_class = []
            for door in doors:
                doors_class.append(self.spawn_door(door))
            self.spawn_button(button_pos, doors_class, lever=True)
        for tower in objects["Towers"]:
            lever_pos = False
            if tower[-1] == "lever":
                lever_pos = tower[-2]
            pos = tower[0]
            orientation = tower[1]
            self.spawn_tower(pos, orientation, lever_pos)
        for platform in objects["Platforms"]:
            self.spawn_platforms(platform)
        self.spawn_cup(objects["Cup"])
        for button in self.object_sprites:
            self.buttons_pushable[button] = False
