import pygame, math, numpy as np


def create_map(level: int) -> list:
    """
    Read a file and create a list corresponding to the map
    :param level: name of the file
    :return carte: map
    """
    filename = f"levels/level{level}.txt"
    # Order is up first and then clockwise
    tile_neigbour = {(0, 0, 1, 1, 1, 0, 0, 0): "1", (0, 0, 1, 1, 1, 1, 1, 0): "2", (0, 0, 0, 0, 1, 1, 1, 0): "3",
                     (1, 1, 1, 0, 1, 1, 1, 1): "4", (1, 1, 1, 1, 1, 0, 1, 1): "5", (1, 1, 1, 1, 1, 0, 0, 0): "6",
                     (1, 1, 1, 1, 1, 1, 1, 1): "7", (1, 0, 0, 0, 1, 1, 1, 1): "8", (1, 0, 1, 1, 1, 1, 1, 1): "9",
                     (1, 1, 1, 1, 1, 1, 1, 0): "a", (1, 1, 1, 0, 0, 0, 0, 0): "b", (1, 1, 1, 0, 0, 0, 1, 1): "c",
                     (1, 0, 0, 0, 0, 0, 1, 1): "d"}
    tile_neigbour_possibilities = [(0, 2, 1, 1, 1, 2, 0, 2),(0, 2, 1, 1, 1, 1, 1, 2),(0, 0, 0, 0, 1, 1, 1, 0),
                                   (1, 1, 1, 0, 1, 1, 1, 1),(1, 1, 1, 1, 1, 0, 1, 1),(1, 1, 1, 1, 1, 2, 0, 2),
                                   (1, 1, 1, 1, 1, 1, 1, 1),(1, 2, 0, 2, 1, 1, 1, 1),(1, 0, 1, 1, 1, 1, 1, 1),
                                   (1, 1, 1, 1, 1, 1, 1, 0),(1, 1, 1, 2, 0, 2, 0, 2),(1, 1, 1, 2, 0, 2, 1, 1),
                                   (1, 2, 0, 2, 0, 2, 1, 1)]
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
    new_map = []
    for row in range(len(carte)):
        temporary_list = []
        for column in range(len(carte[row])):
            if carte[row][column] == "1":
                print(row, column)
                temporary_list.append(tile_neigbour[get_neighbour_tiles(carte,(row,column))])
            else:
                temporary_list.append("0")
        new_map.append(temporary_list)
    return new_map

def get_neighbour_tiles(map:list,index_tile:tuple):
    padded_map = np.pad(map,1,constant_values=0)
    return (int(padded_map[index_tile[0]][index_tile[1]+1]), int(padded_map[index_tile[0]][index_tile[1]+2]),
            int(padded_map[index_tile[0]+1][index_tile[1]+2]), int(padded_map[index_tile[0]+2][index_tile[1]+2]),
            int(padded_map[index_tile[0]+2][index_tile[1]+1]), int(padded_map[index_tile[0]+2][index_tile[1]]),
            int(padded_map[index_tile[0]+1][index_tile[1]]), int(padded_map[index_tile[0]][index_tile[1]]))

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
