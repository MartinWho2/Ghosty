import pygame
from map_functions import collide_with_rects
from math_functions import limit_speed


class Moving_sprite(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, image: pygame.Surface, resize: int, tiles: list, tile_factor: int,
                 sprite_groups: list[pygame.sprite.Group]) -> None:
        super().__init__()
        self.add(sprite_group for sprite_group in sprite_groups)
        self.tiles = tiles
        self.tile_factor = tile_factor
        self.pos = pos
        self.image = pygame.transform.scale(image, (resize, resize))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos.x, pos.y
        self.speed = pygame.Vector2(0, 0)
        self.gravity, self.friction = 0.5, -0.18
        self.max_speed = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.tile = pygame.mask.Mask((tile_factor, tile_factor), fill=True)

    def collide_with_mask(self, mask, pos_mask):
        return self.mask.overlap_mask(mask, (pos_mask[0]-self.rect.x,pos_mask[1]-self.rect.y))

    def check_collision(self):
        get_hits = []
        for row in range(len(self.tiles)):
            for column in range(len(self.tiles[row])):
                if self.tiles[row][column] != '0':

                    # rect = (column*self.tile_factor, row*self.tile_factor, self.tile_factor, self.tile_factor)
                    # player_rect = (self.pos.x, self.pos.y, self.rect.w, self.rect.h)
                    # if collide_with_rects(rect, player_rect):
                    mask = self.collide_with_mask(self.tile, (column * self.tile_factor, row * self.tile_factor))
                    print("Mask overlapping is ",mask)
                    if mask.count():
                        rect = (column*self.tile_factor, row*self.tile_factor, self.tile_factor, self.tile_factor)
                        get_hits.append(mask)
        return get_hits

    def collide(self, hits: list, axis: bool) -> None:
        """
        Deals with detected collision
        :param hits: Masks colliding with the entity
        :param axis: True for y and False for x
        :return : None
        """
        for mask in hits:
            if axis:
                if self.speed.y > 0:
                    movement = self.find_bits_from_mask(mask,"down")
                    self.pos.y -= movement
                    self.is_jumping = False
                elif self.speed.y < 0:
                    movement = self.find_bits_from_mask(mask, "up")
                    self.pos.y += movement
                self.speed.y = 0
                self.rect.y = self.pos.y

            else:
                if self.speed.x > 0:
                    movement = self.find_bits_from_mask(mask, "left")
                    self.pos.x += movement
                elif self.speed.x < 0:
                    movement = self.find_bits_from_mask(mask, "right")
                    self.pos.x -= movement
                self.speed.x = 0
                self.rect.x = self.pos.x

    def find_bits_from_mask(self, mask: pygame.mask.Mask, direction: str) -> int:
        size = mask.get_size()
        for column in range(size[0]):
            found = False
            for row in range(size[1]):
                if direction == "left":
                    coordinate = (column, row)
                elif direction == "right":
                    coordinate= (size[0]-1-column, row)
                elif direction == "up":
                    coordinate = (row, column)
                elif direction == "down":
                    coordinate = (size[1]-1-row, column)
                if mask.get_at(coordinate) == 1:
                    found = True
                    break
            if not found:
                if direction == "right":
                    return column + 1
                return column - 1
        print("ERROR")

    def fall(self, acceleration, dt):
        self.speed.y += (acceleration.y + self.gravity) * dt
        # self.speed.y = limit_speed(self.speed.y, self.max_speed)
        self.pos.y += self.speed.y * dt
        self.rect.y = round(self.pos.y)
        hits = self.check_collision()
        self.collide(hits, True)
        self.rect.x = round(self.pos.x)
        self.rect.y = round(self.pos.y)
