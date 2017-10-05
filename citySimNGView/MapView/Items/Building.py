from Converter import Converter
from MapView.CustomSprites.BasicSprite import BasicSprite


class Building(BasicSprite):
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
        BasicSprite.__init__(self, pos_x, pos_y, width, height, texture_path, name)

        self.name = name
        self.id = id
        self.resources_cost = Converter().convertJavaMapToDict(resource_cost)
        self.consumes = Converter().convertJavaMapToDict(consumes)
        self.produces = Converter().convertJavaMapToDict(produces)

        self.is_running = True

    def draw(self, surface, pos_x, pos_y):
        surface.blit(self.image, (pos_x, pos_y))
