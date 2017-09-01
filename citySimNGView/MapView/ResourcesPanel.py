import json

import pygame
from Resource import Resource
from Consts import GREEN, RESOURCES_SPACE, RESOURCES_PANEL_TEXTURE, RESOURCES_PANEL_ARROW_Y, \
    RESOURCES_PANEL_LEFT_ARROW_X, RESOURCES_PANEL_RIGHT_ARROW_X, RESOURCES_ARROW_BUTTON_HEIGHT, RESOURCES_ARROW_BUTTON_WIDTH, \
    DWELLER_ICON_WIDTH, DWELLER_ICON_HEIGHT
from RelativePaths import relative_textures_path
from Panel import Panel
from Utils import draw_text, calculate_text_size, center_image_y
from Button import Button


class ResourcesPanel(Panel):
    it = 0

    def __init__(self, pos_x, pos_y, width, height, main_panel, game_screen):
        Panel.__init__(self, pos_x, pos_y, width, height, RESOURCES_PANEL_TEXTURE)
        self.game_screen = game_screen
        self.resources = {}
        self.main_panel = main_panel

        self.right_arrow = Button(self.width - RESOURCES_ARROW_BUTTON_WIDTH * self.width, self.pos_y,
                                  int(RESOURCES_ARROW_BUTTON_WIDTH * self.width),
                                  int(RESOURCES_ARROW_BUTTON_HEIGHT * self.height),
                                  relative_textures_path + 'RightArrow.png', self, self.scroll_resources_panel_right)

        self.left_arrow = Button(self.pos_x, self.pos_y, int(RESOURCES_ARROW_BUTTON_WIDTH * self.width),
                                 int(RESOURCES_ARROW_BUTTON_HEIGHT * self.height),
                                 relative_textures_path + "LeftArrow.png", self, self.scroll_resources_panel_left)
        self.curr_dwellers_amount = 0
        self.curr_max_dwellers_amount = 0

    def draw_panel(self):
        self.resources_list = self.resources_info.keys()

        # draw empty panel
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))

        # draw dwellers info
        dwellers_info_width = self.draw_dwellers_info()

        # update left arrow pos_x and draw arrow buttons
        self.left_arrow.rect = self.left_arrow.image.get_rect(topleft=(dwellers_info_width, self.left_arrow.rect[1]))
        self.game_screen.blit(self.right_arrow.image, self.right_arrow.rect)
        self.game_screen.blit(self.left_arrow.image, self.left_arrow.rect)

        # draw resources information
        pos_x = self.left_arrow.rect[0] + self.left_arrow.width
        self.displayed_all = True
        for i in range(self.it, len(self.resources_list)):
            resource = self.resources_list[i]
            image = self.main_panel.resources.resources[resource].image
            text_size = calculate_text_size("{}".format(self.resources_info[resource]))
            width = image.get_size()[0] + text_size[0] + pos_x
            if width > self.width - RESOURCES_ARROW_BUTTON_WIDTH * self.width:
                self.displayed_all = False
                break
            self.game_screen.blit(image, (pos_x, center_image_y(self.main_panel.resources.resources[resource].height,
                                                                self.pos_y, self.height)))
            draw_text(pos_x + image.get_size()[0] + RESOURCES_SPACE, center_image_y(text_size[1], self.pos_y, self.height),
                      "{}".format(self.resources_info[resource]), GREEN, self.game_screen)
            pos_x = width + 2 * RESOURCES_SPACE

    def scroll_resources_panel_right(self):
        if self.it < len(self.resources_list) and not self.displayed_all:
            self.it += 1
            self.draw_panel()

    def scroll_resources_panel_left(self):
        if self.it > 0:
            self.it -= 1
            self.draw_panel()

    def redraw_panel(self, map_view):
        self.draw_panel()

    def draw_dwellers_info(self):
        image = pygame.image.load(relative_textures_path + "dweller.jpg")
        image = pygame.transform.scale(image, (int(DWELLER_ICON_WIDTH * self.width), int(DWELLER_ICON_HEIGHT * self.height)))
        rect = image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.game_screen.blit(image, (rect[0], center_image_y(int(DWELLER_ICON_HEIGHT * self.height), rect[1], self.height)))

        text_size = calculate_text_size("{}".format(self.curr_dwellers_amount))

        text_width = draw_text(int(DWELLER_ICON_WIDTH * self.width), center_image_y(text_size[1], self.pos_y, self.height),
                               "{}".format(self.curr_dwellers_amount), GREEN,
                               self.game_screen)[0]

        return (int(DWELLER_ICON_WIDTH * self.width)) + text_width

