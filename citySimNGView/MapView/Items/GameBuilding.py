from MapView.Items.Building import Building


class GameBuilding(Building):
    """ This class represents an instance of building. """
    def __init__(self, name, id, texture_path, type, resource_cost, consumes,
                 produces, dwellers_amount, dwellers_name, pos_x, pos_y, width,
                 height):
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

        self.is_running = True
        self.working_dwellers = 0

    def draw(self, surface, pos_x, pos_y):
        surface.blit(self.image, (pos_x, pos_y))
