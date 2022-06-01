import pygame
import math
import numpy as np


def create_map(level: int) -> list:
    """
    Read a file and create a list corresponding to the map
    :param level: name of the file
    :return carte: map
    """
    filename = f"levels/level{level}.txt"
    # Order is up first and then clockwise
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
                neighbours = get_neighbour_tiles(carte, (row, column))

                temporary_list.append(get_same_neighbours_with_possibilities(neighbours))
            else:
                temporary_list.append(0)
        new_map.append(temporary_list)
    return new_map


def upleft_if_centered(pos_big:tuple[int,int], size_obj:tuple[int,int], size_big:tuple[int,int], rounding=True):
    x = (size_big[0]-size_obj[0]) / 2 - pos_big[0]
    y = (size_big[1] - size_obj[1]) / 2 - pos_big[1]
    if rounding:
        x,y = round(x),round(y)
    return [x, y]


def get_same_neighbours_with_possibilities(neighbours):
    """
    Guess what the tile should be (like corner topleft, center, ...)
    """
    tile_neighbor_possibilities = [(0, 2, 1, 1, 1, 2, 0, 2), (0, 2, 1, 1, 1, 1, 1, 2), (0, 2, 0, 2, 1, 1, 1, 2),
                                   (1, 1, 1, 0, 1, 1, 1, 1), (1, 1, 1, 1, 1, 0, 1, 1), (1, 1, 1, 1, 1, 2, 0, 2),
                                   (1, 1, 1, 1, 1, 1, 1, 1), (1, 2, 0, 2, 1, 1, 1, 1), (1, 0, 1, 1, 1, 1, 1, 1),
                                   (1, 1, 1, 1, 1, 1, 1, 0), (1, 1, 1, 2, 0, 2, 0, 2), (1, 1, 1, 2, 0, 2, 1, 1),
                                   (1, 2, 0, 2, 0, 2, 1, 1)]
    dec_to_hex = {10: "a", 11: "b", 12: "c", 13: "d"}
    for index in range(len(tile_neighbor_possibilities)):
        correct = index + 1
        possibility = tile_neighbor_possibilities[index]
        for i in range(len(possibility)):
            if possibility[i] != 2 and possibility[i] != neighbours[i]:
                correct = False
                break
        if type(correct) == int:
            return correct
    print(f"The tile is not correct. Neighbors : {neighbours}")
    # raise WindowsError
    return 7


def get_neighbour_tiles(matrix: list, index_tile: tuple):
    """
    Gets the neighbours of an element in a matrix
    """
    padded_map = np.pad(matrix, 1, constant_values=0)
    return (int(padded_map[index_tile[0]][index_tile[1] + 1]), int(padded_map[index_tile[0]][index_tile[1] + 2]),
            int(padded_map[index_tile[0] + 1][index_tile[1] + 2]),
            int(padded_map[index_tile[0] + 2][index_tile[1] + 2]),
            int(padded_map[index_tile[0] + 2][index_tile[1] + 1]), int(padded_map[index_tile[0] + 2][index_tile[1]]),
            int(padded_map[index_tile[0] + 1][index_tile[1]]), int(padded_map[index_tile[0]][index_tile[1]]))


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
            if tiles[row][column] != 0:
                rects.append(pygame.rect.Rect(column * factor, row * factor, factor, factor))
    return rects


def collide_with_rects(rect_style_tuple: tuple, rect2: tuple) -> bool:
    if rect2[0] + rect2[2] > rect_style_tuple[0] > rect2[0] - rect_style_tuple[2] and rect2[1] + rect2[3] > \
            rect_style_tuple[1] > rect2[1] - rect_style_tuple[3]:
        return True
    return False


def show_mask(mask: pygame.mask.Mask):
    size = mask.get_size()
    for row in range(size[0]):
        mask_list = []
        for column in range(size[1]):
            mask_list.append(mask.get_at((column, row)))


def check_area_around(pos: [int, int], size: [int, int], tiles: list[list]) -> [[int, int], [int, int]]:
    """
    Gets the area around the position of a moving sprite (f.i. the player or an ennemy) with a given size
    :param pos: Position of object (approximate)
    :param size: Size of object (approximate)
    :param tiles: Matrix of "0" and "1"
    :return: rows and columns
    """
    columns = [pos[0] - size[0],
               pos[0] + size[0]]
    if columns[0] < 0:
        columns[0] = 0  # If too left
    if columns[1] > len(tiles[0]):
        columns[1] = len(tiles[0])  # If too right
    if columns[1] < size[1]:
        columns[1] = size[1]  # If far too left
    rows = [pos[1] - size[1], pos[1] + size[1]]
    if rows[0] < 0:
        rows[0] = 0  # If too up
    if rows[1] > len(tiles):
        rows[1] = len(tiles)  # If too down
    if rows[1] < size[1]:
        rows[1] = size[1]  # If far too up
    return rows, columns


def create_darker_image(image: pygame.Surface):
    """
    Creates a new image for the ghosty world
    :param image: Image to change
    :return:
    """
    new_surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    darker = (20, 25, 60, 130)
    new_surface.fill(darker)
    image.blit(new_surface, (0, 0))
    image.set_colorkey(darker)
    return image


def load_tile_set(filename, final_size, size=16, dark=False):
    """
    Loads a tileset and creates a list of tiles
    :param filename:
    :param final_size:
    :param size:
    :param dark:
    :return:
    """
    tile_set = pygame.image.load(filename).convert_alpha()
    if dark:
        create_darker_image(tile_set)
    if tile_set.get_width() / 5 == tile_set.get_height() / 3 == size:
        tiles = {}
        char_to_hex = {10: "a", 11: "b", 12: "c", 13: "d"}
        for i in range(1, 14):
            tile = pygame.surface.Surface((size, size), pygame.SRCALPHA)
            x, y = (i - 1) % 5 * size, math.floor((i - 1) / 5) * size
            tile.blit(tile_set, (-x, -y))
            tile = pygame.transform.scale(tile, (final_size, final_size))
            tiles[i] = tile
        return tiles
    else:
        print("The tileset is not the correct format")
        raise FileNotFoundError
