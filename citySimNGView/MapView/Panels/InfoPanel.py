from CreatorView.RelativePaths import relative_textures_path

from MapView.Consts import YELLOW, RED, LIGHT_BLUE
from MapView.Items.Button import Button
from MapView.Items.Resource import Resource
from MapView.Items.Dweller import Dweller
from MapView.Panels.Panel import Panel
from MapView.Utils import draw_text
from MapView.Items.Resources import resources, draw_items_info
from MapView.Items.Dwellers import dwellers, draw_dwellers_info
import pygame

DELETE_BUILDING_BUTTON_HEIGHT = 0.25
DELETE_BUILDING_BUTTON_WIDTH = 0.1
STOP_PRODUCTION_BUTTON_WIDTH = 0.1
STOP_PRODUCTION_BUTTON_HEIGHT = 0.25
ITEM_IMAGE_WIDTH = 35
ITEM_IMAGE_HEIGHT = 35
SPACE = 0.1
FONT_SIZE = 25


class InfoPanel(Panel):
    """ This class represents an instance of panel containing information about
     selected building. """

    def __init__(self, pos_x, pos_y, width, height, texture_path, blit_surface,
                 del_building_fun, stop_production_fun):
        """ Constructor.

        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: panel's width
        :param height: panel's height
        :param surface: surface on which panel should be drawn
        :param del_building_fun: function performed when delete building
        button is clicked
        :param stop_production_fun: function performed when stop production
        button is clicked
        """
        Panel.__init__(self, pos_x, pos_y, width, height, texture_path,
                       blit_surface, 'Info Panel')
        self.curr_building = None
        self.buttons_sprites = pygame.sprite.Group()
        self.sprites_for_current_building = pygame.sprite.Group()
        self.produces = {}
        self.consumes = {}

        self.create_buttons(del_building_fun, stop_production_fun)

    def draw(self):
        """ Draw info panel with buttons and information about currently
        selected building. Before drawing in panel it is being cleaned.
        """
        self.clean()
        self.all_sprites.remove(self.sprites_for_current_building)
        self.all_sprites.remove(self.buttons_sprites)
        self.sprites_for_current_building.empty()
        self.buttons_sprites.empty()

        if self.curr_building:
            # draw buttons
            self.surface.blit(self.del_building_button.image,
                              (self.del_building_button.rect[0] - self.pos_x,
                               self.del_building_button.rect[1] - self.pos_y))
            self.surface.blit(self.stop_production_button.image,
                              (
                              self.stop_production_button.rect[0] - self.pos_x,
                              self.stop_production_button.rect[
                                  1] - self.pos_y))
            self.buttons_sprites.add(self.del_building_button,
                                     self.stop_production_button)
            self.all_sprites.add(self.buttons_sprites)

            # draw text
            curr_y = draw_text(0, 0, self.curr_building.name, YELLOW,
                               self.surface, FONT_SIZE)[1]

            curr_x, curr_y = draw_text(0, curr_y, 'Produces: ', YELLOW,
                                       self.surface, FONT_SIZE)
            curr_y = \
            draw_items_info(self.curr_building.produces, curr_x, curr_y,
                            self.width, self, self.produces,
                            self.sprites_for_current_building,
                            font_size=FONT_SIZE)[1]

            curr_x = draw_text(0, curr_y, 'Consumes: ', RED, self.surface,
                               FONT_SIZE)[0]
            curr_y = \
            draw_items_info(self.curr_building.consumes, curr_x, curr_y,
                            self.width, self, self.consumes,
                            self.sprites_for_current_building, color=RED,
                            font_size=FONT_SIZE)[1]

            curr_x = draw_text(0, curr_y, 'Dwellers: ', LIGHT_BLUE,
                               self.surface, FONT_SIZE)[0]
            curr_x = draw_dwellers_info(self.curr_building.dwellers_name,
                                        '{} / {}'.format(
                                            self.curr_building.working_dwellers,
                                            self.curr_building.required_dwellers),
                                        curr_x, curr_y, self,
                                        self.dweller_sprite, color=LIGHT_BLUE,
                                        font_size=FONT_SIZE)
            self.sprites_for_current_building.add(self.dweller_sprite)

            self.all_sprites.add(self.sprites_for_current_building)

        # draw panel
        self.blit_surface.blit(self.surface, (self.pos_x, self.pos_y))

    def set_stop_production_button_texture(self):
        """ Set texture for stop production button according to building state """
        if self.curr_building.is_running:
            self.stop_production_button.set_texture(
                relative_textures_path + 'new\\stop.png')
        else:
            self.stop_production_button.set_texture(
                relative_textures_path + 'Start.png')

    def create_sprites_for_current_building(self):
        for resource in self.curr_building.produces:
            resource_sprite = Resource(resource,
                                       resources[resource]['texture_path'],
                                       ITEM_IMAGE_WIDTH,
                                       ITEM_IMAGE_HEIGHT)
            self.produces[resource] = resource_sprite
            self.sprites_for_current_building.add(resource_sprite)
        for resource in self.curr_building.consumes:
            resource_sprite = Resource(resource,
                                       resources[resource]['texture_path'],
                                       ITEM_IMAGE_WIDTH,
                                       ITEM_IMAGE_HEIGHT)
            self.consumes[resource] = resource_sprite
            self.sprites_for_current_building.add(resource_sprite)
        self.dweller_sprite = Dweller(self.curr_building.dwellers_name,
                                      dwellers[
                                          self.curr_building.dwellers_name]
                                      ['texture_path'],
                                      ITEM_IMAGE_WIDTH,
                                      ITEM_IMAGE_HEIGHT)
        self.sprites_for_current_building.add(self.dweller_sprite)
        self.all_sprites.add(self.sprites_for_current_building)

    def prepare_dwellers_info(self):
        self.dwellers_info = '{} / {}'.format(
            self.curr_building.working_dwellers,
            self.curr_building.required_dwellers)

    def create_buttons(self, del_building_fun, stop_production_fun):
        self.del_building_button = Button(
            self.pos_x + self.width - DELETE_BUILDING_BUTTON_WIDTH * self.width,
            self.pos_y, DELETE_BUILDING_BUTTON_WIDTH * self.width,
            DELETE_BUILDING_BUTTON_HEIGHT * self.height,
            relative_textures_path + 'new\\delete.png', del_building_fun,
            self, "Delete building")

        self.stop_production_button = Button(
            self.pos_x + self.width - STOP_PRODUCTION_BUTTON_WIDTH * self.width,
            self.pos_y + self.height * DELETE_BUILDING_BUTTON_HEIGHT + self.height * SPACE,
            STOP_PRODUCTION_BUTTON_WIDTH * self.width,
            STOP_PRODUCTION_BUTTON_HEIGHT * self.height,
            relative_textures_path + 'new\\stop.png', stop_production_fun,
            self, "Stop production in building")
