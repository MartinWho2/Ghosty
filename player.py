import pygame
import random
from particle import Particle
from math_functions import positive, limit_speed
from moving_sprite import Moving_sprite
from bullet import Bullet


class Fantom(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('media/fantome.png').convert_alpha(), (40, 64))
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
        self.max_speed = 5
        self.friction = -0.1
        self.particle_image = pygame.image.load("media/particle.png")
    def die(self):
        # He obviously can't die
        pass


class Player(Moving_sprite):
    def __init__(self, tiles: list, tile_factor: int, surface: pygame.Surface, groups: list[pygame.sprite.Group],
                 elements: list[pygame.sprite.Group], enemies: list[pygame.sprite.Group], spawn:list) -> None:
        super().__init__(pygame.Vector2(0, 0), pygame.image.load('media/chevalier.png').convert_alpha(), tile_factor, tiles,
                         tile_factor, elements, groups)
        self.surface = surface  # A surface to draw the circle appearing when the ghost tries to run away
        self.surface_above = pygame.Surface((surface.get_width(), surface.get_height()), pygame.SRCALPHA)
        self.image_copy = self.image.copy()
        self.empty_image = self.image.copy()
        self.heading_right = True
        self.empty_image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.SPAWN_POS = (round(spawn[0]*self.tile_factor+self.rect.w/2),round(spawn[1]*self.tile_factor+self.rect.h/2))
        self.rect.center = self.SPAWN_POS
        self.facing_right = True
        self.pos = pygame.Vector2(self.rect.x, self.rect.y)
        self.fantom = Fantom()
        self.fantom.add(group for group in groups)
        self.fantom.rect.center = (self.rect.x - self.fantom.rect.w / 2, self.rect.y)
        self.fantom.pos.x, self.fantom.pos.y = self.fantom.rect.x, self.fantom.rect.y
        self.dist_max = 200
        self.max_speed = 10
        self.is_jumping = False
        self.enemies = enemies

    def move(self, acceleration: pygame.Vector2, moving_object: Moving_sprite, dt: float,
             camera_pos: pygame.Vector2) -> None:
        """
        Moves the player or the fantom with a given acceleration
        :param acceleration: Acceleration of the moving object
        :param moving_object: Player or Fantom
        :param dt: Value to compensate a hypothetical FPS loss
        :param camera_pos: position of the camera
        :return: None
        """
        if self.flip_mask:
            self.flip_mask += dt
            if self.flip_mask > 15:
                self.mask = self.masks[self.heading_right]
                self.flip_mask = 0
        if self.on_platform:
            self.pos += self.on_platform.move(get_move=True)
            self.rect.x,self.rect.y = round(self.pos.x),round(self.pos.y)
        self.fall(acceleration, dt)
        acceleration.x += moving_object.speed.x * self.friction
        moving_object.pos.x += 0.5*acceleration.x * (dt**2) + moving_object.speed.x * dt
        moving_object.speed.x += acceleration.x * dt
        moving_object.rect.x = round(moving_object.pos.x)

        if moving_object.__class__ == Player:
            if self.speed.x > 0:
                self.image = self.images[True]
                if not self.flip_mask:
                    self.flip_mask = 1
                self.heading_right = True
            elif self.speed.x < 0:
                self.image = self.images[False]
                if not self.flip_mask:
                    self.flip_mask = 1
                self.heading_right = False

            if self.check_collision(tiles=False,sprite_groups=self.enemies):
                self.die()

            hits = self.check_collision()
            self.collide(hits, False)

            # !!!! THIS IS REALLY BAD BUT I DON'T KNOW HOW ELSE I COULD DO IT
            if self.speed.y > 1.5:
                self.is_jumping = True

        elif moving_object.__class__ == Fantom:
            acceleration.y += moving_object.speed.y * moving_object.friction
            moving_object.speed.y += acceleration.y * dt
            # moving_object.speed.y = limit_speed(moving_object.speed.y, moving_object.max_speed)
            moving_object.pos.y += moving_object.speed.y * dt
            moving_object.rect.y = round(moving_object.pos.y)
            self.calculate_distance(dt, camera_pos)

    def die(self):
        self.rect.center = self.SPAWN_POS
        self.pos.x, self.pos.y = self.rect.x,self.rect.y
        self.speed.x, self.speed.y = 0, 0
        self.fantom.pos.x -= self.fantom.rect.right - self.rect.x
        self.fantom.pos.y -= self.fantom.rect.centery - self.rect.y
        self.fantom.rect.topleft = self.fantom.pos

    def calculate_distance(self, dt: float, camera_pos: pygame.Vector2) -> None:
        """
        Calculates if the ghost is too far away from the player and replaces it
        :param dt: Value to compensate
        :param camera_pos: Position of the camera
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
        pygame.draw.circle(self.surface_above, (120, 120, 120, alpha), pygame.Vector2(self.rect.center) - camera_pos,
                           self.dist_max, 10)
        self.surface.blit(self.surface_above, (0, 0))
        self.spawn_particles(vector, particles_value, dt, camera_pos)
        self.fantom.pos.x = self.pos.x + self.rect.w / 2 + vector.x - self.fantom.rect.w / 2
        self.fantom.pos.y = self.pos.y + self.rect.h / 2 + vector.y - self.fantom.rect.h / 2
        self.fantom.rect.x = round(self.fantom.pos.x)
        self.fantom.rect.y = round(self.fantom.pos.y)

    def spawn_particles(self, vector: pygame.Vector2, particles_value: float, dt: float, camera_pos):
        vector_fantom_player = pygame.Vector2(vector.x * -1, vector.y * -1)
        if self.fantom.particle_counter >= 200:
            self.fantom.particles.append(
                Particle(self.fantom.particle_image, random.randint(round(particles_value / 17),
                                                                    round(particles_value / 13)),
                         (self.fantom.rect.centerx - camera_pos.x + random.randint(-10, 10),
                          self.fantom.rect.centery - camera_pos.y + random.randint(-10, 10)),
                         vector_fantom_player.normalize()))
            self.fantom.particle_counter = 0
        else:
            self.fantom.particle_counter += particles_value / dt

    def fantom_replace(self, dt: float, camera_pos: pygame.Vector2):
        x, y = self.fantom.rect.right - self.rect.x, self.fantom.rect.centery - self.rect.y
        self.fantom.pos.x -= 0.2 * x
        self.fantom.pos.y -= 0.2 * y
        self.fantom.rect.x = round(self.fantom.pos.x)
        self.fantom.rect.y = round(self.fantom.pos.y)
        self.fantom.particle_counter += dt
        if self.fantom.particle_counter > 10:
            self.fantom.particles.append(Particle(self.fantom.particle_image, 5, (
                random.randint(self.fantom.rect.x, self.fantom.rect.right) - camera_pos.x,
                self.fantom.rect.bottom - camera_pos.y), pygame.Vector2(0, 0.5)))
            self.fantom.particle_counter = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.speed.y = -12

    def shoot(self, sprite_groups: list[pygame.sprite.Group], group_collisions: list[pygame.sprite.Group]) -> None:
        """

        :param sprite_groups: Groups to include the bullet
        :param group_collisions: Groups colliding with the bullet
        :return:
        """
        speed = pygame.Vector2(-10, 0)
        x_pos = self.rect.left - 10
        if self.heading_right:
            speed.x = 10
            x_pos = self.rect.right
        pos = pygame.Vector2(x_pos, self.rect.centery)
        bullet = Bullet(pos, pygame.Vector2(speed.x, speed.y), group_collisions, self.tile_factor, self.tiles)
        bullet.add(group for group in sprite_groups)
