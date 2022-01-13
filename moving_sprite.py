import pygame
from moving_platform import Moving_platform

class Moving_sprite(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, image: pygame.Surface, resize: int, tiles: list, tile_factor: int,
                 sprite_elements: list[pygame.sprite.Group], sprite_groups: list[pygame.sprite.Group]) -> None:
        super().__init__()
        self.add(sprite_group for sprite_group in sprite_groups)
        self.sprite_elements = sprite_elements
        self.tiles = tiles
        self.tile_factor = tile_factor
        self.pos = pos
        self.image = pygame.transform.scale(image, (resize, resize))
        self.images = {True: self.image, False: pygame.transform.flip(self.image, True, False)}
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos.x, pos.y
        self.speed = pygame.Vector2(0, 0)
        self.gravity, self.friction = 0.5, -0.18
        self.is_jumping = False
        self.max_speed = 10
        self.mask = pygame.mask.from_surface(self.image)
        self.flip_mask = 0
        self.masks = {True: self.mask, False: pygame.mask.from_surface(pygame.transform.flip(self.image, True, False))}
        self.tile = pygame.mask.Mask((tile_factor, tile_factor), fill=True)
        self.on_platform = False
        self.was_on_platform = 0

    def collide_with_mask(self, mask, pos_mask):
        return self.mask.overlap_mask(mask, (pos_mask[0]-self.rect. x, pos_mask[1]-self.rect.y))

    def check_collision(self, tiles=True, sprite_groups="normal") -> list[pygame.mask.Mask]:
        if sprite_groups == "normal":
            sprite_groups = self.sprite_elements
        get_hits = []
        # Collision with tiles
        if tiles:
            for row in range(len(self.tiles)):
                for column in range(len(self.tiles[row])):
                    if self.tiles[row][column] != '0':
                        # rect = (column*self.tile_factor, row*self.tile_factor, self.tile_factor, self.tile_factor)
                        # player_rect = (self.pos.x, self.pos.y, self.rect.w, self.rect.h)
                        # if collide_with_rects(rect, player_rect):
                        mask = self.collide_with_mask(self.tile, (column * self.tile_factor, row * self.tile_factor))
                        if mask.count():
                            # rect = (column*self.tile_factor, row*self.tile_factor, self.tile_factor, self.tile_factor)
                            get_hits.append(mask)
        # Collision with elements
        for group in sprite_groups:
            for element in group:
                mask = self.collide_with_mask(element.mask, (element.rect.x, element.rect.y))
                if mask.count():
                    get_hits.append(mask)
                    if element.__class__ == Moving_platform:
                        self.on_platform = element
                        self.was_on_platform = 0
        self.was_on_platform += 1
        if self.was_on_platform > 10:
            self.on_platform = False
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
                    movement = self.find_bits_from_mask(mask, "down")
                    self.pos.y -= movement
                    self.is_jumping = False
                elif self.speed.y < 0:
                    movement = self.find_bits_from_mask(mask, "up")
                    self.pos.y += movement
                self.speed.y = 0
                self.rect.y = round(self.pos.y)

            else:

                if self.speed.x > 0:
                    movement = self.find_bits_from_mask(mask, "right")
                    self.pos.x -= movement
                elif self.speed.x < 0:
                    movement = self.find_bits_from_mask(mask, "left")
                    self.pos.x += movement
                self.speed.x = 0
                self.rect.x = round(self.pos.x)

    def find_bits_from_mask(self, mask: pygame.mask.Mask, direction: str) -> int:
        size = mask.get_size()
        found = False
        for column in range(size[0]):
            continue_finding = False
            for row in range(size[1]):
                coordinate = (column, row)
                if direction == "left":
                    coordinate = (size[0]-1-column, row)
                elif direction == "down":
                    coordinate = (row, column)
                elif direction == "up":
                    coordinate = (row, size[1]-1-column)
                if mask.get_at(coordinate) == 1:
                    if not found:
                        found = column
                    continue_finding = True
            if found and not continue_finding:
                return column-found
        if direction in {"right", "left"}:
            return size[0]-found
        return size[1]-found

    def fall(self, acceleration, dt):
        self.pos.y += 0.5 * (acceleration.y + self.gravity) * (dt ** 2) + self.speed.y * dt
        self.speed.y += (acceleration.y + self.gravity) * dt
        # self.speed.y = limit_speed(self.speed.y, self.max_speed)
        self.rect.y = round(self.pos.y)
        hits = self.check_collision()
        self.collide(hits, True)
        self.rect.y = round(self.pos.y)
