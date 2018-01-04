import pygame
from CreatorView.RelativePaths import relative_textures_path

from MapView.Consts import YELLOW, RESOURCES_SPACE, \
    DWELLER_ICON_WIDTH, DWELLER_ICON_HEIGHT, RED
from MapView.Items.Button import Button
from MapView.Panels.Panel import Panel
from MapView.Utils import draw_text, calculate_text_size, center_image_y_pos
from MapView.Items.Resources import resources
from MapView.Items.PanelResource import PanelResource
from MapView.CustomSprites.BasicSprite import BasicSprite

RESOURCE_WIDTH = 0.05
RESOURCE_HEIGHT = 0.9
ARROW_BUTTON_HEIGHT = 0.9
ARROW_BUTTON_WIDTH = 0.04


class ResourcesPanel(Panel):
    """ This class represents an instance of panel containing information about dwellers and resources. """

    first_disp_res_index = 0

    def __init__(self, pos_x, pos_y, width, height, texture_path, blit_surface,
                 initial_resources_values, initial_resources_incomes,
                 initial_resources_consumption, initial_resources_balance,
                 resources_data, available_dwellers):
        """ Constructor.

        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: panel's width
        :param height: panel's height
        :param initial_resources_values: initial amount of resources
        :param initial_resources_incomes: initial incomes of resources
        :param resources_data: list of resources objects
        """
        Panel.__init__(self, pos_x, pos_y, width, height, texture_path,
                       blit_surface, "Resources Panel")
        self.resources_values = initial_resources_values
        self.resources_incomes = initial_resources_incomes
        self.resources_consumption = initial_resources_consumption
        self.resources_balance = initial_resources_balance
        self.resources_data = resources_data
        self.resources_sprites = pygame.sprite.Group()
        self.resources = {}

        self.parse_resources_data()

        self.displayed_last = True

        self.curr_dwellers_amount = 0
        self.curr_max_dwellers_amount = available_dwellers

        self.right_arrow = Button(self.width - ARROW_BUTTON_WIDTH * self.width,
                                  self.pos_y,
                                  ARROW_BUTTON_WIDTH * self.width,
                                  ARROW_BUTTON_HEIGHT * self.height,
                                  relative_textures_path + 'RightArrow.png',
                                  self.scroll_resources_panel_right, self,
                                  "Scroll right")
        self.left_arrow = Button(self.pos_x, self.pos_y,
                                 ARROW_BUTTON_WIDTH * self.width,
                                 ARROW_BUTTON_HEIGHT * self.height,
                                 relative_textures_path + "LeftArrow.png",
                                 self.scroll_resources_panel_left, self,
                                 "Scroll left")
        self.all_sprites.add(self.right_arrow, self.left_arrow)

        self.dweller_sprite = BasicSprite(self.pos_x, center_image_y_pos(
            DWELLER_ICON_HEIGHT * self.height,
            self.pos_y, self.height),
                                          DWELLER_ICON_WIDTH * self.width,
                                          DWELLER_ICON_HEIGHT * self.height,
                                          relative_textures_path + "Middleages\\dwellers\\mieszczanin.png",
                                          "Working dwellers / All dwellers")
        self.all_sprites.add(self.dweller_sprite)

    def draw(self):
        """ Draw resources panel and items it contains: dwellers info, resources info and arrows for
        scrolling resources. Before drawing in panel it is being cleaned. """
        self.clean()
        self.all_sprites.remove(self.resources_sprites)
        self.resources_sprites = pygame.sprite.Group()

        curr_x = self.pos_x

        # draw dwellers info and add it's width to curr_x
        curr_x += self.draw_dwellers_info()[0]

        # update left arrow pos_x and draw arrow buttons
        self.left_arrow.rect = self.left_arrow.image.get_rect(
            topleft=(curr_x, self.left_arrow.rect[1]))
        self.surface.blit(self.right_arrow.image, self.right_arrow.rect)
        self.surface.blit(self.left_arrow.image, self.left_arrow.rect)
        curr_x += self.left_arrow.width

        # draw resources information
        self.displayed_last = True
        for i in range(self.first_disp_res_index, len(resources)):
            resource_name = resources.keys()[i]
            image = self.resources[resource_name].image

            self.resources[resource_name].consumption = \
            self.resources_consumption[resource_name]
            self.resources[resource_name].production = self.resources_incomes[
                resource_name]
            self.resources[resource_name].update_popup_text()

            if self.resources_balance[resource_name] >= 0:
                sign = "+"
            else:
                sign = ""

            # check if info for current resource will fit in
            text_size = calculate_text_size(
                "{} {} {}".format(self.resources_values[resource_name], sign,
                                  self.resources_balance[resource_name]))
            width = image.get_size()[0] + text_size[0] + curr_x
            if width > self.width - ARROW_BUTTON_WIDTH * self.width:
                self.displayed_last = False
                break

            # draw info for current resource
            self.resources[resource_name].rect = image.get_rect(
                topleft=(curr_x,
                         center_image_y_pos(image.get_size()[1], self.pos_y,
                                            self.height)))
            self.surface.blit(image, self.resources[resource_name].rect)
            self.resources_sprites.add(self.resources[resource_name])

            draw_text(curr_x + image.get_size()[0] + RESOURCES_SPACE,
                      center_image_y_pos(text_size[1], self.pos_y,
                                         self.height),
                      "{} {} {}".format(self.resources_values[resource_name],
                                        sign,
                                        self.resources_balance[resource_name]),
                      YELLOW,
                      self.surface)

            # update current x position
            curr_x += image.get_size()[0] + text_size[0] + 2 * RESOURCES_SPACE

        self.all_sprites.add(self.resources_sprites)
        self.blit_surface.blit(self.surface, (self.pos_x, self.pos_y))

    def scroll_resources_panel_right(self):
        """ Scroll displayed resources to the right. """
        if self.first_disp_res_index < len(
                resources) and not self.displayed_last:
            self.first_disp_res_index += 1
            # self.draw()

    def scroll_resources_panel_left(self):
        """ Scroll displayed resources to the left. """
        if self.first_disp_res_index > 0:
            self.first_disp_res_index -= 1
            # self.draw()

    def draw_dwellers_info(self):
        """ Draw information about dwellers.

        :return: tuple containing width and height of drawn info
        """
        self.surface.blit(self.dweller_sprite.image, self.dweller_sprite.rect)

        # TODO: mby find better way?
        text_height = calculate_text_size(
            "{} / {}".format(self.curr_dwellers_amount,
                             self.curr_max_dwellers_amount))[1]
        text_x_pos = self.dweller_sprite.image.get_size()[0] + RESOURCES_SPACE

        color = YELLOW if self.curr_dwellers_amount < self.curr_max_dwellers_amount else RED

        text_width = draw_text(text_x_pos,
                               center_image_y_pos(text_height, self.pos_y,
                                                  self.height),
                               "{} / {}".format(self.curr_dwellers_amount,
                                                self.curr_max_dwellers_amount),
                               color,
                               self.surface)[0]

        return (
        self.dweller_sprite.image.get_size()[0] + text_width + RESOURCES_SPACE,
        self.dweller_sprite.image.get_size()[1])

    def parse_resources_data(self):
        for resource in self.resources_data:
            resource_sprite = PanelResource(resource.getName(),
                                            resource.getTexturePath(),
                                            self.width * RESOURCE_WIDTH,
                                            self.height * RESOURCE_HEIGHT,
                                            self.resources_consumption[
                                                resource.getName()],
                                            self.resources_incomes[
                                                resource.getName()])
            self.resources[resource.getName()] = resource_sprite
            self.resources_sprites.add(resource_sprite)
            self.all_sprites.add(resource_sprite)
