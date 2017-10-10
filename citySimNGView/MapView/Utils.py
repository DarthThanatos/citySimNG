"""
    This module contains functions facilitating common operations.
"""

import pygame
from Consts import FONT, FONT_SIZE, GREEN


def draw_text(pos_x, pos_y, msg, color, surface):
    """ Draw text in given location.

    :param pos_x: initial x position
    :param pos_y:  initial y position
    :param msg: text to draw
    :param color: font color
    :param surface: surface on which text should be drawn
    :return: dimensions of text after drawing
    """
    font = pygame.font.SysFont(FONT, FONT_SIZE)
    screen_text = font.render(msg, True, color)
    surface.blit(screen_text, [int(pos_x), int(pos_y)])
    return screen_text.get_size()


def calculate_text_size(msg):
    """ Calculate dimensions of text after drawing.

    :param msg: text for which dimensions will be calculated
    :return: dimensions of text after drawing
    """
    font = pygame.font.SysFont(FONT, FONT_SIZE)
    screen_text = font.render(msg, True, GREEN)
    return screen_text.get_size()


# TODO: better dealing with newlines
def draw_text_with_wrapping(pos_x, pos_y, max_x, msg, color, surface, font_size=FONT_SIZE):
    """ Draw text with wrapping so that it does not exceed given x value.

    :param pos_x: initial x position
    :param pos_y: initial y position
    :param max_x: x value that text should not exceed
    :param msg: text to draw
    :param color: font color
    :param surface: surface on which text should be drawn
    :param font_size: size of font
    """
    widest_line = 0
    font = pygame.font.SysFont(FONT, font_size)
    space_width = font.size(' ')[0]  # get space width
    curr_x, curr_y = pos_x, pos_y
    text_size = (0, 0)

    def _go_to_next_line(curr_x, curr_y, widest_line):
        widest_line = max(curr_x, widest_line)
        curr_x = pos_x  # Reset the x.
        curr_y += word_height  # Start on new row.
        return curr_x, curr_y, widest_line

    for word in msg.split(" "):
        draw_new_line = False
        if len(word) > 0 and word[-1] == '\n':
            word = word[:-1]
            draw_new_line = True
        word_surface = font.render(word, True, color)
        text_size = word_width, word_height = word_surface.get_size()

        if curr_x + word_width >= max_x:
            curr_x, curr_y, widest_line = _go_to_next_line(curr_x, curr_y, widest_line)

        surface.blit(word_surface, (curr_x, curr_y))

        if draw_new_line:
            curr_x, curr_y, widest_line = _go_to_next_line(curr_x + word_width, curr_y, widest_line)
        else:
            curr_x += word_width + space_width

    return curr_y + text_size[1], max(widest_line, curr_x)


def center_image_y_pos(height, y_min, y_max):
    """ Get y value of centered image's top border.

    :param height: image height
    :param y_min: minimal y value
    :param y_max: maximal y value
    :return: y value of centered image's top border
    """
    return (y_min + y_max)/2 - height/2
