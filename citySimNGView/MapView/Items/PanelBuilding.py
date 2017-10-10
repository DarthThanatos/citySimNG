from Building import Building
from MapView.Popups.BuildingsPanelPopup import BuildingsPanelPopup
import pygame


class PanelBuilding(Building):
    """ This class represents an instance of building. """
    def __init__(self, name, id, texture_path, resource_cost, consumes, produces, pos_x, pos_y, width, height,
                 is_enabled):
        """ Constructor.

        :param name: building's name
        :param id: building's unique id
        :param texture_path: path to building's texture
        :param resource_cost: amount of resources needed to construct this building
        :param consumes: amount of resources this building consumes
        :param produces: amount of resources this building produces
        :param pos_x: x position [px]
        :param pos_y: y position [px]
        :param width: building's width [px]
        :param height: building's height [px]
        """
        Building.__init__(self, name, id, texture_path, resource_cost, consumes, produces, pos_x, pos_y, width, height)

        self.popup = None
        self.is_enabled = is_enabled

    def create_popup(self, pos_x, pos_y, width, height, surface):
        """ Create popup for building.

        :param pos_x: popup x position [px]
        :param pos_y: popup y position [px]
        :param width: popup width [px]
        :param height: popup height [px]
        :param surface: surface on which popup should be drawn
        :return: popup
        """
        popup = BuildingsPanelPopup(pos_x, pos_y, width, height, self, surface)

        return popup

    def draw(self, surface, pos_x, pos_y):
        surface.blit(self.image, (pos_x, pos_y))
        if not self.is_enabled:
            s = pygame.Surface((self.width, self.height))  # the size of your rect
            s.set_alpha(128)  # alpha level
            s.fill((255, 0, 0))  # this fills the entire surface
            surface.blit(s, (pos_x, pos_y))  # (0,0) are the top-left coordinates