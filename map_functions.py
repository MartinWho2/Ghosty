import pygame


def create_map(filename: str, ) -> list:
    """
    Read a file and create a list corresponding to the map
    :param filename: name of the file
    :return carte: map
    """
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


def collide_with_rects(rect_style_tuple: tuple, rect2: pygame.Rect) -> bool:
    if rect2.x + rect2.w > rect_style_tuple[0] > rect2.x - rect_style_tuple[2] and rect2.y + rect2.h > rect_style_tuple[
        1] > rect2.y - rect_style_tuple[3]:
        return True
    return False
