import pygame
from player import Player
from map_functions import create_map
from ennemy import Ennemy
from bullet import Bullet
class Game:
    def __init__(self, window: pygame.Surface) -> None:
        self.window = window
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.size_world = 64
        self.surface = pygame.Surface((self.w, self.h))

        self.map = create_map("levels/level1.txt")

        self.player = Player(self.map, self.size_world, self.surface)
        self.camera_pos = pygame.Vector2(self.player.rect.centerx-self.w/2,self.player.rect.centery-self.h/2)
        self.sprites = pygame.sprite.Group(self.player, self.player.fantom)
        self.bullets = pygame.sprite.Group()
        self.keys = {}
        self.characters = ["player", "fantom"]
        self.characters_class = {"player": self.player, "fantom": self.player.fantom}
        self.moving_character = self.characters[0]
        self.timer_characters = 0.0
        self.tiles = {
            "fantom": {"1": pygame.transform.scale(pygame.image.load("tiles/fantom/up.png").convert_alpha(), (self.size_world, self.size_world)),
                       "2": pygame.transform.scale(pygame.image.load("tiles/fantom/mid.png").convert(), (self.size_world, self.size_world)),
                       },
            "player": {"1": pygame.transform.scale(pygame.image.load("tiles/player/up.png").convert_alpha(), (self.size_world, self.size_world)),
                       "2": pygame.transform.scale(pygame.image.load("tiles/player/mid.png").convert_alpha(), (self.size_world, self.size_world)),
                       }
        }
        self.bg = {"player": (25, 78, 84), "fantom": (15, 52, 43)}
        counter = 0
        spawns = []
        for row in range(len(self.map)):
            for column in range(len(self.map[row])):
                if self.map[row][column] == '2':
                    counter += 1
                    if counter == 2:
                        spawns.append([row,column])
                        counter = 0
        self.ennemies = pygame.sprite.Group()
        for spawn in spawns:
            ennemy = Ennemy(pygame.image.load("ennemy.png").convert_alpha(),pygame.Vector2(spawn[1]*64,spawn[0]*64),True,100,self.map,64)

            ennemy.add(self.ennemies,self.sprites)

    def update(self, dt: float) -> None:
        self.surface.fill(self.bg[self.moving_character])
        self.window.fill((0,0,0,0))
        scroll = pygame.Vector2(self.player.pos.x+self.player.rect.w/2-self.w/2 - self.camera_pos.x,self.player.pos.y + self.player.rect.h/2-self.h/2-self.camera_pos.y)
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
        for person in self.ennemies:
            person.move(dt)
            for bullet in self.bullets:
                if pygame.sprite.collide_mask(person,bullet):
                    bullet.kill()
                    person.kill()
        move = pygame.Vector2(0, 0)
        value = 0.8 * dt
        if self.keys.get(pygame.K_LEFT):
            move.x -= value
        if self.keys.get(pygame.K_RIGHT):
            move.x += value
        if self.moving_character == "fantom":
            if self.keys.get(pygame.K_UP):
                move.y -= value
            if self.keys.get(pygame.K_DOWN):
                move.y += value
        self.player.move(move, self.moving_character, dt,self.camera_pos)
        if self.moving_character == "fantom":
            self.player.move(pygame.Vector2(0, 0), "player", dt,self.camera_pos)
        if self.timer_characters:
            self.change_character(dt)
        for sprite in self.sprites:
            if sprite.__class__ == Player:
                pass
            self.surface.blit(sprite.image,(sprite.rect.x-round(self.camera_pos.x),sprite.rect.y-round(self.camera_pos.y)))
        if self.moving_character == "player":
            self.player.fantom_replace(dt,self.camera_pos)
        self.window.blit(self.surface, (0,0))
    def shoot(self):
        speed = pygame.Vector2(5,0)
        if speed.x < 0:
            speed.x = -5
        pos = pygame.Vector2(self.player.rect.right,self.player.rect.centery)
        bullet = Bullet(pos,pygame.Vector2(speed.x,speed.y))
        bullet.add(self.bullets,self.sprites)
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
                    self.surface.blit(tiles[tile], (column * self.size_world - self.camera_pos.x, row * self.size_world - self.camera_pos.y))
