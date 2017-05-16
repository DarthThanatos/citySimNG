import pygame
from Resource import Resource
from Consts import GREEN, RESOURCES_SPACE, RESOURCES_PANEL_TEXTURE, RESOURCES_PANEL_ARROW_Y, \
    RESOURCES_PANEL_LEFT_ARROW_X, RESOURCES_PANEL_RIGHT_ARROW_X, RESOURCES_ARROW_BUTTON_HEIGHT, RESOURCES_ARROW_BUTTON_WIDTH
from RelativePaths import relative_textures_path


class ResourcesPanel(pygame.sprite.Sprite):
    it = 0

    def __init__(self, game_screen, pos_x, pos_y, size_x, size_y, main_panel):
        pygame.sprite.Sprite.__init__(self)
        self.game_screen = game_screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.resources = {}
        self.main_panel = main_panel

        self.image = pygame.image.load(RESOURCES_PANEL_TEXTURE)
        self.image = pygame.transform.scale(self.image, (int(self.size_x), int(self.size_y)))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        self.right_arrow_image = pygame.image.load(relative_textures_path + 'RightArrow.png')
        self.right_arrow_image = pygame.transform.scale(self.right_arrow_image, (int(RESOURCES_ARROW_BUTTON_WIDTH * self.size_x),
                                                                                 int(RESOURCES_ARROW_BUTTON_HEIGHT * self.size_y)))
        self.right_arrow_rect = self.right_arrow_image.get_rect(
            topleft=(self.pos_x + RESOURCES_PANEL_RIGHT_ARROW_X * self.size_x,
                     self.pos_y + RESOURCES_PANEL_ARROW_Y * self.size_y))

        self.left_arrow_image = pygame.image.load(relative_textures_path + 'LeftArrow.png')
        self.left_arrow_image = pygame.transform.scale(self.left_arrow_image, (int(RESOURCES_ARROW_BUTTON_WIDTH * self.size_x),
                                                                               int(RESOURCES_ARROW_BUTTON_HEIGHT * self.size_y)))
        self.left_arrow_rect = self.left_arrow_image.get_rect(
            topleft=(self.pos_x + RESOURCES_PANEL_LEFT_ARROW_X * self.size_x,
                     self.pos_y + RESOURCES_PANEL_ARROW_Y * self.size_y))

    def draw_resources_panel(self, resources_info):
        self.resources_list = resources_info.keys()
        self.resources_info = resources_info
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))

        self.game_screen.blit(self.right_arrow_image, (self.pos_x + RESOURCES_PANEL_RIGHT_ARROW_X * self.size_x,
                                                       self.pos_y + RESOURCES_PANEL_ARROW_Y * self.size_y))

        self.game_screen.blit(self.left_arrow_image, (self.pos_x + RESOURCES_PANEL_LEFT_ARROW_X * self.size_x,

                                                      self.pos_y + RESOURCES_PANEL_ARROW_Y * self.size_y))
        pos_x = 0
        self.displayed_all = True
        for i in range(self.it, len(self.resources_list)):
            resource = self.resources_list[i]
            image = self.resources[resource].image
            text_size = self.main_panel.mes("{}: {} ".format(resource, resources_info[resource]), GREEN,
                                            pos_x + image.get_size()[0] + RESOURCES_SPACE, self.pos_y, draw=False)
            width = image.get_size()[0] + text_size[0] + pos_x
            if width > self.size_x:
                self.displayed_all = False
                break
            self.game_screen.blit(image, (pos_x, self.pos_y))
            text_size = self.main_panel.mes("{}: {} ".format(resource, resources_info[resource]), GREEN,
                                            pos_x + image.get_size()[0] + RESOURCES_SPACE, self.pos_y)
            pos_x = width + RESOURCES_SPACE

    def add_resources_to_resources_panel(self, resources_info):
        for (i, resource) in enumerate(resources_info):
            resource_sprite = Resource(resource["name"], resource["texturePath"], self.game_screen.get_size())
            self.resources[resource["name"]] = resource_sprite

    def scroll_resources_panel_right(self):
        if self.it < len(self.resources_list) and not self.displayed_all:
            self.it += 1
            self.draw_resources_panel(self.resources_info)

    def scroll_resources_panel_left(self):
        if self.it > 0:
            self.it -= 1
            self.draw_resources_panel(self.resources_info)
