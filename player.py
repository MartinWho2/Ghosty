import pygame
import random
from particle import Particle
from map_functions import create_rect_map, collide_with_rects
from math_functions import positive, limit_speed


class Fantom(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('fantome.png').convert_alpha(), (40, 64))
        self.image.set_alpha(100)
        self.image_copy = self.image.copy()
        self.empty_image = self.image.copy()
        self.empty_image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)
        self.alphas = {"player": 100, "fantom": 200}
        self.particle_counter = 0
        # The reached value gets lower if the fantom goes away
        self.particles = []
        self.speed = pygame.Vector2(0, 0)
        self.friction = -0.1
        self.particle_image = pygame.image.load("particle.png")


class Player(pygame.sprite.Sprite):
    def __init__(self, tiles: list, tile_factor: int, surface: pygame.Surface) -> None:
        super().__init__()
        self.surface = surface
        self.surface_above = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        self.tiles = tiles
        self.tile_factor = tile_factor
        self.image = pygame.transform.scale(pygame.image.load('chevalier.png').convert_alpha(), (64, 64))
        self.image_copy = self.image.copy()
        self.images = {True: self.image, False: pygame.transform.flip(self.image, True, False)}
        self.empty_image = self.image.copy()
        self.empty_image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.rect.center = (100, 100)
        self.facing_right = True
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)
        self.fantom = Fantom()
        self.fantom.rect.center = (self.rect.x - self.fantom.rect.w / 2, self.rect.y)
        self.fantom.pos.x, self.fantom.pos.y = self.fantom.rect.x, self.fantom.rect.y
        self.dist_max = 200
        self.speed = pygame.Vector2(0, 0)
        self.gravity, self.friction = 0.4, -0.2
        self.is_jumping = False

    def move(self, acceleration: pygame.Vector2, moving_object: str, dt: float, camera_pos:pygame.Vector2) -> None:
        """
        Moves the player or the fantom with a given acceleration
        :param acceleration: Acceleration of the moving object
        :param moving_object: Player or Fantom
        :param dt: Value to compensate a hypothetical FPS loss
        :param scroll: Value to scroll
        :return: None
        """
        if moving_object == "player":
            acceleration.x += self.speed.x * self.friction
            # acceleration.y += self.speed.y * self.friction
            self.speed.x += acceleration.x * dt
            self.speed.x = limit_speed(self.speed.x, 10)
            self.pos.x += self.speed.x * dt
            self.rect.x = round(self.pos.x)
            if self.speed.x > 0:
                self.image = self.images[True]
            elif self.speed.x < 0:
                self.image = self.images[False]
            hits = self.check_collision()
            self.collide(hits, 0)

            self.speed.y += (acceleration.y + self.gravity) * dt
            # self.speed.y = limit_speed(self.speed.y,10)
            self.pos.y += self.speed.y * dt
            self.rect.y = round(self.pos.y)
            hits = self.check_collision()
            self.collide(hits, 1)
            self.rect.x = round(self.pos.x)
            self.rect.y = round(self.pos.y)
        else:
            acceleration.x += self.fantom.speed.x * self.fantom.friction
            self.fantom.speed.x += acceleration.x * dt
            if abs(self.fantom.speed.x) > 5:
                if self.fantom.speed.x > 0:
                    self.fantom.speed.x = 5
                else:
                    self.fantom.speed.x = -5
            self.fantom.pos.x += self.fantom.speed.x * dt

            acceleration.y += self.fantom.speed.y * self.fantom.friction
            self.fantom.speed.y += acceleration.y * dt
            if abs(self.fantom.speed.y) > 5:
                if self.fantom.speed.y > 0:
                    self.fantom.speed.y = 5
                else:
                    self.fantom.speed.y = -5
            self.fantom.pos.y += self.fantom.speed.y * dt
            self.fantom.rect.x = int(self.fantom.pos.x)
            self.fantom.rect.y = int(self.fantom.pos.y)
            self.calculate_distance(dt,camera_pos)

    def calculate_distance(self, dt: float, camera_pos:pygame.Vector2) -> None:
        """
        Calculates if the ghost is too far away from the player and replaces it
        :param dt:
        :return:
        """
        vector = pygame.Vector2(self.fantom.pos.x + self.fantom.rect.w / 2 - self.pos.x - self.rect.w / 2,
                                self.fantom.pos.y + self.fantom.rect.h / 2 - self.pos.y - self.rect.h / 2)

        particles_value = vector.length()
        if particles_value > self.dist_max:
            vector.scale_to_length(self.dist_max)
            particles_value = self.dist_max
        alpha = positive(particles_value - 150)
        self.surface_above.fill((0, 0, 0, 0))
        pygame.draw.circle(self.surface_above, (120, 120, 120, alpha), pygame.Vector2(self.rect.center)-camera_pos, self.dist_max, 10)
        self.surface.blit(self.surface_above, (0, 0))
        self.spawn_particles(vector, particles_value, dt, camera_pos)
        self.fantom.pos.x = self.pos.x + self.rect.w / 2 + vector.x - self.fantom.rect.w / 2
        self.fantom.pos.y = self.pos.y + self.rect.h / 2 + vector.y - self.fantom.rect.h / 2
        self.fantom.rect.x = round(self.fantom.pos.x)
        self.fantom.rect.y = round(self.fantom.pos.y)

    def spawn_particles(self, vector: pygame.Vector2, particles_value: float, dt: float,camera_pos):
        vector_fantom_player = pygame.Vector2(vector.x * -1, vector.y * -1)
        if self.fantom.particle_counter >= 200:
            self.fantom.particles.append(
                Particle(self.fantom.particle_image, random.randint(round(particles_value / 17),
                                                                    round(particles_value / 13)),
                         (self.fantom.rect.centerx - camera_pos.x + random.randint(-10, 10),
                          self.fantom.rect.centery - camera_pos.y + random.randint(-10, 10)), vector_fantom_player.normalize()))
            self.fantom.particle_counter = 0
        else:
            self.fantom.particle_counter += particles_value / dt

    def fantom_replace(self, dt: float, camera_pos: pygame.Vector2):
        x, y = self.fantom.rect.right - self.rect.x, self.fantom.rect.centery - self.rect.y
        self.fantom.pos.x -= 0.1 * x
        self.fantom.pos.y -= 0.1 * y
        self.fantom.rect.x = int(self.fantom.pos.x)
        self.fantom.rect.y = int(self.fantom.pos.y)
        self.fantom.particle_counter += dt
        if self.fantom.particle_counter > 10:
            self.fantom.particles.append(Particle(self.fantom.particle_image, 5, (random.randint(self.fantom.rect.x , self.fantom.rect.right)-camera_pos.x, self.fantom.rect.bottom-camera_pos.y),
                                                  pygame.Vector2(0, 0.5)))
            self.fantom.particle_counter = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.speed.y = -10

    def check_collision(self):
        get_hits = []
        for row in range(len(self.tiles)):
            for column in range(len(self.tiles[row])):
                if self.tiles[row][column] != '0':
                    rect = (column*self.tile_factor, row*self.tile_factor, self.tile_factor, self.tile_factor)
                    player_rect = (self.pos.x,self.pos.y,self.rect.w,self.rect.h)
                    if collide_with_rects(rect, player_rect):
                        get_hits.append(rect)
        return get_hits

    def collide(self, hits, axis):
        for rect in hits:
            if axis:
                if self.speed.y > 0:
                    self.pos.y = rect[1] - self.rect.h
                    self.is_jumping = False
                elif self.speed.y < 0:
                    self.pos.y = rect[1]+rect[3]
                self.speed.y = 0
                self.rect.y = self.pos.y

            else:
                if self.speed.x > 0:
                    self.pos.x = rect[0] - self.rect.w
                elif self.speed.x < 0:
                    self.pos.x = rect[0] + rect[2]
                self.speed.x = 0
                self.rect.x = self.pos.x
