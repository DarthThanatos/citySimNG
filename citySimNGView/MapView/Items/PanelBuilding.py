from Building import Building
from MapView.Popups.BuildingsPanelPopup import BuildingsPanelPopup


class PanelBuilding(Building):
    """ This class represents an instance of building. """
    def __init__(self, name, id, texture_path, resource_cost, consumes, produces, pos_x, pos_y, width, height):
        """ Constructor.

        :param name: building's name
        :param id: building's unique id
        :param texture_path: path to building's texture
        :param resource_cost: amount of resources needed to construct this building
        :param consumes: amount of resources this building consumes
        :param produces: amount of resources this building produces
        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: building's width
        :param height: building's height
        """
        Building.__init__(self, name, id, texture_path, resource_cost, consumes, produces, pos_x, pos_y, width, height)

        self.popup = None

    def create_popup(self, pos_x, pos_y, width, height, surface):
        popup = BuildingsPanelPopup(pos_x, pos_y, width, height, self, surface)

        return popup
