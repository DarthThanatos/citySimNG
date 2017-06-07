import pygame
from Resource import Resource
from Consts import GREEN, RESOURCES_SPACE, RESOURCES_PANEL_TEXTURE, RESOURCES_PANEL_ARROW_Y, \
    RESOURCES_PANEL_LEFT_ARROW_X, RESOURCES_PANEL_RIGHT_ARROW_X, RESOURCES_ARROW_BUTTON_HEIGHT, RESOURCES_ARROW_BUTTON_WIDTH
from RelativePaths import relative_textures_path
from Panel import Panel
from Utils import draw_text, calculate_text_size


class ResourcesPanel(Panel):
    it = 0

    def __init__(self, pos_x, pos_y, width, height, main_panel, game_screen):
        Panel.__init__(self, pos_x, pos_y, width, height, RESOURCES_PANEL_TEXTURE)
        self.game_screen = game_screen
        self.resources = {}
        self.main_panel = main_panel

        self.right_arrow_image = pygame.image.load(relative_textures_path + 'RightArrow.png')
        self.right_arrow_image = pygame.transform.scale(self.right_arrow_image, (int(RESOURCES_ARROW_BUTTON_WIDTH * self.width),
                                                                                 int(RESOURCES_ARROW_BUTTON_HEIGHT * self.height)))
        self.right_arrow_rect = self.right_arrow_image.get_rect(
            topleft=(self.width - RESOURCES_ARROW_BUTTON_WIDTH * self.width,
                     self.height))

        self.left_arrow_image = pygame.image.load(relative_textures_path + 'LeftArrow.png')
        self.left_arrow_image = pygame.transform.scale(self.left_arrow_image, (int(RESOURCES_ARROW_BUTTON_WIDTH * self.width),
                                                                               int(RESOURCES_ARROW_BUTTON_HEIGHT * self.height)))
        self.left_arrow_rect = self.left_arrow_image.get_rect(
            topleft=(self.pos_x, self.height))

    def draw_panel(self):
        self.resources_list = self.resources_info.keys()
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))

        self.game_screen.blit(self.right_arrow_image, (self.width - RESOURCES_ARROW_BUTTON_WIDTH * self.width,
                                                       self.pos_y))

        self.game_screen.blit(self.left_arrow_image, (self.pos_x,
                                                      self.pos_y))

        pos_x = RESOURCES_ARROW_BUTTON_WIDTH * self.width
        self.displayed_all = True
        for i in range(self.it, len(self.resources_list)):
            resource = self.resources_list[i]
            image = self.main_panel.resources.resources[resource].image
            text_size = calculate_text_size("{}".format(self.resources_info[resource]))
            width = image.get_size()[0] + text_size[0] + pos_x
            if width > self.width - RESOURCES_ARROW_BUTTON_WIDTH * self.width:
                self.displayed_all = False
                break
            self.game_screen.blit(image, (pos_x, self.pos_y))
            draw_text(pos_x + image.get_size()[0] + RESOURCES_SPACE, self.pos_y,
                      "{}".format(self.resources_info[resource]), GREEN, self.game_screen)
            pos_x = width + RESOURCES_SPACE

    # def add_resources_to_resources_panel(self, resources_info):
    #     for (i, resource) in enumerate(resources_info):
    #         resource_sprite = Resource(resource["name"], resource["texturePath"], self.game_screen.get_size())
    #         self.resources[resource["name"]] = resource_sprite

    def scroll_resources_panel_right(self):
        if self.it < len(self.resources_list) and not self.displayed_all:
            self.it += 1
            self.draw_panel()

    def scroll_resources_panel_left(self):
        if self.it > 0:
            self.it -= 1
            self.draw_panel()
