import pygame, math


def create_map(level: int) -> list:
    """
    Read a file and create a list corresponding to the map
    :param level: name of the file
    :return carte: map
    """
    filename = f"levels/level{level}.txt"
    with open(filename, "r") as file:
        text = file.read()
        carte = []
        temporary_list = []
        for char in text:
            if char != "\n":
                temporary_list.append(char)
            else:
                carte.append(temporary_list)
                temporary_list = []
        if temporary_list:
            carte.append(temporary_list)
        file.close()

    return carte


def create_rect_map(tiles: list, factor: int) -> list:
    """
    Create a list with rects from the map
    :param tiles: The map in a list
    :param factor: The size of a tile
    :return rects: The list of rects colliding with the player
    """
    rects = []
    for row in range(len(tiles)):
        for column in range(len(tiles[row])):
            if tiles[row][column] != "0":
                rects.append(pygame.rect.Rect(column * factor, row * factor, factor, factor))
    return rects


def collide_with_rects(rect_style_tuple: tuple, rect2: tuple) -> bool:
    if rect2[0] + rect2[2] > rect_style_tuple[0] > rect2[0] - rect_style_tuple[2] and rect2[1] + rect2[3] > rect_style_tuple[
        1] > rect2[1] - rect_style_tuple[3]:
        return True
    return False
def show_mask(mask:pygame.mask.Mask):
    size = mask.get_size()
    for row in range(size[0]):
        list = []
        for column in range(size[1]):
            list.append(mask.get_at((column,row)))

def load_tile_set(filename,final_size,size=16):
    tile_set = pygame.image.load(filename).convert_alpha()
    tile_size = tile_set.get_width()/5
    if tile_set.get_width()/5 == tile_set.get_height()/3 == size:
        tiles = {}
        char_to_hex = {10:"a",11:"b",12:"c",13:"d"}
        for i in range(1,14):
            tile = pygame.surface.Surface((size,size),pygame.SRCALPHA)
            x,y = (i-1)%5*size, math.floor((i-1)/5)*size
            tile.blit(tile_set,(-x,-y))
            tile = pygame.transform.scale(tile,(final_size,final_size))
            if i < 10:
                tiles[str(i)] = tile
            else:
                tiles[char_to_hex[i]] = tile
    return tiles
