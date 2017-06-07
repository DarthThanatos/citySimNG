import pygame
from Consts import FONT, FONT_SIZE, GREEN


def draw_text(pos_x, pos_y, msg, color, surface):
    font = pygame.font.SysFont(FONT, FONT_SIZE)
    screen_text = font.render(msg, True, color)
    surface.blit(screen_text, [pos_x, pos_y])
    return screen_text.get_size()


def calculate_text_size(msg):
    font = pygame.font.SysFont(FONT, FONT_SIZE)
    screen_text = font.render(msg, True, GREEN)
    return screen_text.get_size()


# TODO: better dealing with newlines
def draw_text_with_wrapping(pos_x, pos_y, max_width, msg, color, surface):
    font = pygame.font.SysFont(FONT, FONT_SIZE)
    space_width = font.size(' ')[0]  # get space width
    curr_x, curr_y = pos_x, pos_y
    for word in msg.split(" "):
        word_surface = font.render(word, True, color)
        word_width, word_height = word_surface.get_size()
        if curr_x + word_width >= max_width:
            curr_x = pos_x  # Reset the x.
            curr_y += word_height  # Start on new row.
        surface.blit(word_surface, (curr_x, curr_y))
        curr_x += word_width + space_width
