import pygame
from RelativePaths import relative_textures_path

from MapView.Consts import GREEN, RESOURCES_SPACE, RESOURCES_PANEL_TEXTURE, RESOURCES_ARROW_BUTTON_HEIGHT, \
    RESOURCES_ARROW_BUTTON_WIDTH, \
    DWELLER_ICON_WIDTH, DWELLER_ICON_HEIGHT, RESOURCE_WIDTH, RESOURCE_HEIGHT
from MapView.Items.Button import Button
from MapView.Panels.Panel import Panel
from MapView.Utils import draw_text, calculate_text_size, center_image_y_pos
from MapView.Items.Resources import resources


class ResourcesPanel(Panel):
    """ This class represents an instance of panel containing information about dwellers and resources. """

    first_disp_res_index = 0

    def __init__(self, pos_x, pos_y, width, height, surface, initial_resources_values, initial_resources_incomes):
        """ Constructor.

        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: panel's width
        :param height: panel's height
        :param initial_resources_values: initial amount of resources
        :param initial_resources_incomes: initial incomes of resources
        """
        Panel.__init__(self, pos_x, pos_y, width, height, RESOURCES_PANEL_TEXTURE, surface)
        self.resources_values = initial_resources_values
        self.resources_incomes = initial_resources_incomes

        self.displayed_last = True

        self.curr_dwellers_amount = 0
        self.curr_max_dwellers_amount = 0

        self.right_arrow = Button(self.width - RESOURCES_ARROW_BUTTON_WIDTH * self.width, self.pos_y,
                                  RESOURCES_ARROW_BUTTON_WIDTH * self.width,
                                  RESOURCES_ARROW_BUTTON_HEIGHT * self.height,
                                  relative_textures_path + 'RightArrow.png', self.scroll_resources_panel_right, self)

        self.left_arrow = Button(self.pos_x, self.pos_y, RESOURCES_ARROW_BUTTON_WIDTH * self.width,
                                 RESOURCES_ARROW_BUTTON_HEIGHT * self.height,
                                 relative_textures_path + "LeftArrow.png", self.scroll_resources_panel_left, self)

        self.dweller_image = pygame.image.load(relative_textures_path + "dweller.jpg")
        self.dweller_image = pygame.transform.scale(self.dweller_image, (int(DWELLER_ICON_WIDTH * self.width),
                                                                         int(DWELLER_ICON_HEIGHT * self.height)))
        self.dweller_rect = self.dweller_image.get_rect(topleft=(self.pos_x,
                                                                 center_image_y_pos(
                                                                     int(DWELLER_ICON_HEIGHT * self.height),
                                                                     self.pos_y, self.height)))

    def draw(self):
        """ Draw resources panel and items it contains: dwellers info, resources info and arrows for
        scrolling resources. Before drawing in panel it is being cleaned. """
        self.clean()
        curr_x = self.pos_x

        # draw dwellers info and add it's width to curr_x
        curr_x += self.draw_dwellers_info()[0]

        # update left arrow pos_x and draw arrow buttons
        self.left_arrow.rect = self.left_arrow.image.get_rect(topleft=(curr_x, self.left_arrow.rect[1]))
        self.panels_surface.blit(self.right_arrow.image, self.right_arrow.rect)
        self.panels_surface.blit(self.left_arrow.image, self.left_arrow.rect)
        curr_x += self.left_arrow.width

        # draw resources information
        self.displayed_last = True
        for i in range(self.first_disp_res_index, len(resources)):
            resource = resources.keys()[i]
            image = resources[resource].image
            image = pygame.transform.scale(image, (int(self.width * RESOURCE_WIDTH),
                                                   int(self.height * RESOURCE_HEIGHT)))

            if self.resources_incomes[resource] >= 0:
                sign = "+"
            else:
                sign = ""

            # check if info for current resource will fit in
            text_size = calculate_text_size("{} {} {}".format(self.resources_values[resource], sign,
                                                              self.resources_incomes[resource]))
            width = image.get_size()[0] + text_size[0] + curr_x
            if width > self.width - RESOURCES_ARROW_BUTTON_WIDTH * self.width:
                self.displayed_last = False
                break

            # draw info for current resource
            self.panels_surface.blit(image, (curr_x, center_image_y_pos(image.get_size()[1], self.pos_y, self.height)))
            draw_text(curr_x + image.get_size()[0] + RESOURCES_SPACE,
                      center_image_y_pos(text_size[1], self.pos_y, self.height),
                      "{} {} {}".format(self.resources_values[resource], sign, self.resources_incomes[resource]), GREEN,
                      self.panels_surface)

            # update current x position
            curr_x += image.get_size()[0] + text_size[0] + 2 * RESOURCES_SPACE

        self.surface.blit(self.panels_surface, (self.pos_x, self.pos_y))

    def scroll_resources_panel_right(self):
        """ Scroll displayed resources to the right. """
        if self.first_disp_res_index < len(resources) and not self.displayed_last:
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
        self.panels_surface.blit(self.dweller_image, self.dweller_rect)

        # TODO: mby find better way?
        text_height = calculate_text_size("{}".format(self.curr_dwellers_amount))[1]
        text_x_pos = self.dweller_image.get_size()[0] + RESOURCES_SPACE
        text_width = draw_text(text_x_pos, center_image_y_pos(text_height, self.pos_y, self.height),
                               "{}".format(self.curr_dwellers_amount), GREEN, self.panels_surface)[0]

        return (self.dweller_image.get_size()[0] + text_width + RESOURCES_SPACE,
                self.dweller_image.get_size()[1])
