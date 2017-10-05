from CreatorView.RelativePaths import relative_textures_path

from MapView.Consts import BUILDINGS_PANEL_TEXTURE, GREEN, RED
from MapView.Items.Button import Button
from MapView.Items.Resource import Resource
from MapView.Panels.Panel import Panel
from MapView.Utils import draw_text
from MapView.Items.Resources import resources, draw_resources_info
import pygame

DELETE_BUILDING_BUTTON_HEIGHT = 0.25
DELETE_BUILDING_BUTTON_WIDTH = 0.1
STOP_PRODUCTION_BUTTON_WIDTH = 0.1
STOP_PRODUCTION_BUTTON_HEIGHT = 0.25
SPACE = 0.1


class InfoPanel(Panel):
    """ This class represents an instance of panel containing information about selected building. """
    def __init__(self, pos_x, pos_y, width, height, blit_surface, del_building_fun, stop_production_fun):
        """ Constructor.

        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: panel's width
        :param height: panel's height
        :param surface: surface on which panel should be drawn
        :param del_building_fun: function performed when delete building button is clicked
        :param stop_production_fun: function performed when stop production button is clicked
        """
        Panel.__init__(self, pos_x, pos_y, width, height, BUILDINGS_PANEL_TEXTURE, blit_surface, 'Info Panel')
        self.curr_building = None
        self.buttons_sprites = pygame.sprite.Group()
        self.resources_sprites = pygame.sprite.Group()
        self.produces = {}
        self.consumes = {}

        self.del_building_button = Button(
            self.pos_x + self.width - DELETE_BUILDING_BUTTON_WIDTH * self.width,
            self.pos_y, DELETE_BUILDING_BUTTON_WIDTH * self.width, DELETE_BUILDING_BUTTON_HEIGHT * self.height,
            relative_textures_path + 'DeleteBuilding.png', del_building_fun, self, "Delete building")

        self.stop_production_button = Button(
            self.pos_x + self.width - STOP_PRODUCTION_BUTTON_WIDTH * self.width,
            self.pos_y + self.height * DELETE_BUILDING_BUTTON_HEIGHT + self.height * SPACE,
            STOP_PRODUCTION_BUTTON_WIDTH * self.width, STOP_PRODUCTION_BUTTON_HEIGHT * self.height,
            relative_textures_path + 'StopProduction.png', stop_production_fun, self, "Stop production in building")

        self.buttons_sprites.add(self.del_building_button, self.stop_production_button)
        self.all_sprites.add(self.buttons_sprites)

    def draw(self):
        """ Draw info panel with buttons and information about currently selected building.
        Before drawing in panel it is being cleaned.
        """
        self.clean()
        self.all_sprites.remove(self.resources_sprites)
        self.resources_sprites = pygame.sprite.Group()

        if self.curr_building:
            # draw buttons
            self.surface.blit(self.del_building_button.image, (self.del_building_button.rect[0] - self.pos_x,
                                                               self.del_building_button.rect[1] - self.pos_y))
            self.surface.blit(self.stop_production_button.image,
                                     (self.stop_production_button.rect[0] - self.pos_x,
                                      self.stop_production_button.rect[1] - self.pos_y))
            self.buttons_sprites.add(self.del_building_button, self.stop_production_button)
            self.all_sprites.add(self.buttons_sprites)

            # draw text
            curr_y = draw_text(0, 0, self.curr_building.name, GREEN, self.surface)[1]
            curr_x, curr_y = draw_text(0, curr_y, 'Produces: ', GREEN, self.surface)
            curr_y = draw_resources_info(self.curr_building.produces, self.produces, curr_x, curr_y, self.width,
                                         self, 20, 20, self.resources_sprites)
            curr_x = draw_text(0, curr_y, 'Consumes: ', RED, self.surface)[0]
            curr_y = draw_resources_info(self.curr_building.consumes, self.consumes, curr_x, curr_y, self.width,
                                         self, 20, 20, self.resources_sprites)
            self.all_sprites.add(self.resources_sprites)

        # draw panel
        self.blit_surface.blit(self.surface, (self.pos_x, self.pos_y))

    def set_stop_production_button_texture(self):
        """ Set texture for stop production button according to building state """
        if self.curr_building.is_running:
            self.stop_production_button.set_texture(relative_textures_path + 'StopProduction.png')
        else:
            self.stop_production_button.set_texture(relative_textures_path + 'Start.png')

    def create_resources_sprites(self):
        for resource in self.curr_building.produces:
            resource_sprite = Resource(resource, resources[resource]['texture_path'], 20, 20)
            self.produces[resource] = resource_sprite
            self.resources_sprites.add(resource_sprite)
        for resource in self.curr_building.consumes:
            resource_sprite = Resource(resource, resources[resource]['texture_path'], 20, 20)
            self.consumes[resource] = resource_sprite
            self.resources_sprites.add(resource_sprite)
        self.all_sprites.add(self.resources_sprites)
