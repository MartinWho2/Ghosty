import pygame
# import pygame.camera
import json
import math
from typing import Union

from player import Player
from map_functions import create_map, load_tile_set, upleft_if_centered as get_corner
from enemy import Enemy
from button import Button
from door import Door
from text_sprites import Text_sprite
from auto_tower import Auto_Tower
from moving_platform import Moving_platform


class Game:
    def __init__(self, window: pygame.Surface) -> None:
        self.shot = None
        self.player = None
        self.camera_pos = None
        self.moving_character = None
        self.characters_class = None
        self.window = window
        with open("level_objects.json", "r") as f:
            self.level_objects = json.load(f)
            f.close()
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.level = 1
        self.size_world = 64
        self.zoom_coeff = 1
        self.can_zoom = True
        self.zoom_max = 2
        self.surface = pygame.Surface((self.w, self.h))

        # Variables related to the menu
        self.timer = 0
        self.title_font = pygame.font.Font("media/fonts/pixel-font.ttf", 40)
        self.text_white = self.title_font.render("Press space to start", True, "white")
        self.text_dark = self.title_font.render("Press space to start", True, "black")
        self.level_box = pygame.transform.scale(pygame.image.load("media/level choose.png").convert(),
                                                (round(self.w / 9),
                                                 round(self.h / 5)))
        self.choose_level_text = self.title_font.render("Select a level", True, "white")
        self.choose_level_text_rect = self.choose_level_text.get_rect(midtop=(round(self.w/2), round(self.h/80)))
        self.level_boxes_rects = []
        for row in range(1):
            for column in range(4):
                self.level_boxes_rects.append(pygame.rect.Rect(round(self.w / 9 + column * self.w / 4.5),
                                                               round(self.h / 5 + row * self.h / 2.5),
                                                               self.level_box.get_width(), self.level_box.get_height()))
        self.level_page = 0
        self.numbers_in_text = []
        self.numbers_in_text_rect = []
        for i in range(10):
            number = pygame.transform.scale(self.title_font.render(str(i), True, "white"),
                                            (round(self.w / 9), round(self.h / 5)))
            self.numbers_in_text.append(number)

        # pygame.camera.init()
        self.map = create_map(self.level)
        self.cup = pygame.sprite.Sprite()
        self.object_sprites = pygame.sprite.Group()
        self.doors_sprites = pygame.sprite.Group()
        self.platform_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.towers = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.texts = pygame.sprite.Group()

        self.can_push_button = False
        self.buttons_pushable = {}
        self.keys: dict = {}
        self.characters = ["player", "fantom"]
        self.load_new_level(self.level)

        self.timer_characters: float = 0.0

        tiles_file = "media/grass-tileset.png"
        tiles_file = "media/dirt-tileset.png"
        self.tiles = {"fantom": load_tile_set(tiles_file, self.size_world, dark=True),
                      "player": load_tile_set(tiles_file, self.size_world)}
        self.bg: dict = {"player": (25, 78, 84), "fantom": (15, 52, 43)}
        self.a_img = pygame.transform.scale(pygame.image.load("media/key_space.png").convert(), (16, 16))

        press_w_text = Text_sprite("media/fonts/pixel-font.ttf", "Press SPACE to shoot a bullet",
                                   round(self.size_world / 6.4),
                                   (255, 255, 255), (4 * self.size_world, 8.6 * self.size_world))
        press_q_text = Text_sprite("media/fonts/pixel-font.ttf", "Press Q to switch between",
                                   round(self.size_world / 6.4), (255, 255, 255),
                                   (11.8 * self.size_world, 1.56 * self.size_world))
        press_q_text_2 = Text_sprite("media/fonts/pixel-font.ttf", "the player and the ghost",
                                     round(self.size_world / 6.4), (255, 255, 255),
                                     (11.9 * self.size_world, 2 * self.size_world))

        use_arrows_text = Text_sprite("media/fonts/pixel-font.ttf", "Use the keys A-D to move left-right",
                                      round(self.size_world / 6.4), (255, 255, 255), (6.34 * self.size_world, 0))
        use_space_text = Text_sprite("media/fonts/pixel-font.ttf", "Use the key W to jump",
                                     round(self.size_world / 6.4), (255, 255, 255),
                                     (6.34 * self.size_world, 0.78 * self.size_world))
        open_doors_text = Text_sprite("media/fonts/pixel-font.ttf", "Use levers to open or close doors",
                                      round(self.size_world / 6.4), (255, 255, 255),
                                      (12.05 * self.size_world, 10.15 * self.size_world))
        use_bullets_text = Text_sprite("media/fonts/pixel-font.ttf", "Bullets can also activate levers",
                                       round(self.size_world / 6.4), (255, 255, 255),
                                       (3.75 * self.size_world, 9.38 * self.size_world))
        use_platforms_text = Text_sprite("media/fonts/pixel-font.ttf", "Flying platforms are great",
                                         round(self.size_world / 6.4), (255, 255, 255),
                                         (10.16 * self.size_world, 16.4 * self.size_world))
        lever_platforms_text = Text_sprite("media/fonts/pixel-font.ttf", "Use buttons to activate some platforms",
                                           round(self.size_world / 6.4), (255, 255, 255),
                                           (17.97 * self.size_world, 16.4 * self.size_world))
        be_careful_text = Text_sprite("media/fonts/pixel-font.ttf", "Be careful against enemies",
                                      round(self.size_world / 6.4), (255, 255, 255),
                                      (23.44 * self.size_world, 1.56 * self.size_world))
        turrets_text = Text_sprite("media/fonts/pixel-font.ttf", "Use levers to deactivate turrets",
                                   round(self.size_world / 6.4), (255, 255, 255),
                                   (26.56 * self.size_world, 3.13 * self.size_world))
        won_text = Text_sprite("media/fonts/pixel-font.ttf", "WELL",
                               round(self.size_world / 6.4), (255, 255, 255),
                               (36.7 * self.size_world, 5.47 * self.size_world))
        won_text_2 = Text_sprite("media/fonts/pixel-font.ttf", "DONE",
                                 round(self.size_world / 6.4), (255, 255, 255),
                                 (36.7 * self.size_world, 6.88 * self.size_world))
        self.texts.add(press_w_text, press_q_text, press_q_text_2, use_arrows_text,
                       use_space_text, open_doors_text, use_bullets_text, use_platforms_text,
                       lever_platforms_text, be_careful_text, turrets_text, won_text, won_text_2)
        self.game_not_started = True
        self.press_start = False
        self.camera_follow_player = True

    def change_dt(self, dt: float) -> float:
        """
        Readjusts the value of dt if the game needs to be slowed or accelerated
        :param dt:
        :return:
        """
        if self.shot:
            dt /= 2
            # self.zoom_coeff += 0.05
            self.shot += dt
            if self.shot > 30:
                self.shot = 0
        return dt

    def update(self, dt: float) -> None:
        """
        update the screen (central method)
        :param dt: difference of time with last frame
        :return:
        """
        # dt = self.change_dt(dt)
        self.surface.fill(self.bg[self.moving_character])
        # self.surface.blit(self.bg_img, (round(-self.camera_pos.x / 2), round(-self.camera_pos.y / 2)))
        # self.surface.blit(self.bg_img,(0,0))
        # self.window.fill((0, 0, 0, 0))
        if self.camera_follow_player:
            scroll = pygame.Vector2(self.player.pos.x + self.player.rect.w / 2 - self.w / 2 - self.camera_pos.x,
                                    self.player.pos.y + self.player.rect.h / 2 - self.h / 2 - self.camera_pos.y)
            scroll /= 20
        else:
            scroll = pygame.Vector2(0, 0)
        self.camera_pos += scroll
        self.draw_map()
        self.deal_with_particles()
        self.player.move(self.get_input_for_movement(), self.characters_class[self.moving_character], dt,
                         self.camera_pos)
        if self.player.rect.colliderect(self.cup.rect):
            try:
                self.load_new_level(self.level + 1)
            except:
                self.game_not_started = True
        for platform in self.platform_sprites:
            platform.move(dt)
        for bullet in self.bullets:
            bullet.move_and_collide(self.moving_character, dt)
        for person in self.enemies:
            person.move(dt)
        for tower in self.towers:
            tower.waiting(dt)
        if self.player.pos.y > self.size_world * 30:
            self.player.die()
            self.load_new_level(self.level, dead=True)
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
                  self.bullets, self.texts, self.platform_sprites, self.player_sprite]

        # mask_sprite = self.player.mask.to_surface()
        # self.surface.blit(mask_sprite,
        # (self.player.rect.x - round(self.camera_pos.x), self.player.rect.y - round(self.camera_pos.y)))
        for group in groups:
            for sprite in group:
                self.blit_sprite(sprite)
        self.blit_sprite(self.cup)
        for item in self.buttons_pushable.items():
            if item[1]:
                self.surface.blit(self.a_img, (self.player.fantom.rect.centerx - self.a_img.get_width() / 2 -
                                               round(self.camera_pos.x),
                                               self.player.fantom.rect.y - 5 - self.a_img.get_height() - round(
                                                   self.camera_pos.y)))
        if self.zoom_coeff == 1:
            self.window.blit(self.surface, (0, 0))
        else:
            new_surf = pygame.Surface((math.ceil(self.w / self.zoom_coeff), math.ceil(self.h / self.zoom_coeff)))
            pos_up_left = [(i - j) / 2 for i, j in zip(new_surf.get_size(), self.surface.get_size())]
            new_surf.blit(self.surface, pos_up_left)
            new_surf = pygame.transform.scale(new_surf, self.surface.get_size())
            self.window.blit(new_surf, (0, 0))

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
                if tile != 0:
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
        value = self.size_world / 80
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
              move, round(self.size_world * 1.56), self.map, self.size_world, [self.enemies],
              [self.doors_sprites, self.object_sprites, self.platform_sprites])

    def spawn_button(self, button_pos: Union[list, tuple], doors: list[Union[Door, Moving_platform, Auto_Tower]],
                     lever=False) -> pygame.sprite:
        pos = [round((button_pos[0] + 0.5) * self.size_world), (button_pos[1] + 1) * self.size_world]
        button = Button(pos, doors, self.size_world, self.player, lever=lever)
        button.add(self.object_sprites)
        return button

    def spawn_door(self, door, activated=True):
        door = Door(door, self.size_world, activated)
        door.add(self.doors_sprites)
        return door

    def spawn_tower(self, pos, orientation, lever):
        pos = [round((pos[0] + 0.5) * self.size_world), (pos[1] + 1) * self.size_world]
        tower = Auto_Tower(pos, self.size_world, self.map, "media/turret.png", (self.size_world, self.size_world), 20,
                           0.5,
                           [self.player_sprite, self.enemies, self.doors_sprites, self.platform_sprites], self.bullets, orientation)
        tower.add(self.towers)
        self.spawn_button(lever, [tower], lever=True)

    def spawn_platforms(self, platform):
        start_pos = (platform[0][0] * self.size_world, platform[0][1] * self.size_world)
        end_pos = (platform[1][0] * self.size_world, platform[1][1] * self.size_world)
        platform_sprite = Moving_platform(start_pos, end_pos, self.size_world,
                                          always_moving=False if platform[-1] == "lever" else True)
        self.platform_sprites.add(platform_sprite)
        if platform[-1] == "lever":
            self.spawn_button(platform[-2], [platform_sprite], lever=True)

    def spawn_cup(self, pos):
        size = round(self.size_world / 2)
        self.cup.image = pygame.transform.scale(pygame.image.load("media/cup.png").convert_alpha(), (size, size))
        self.cup.rect = self.cup.image.get_rect()
        self.cup.rect.topleft = (int(pos[0]) * self.size_world, int(pos[1]) * self.size_world)

    def spawn_objects(self, level: int) -> None:
        objects = self.level_objects[str(level)]
        for pos in objects["Enemies"]:
            self.spawn_enemy(pos)
        for pos in objects["Doors"]:
            button_pos = pos[0]
            doors = pos[1]
            if pos[-1] != doors:
                door = self.spawn_door(doors, activated=False)
            else:
                door = self.spawn_door(doors)
            self.spawn_button(button_pos, [door], lever=True)
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

    def update_pressed_keys(self):
        print("Keys before : ", self.keys)
        pressed = pygame.key.get_pressed()
        for i in range(len(pressed)):
            if pressed[i]:
                self.keys[i] = True
        for key in self.keys.keys():
            print(key, pressed[key])
            self.keys[key] = pressed[key]
        print("Keys after : ", self.keys)

    def menu(self, dt: float) -> None:
        self.timer += dt
        self.timer %= 60
        self.window.fill("black")
        # self.window.blit(pygame.transform.scale(self.player.image, (256, 256)), (130, 130))
        if self.timer < 30:
            # self.window.blit(self.text_dark, get_corner((0,0),self.text_dark.get_size(),(self.w,self.h)))
            self.window.blit(self.text_white, get_corner((0, 0), self.text_white.get_size(), (self.w, self.h)))

    def main_menu(self, dt):
        self.window.fill("black")
        self.window.blit(self.choose_level_text, self.choose_level_text_rect)
        for row in range(1):
            for column in range(4):
                pos = (round(self.w / 9 + column * self.w / 4.5), round(self.h / 5 + row * self.h / 2.5))
                self.window.blit(self.level_box, pos)
                tile_n = 4 * row + column + 1
                self.window.blit(self.numbers_in_text[tile_n], pos)

    def load_new_level(self, level_nb: int, dead=False):
        self.level = level_nb
        self.map = create_map(level_nb)
        self.object_sprites.empty()
        self.doors_sprites.empty()
        self.platform_sprites.empty()
        self.enemies.empty()
        self.bullets.empty()
        self.towers.empty()
        self.player_sprite.empty()
        self.texts.empty()
        self.player: Player = Player(self.map, self.size_world, self.surface, [self.player_sprite],
                                     [self.doors_sprites, self.platform_sprites, self.towers], [self.enemies],
                                     self.level_objects[str(self.level)]["Spawn"])
        self.characters_class: dict = {"player": self.player, "fantom": self.player.fantom}
        self.moving_character = "player"
        self.camera_pos = pygame.Vector2(self.player.rect.centerx - self.w / 2, self.player.rect.centery - self.h / 2)
        self.shot = 0
        self.spawn_objects(self.level)
        if not dead:
            self.press_start = True
