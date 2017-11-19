import pygame
from MapView.Popups.BuildingsPanelPopup import BuildingsPanelPopup
from MapView.Consts import RED
from MapView.Items.Building import Building

DISABLED_SHADOW_ALPHA_LEVEL = 128

class PanelBuilding(Building):
    """ This class represents an instance of building. """
    def __init__(self, name, id, texture_path, type, resource_cost, consumes,
                 produces, dwellers_amount, dwellers_name, pos_x, pos_y, width,
                 height, is_enabled):
        """ Constructor.

        :param name: building's name
        :param id: building's unique id
        :param texture_path: path to building's texture
        :param resource_cost: amount of resources needed to construct this
        building
        :param consumes: amount of resources this building consumes
        :param produces: amount of resources this building produces
        :param dwellers_amount: map containing type and amount of dwellers that
         should work in this building
        :param pos_x: x position [px]
        :param pos_y: y position [px]
        :param width: building's width [px]
        :param height: building's height [px]
        """
        Building.__init__(self, name, id, texture_path, type, resource_cost,
                          consumes, produces, dwellers_amount, dwellers_name,
                          pos_x, pos_y, width, height)

        self.popup = None
        self.is_enabled = is_enabled

    def create_popup(self, pos_x, pos_y, width, height, texture_path, surface):
        """ Create popup for building.

        :param pos_x: popup x position [px]
        :param pos_y: popup y position [px]
        :param width: popup width [px]
        :param height: popup height [px]
        :param surface: surface on which popup should be drawn
        :return: popup
        """
        popup = BuildingsPanelPopup(pos_x, pos_y, width, height, texture_path,
                                    self, surface)

        return popup

    def draw(self, surface, pos_x, pos_y):
        surface.blit(self.image, (pos_x, pos_y))
        if not self.is_enabled:
            s = pygame.Surface((self.width, self.height))  # the size of rect
            s.set_alpha(DISABLED_SHADOW_ALPHA_LEVEL)  # alpha level
            s.fill(RED)  # this fills the entire surface
            surface.blit(s, (pos_x, pos_y))
