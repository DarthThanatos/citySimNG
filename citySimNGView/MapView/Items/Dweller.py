from CreatorView.RelativePaths import relative_textures_path
from MapView.CustomSprites.BasicSprite import BasicSprite


class Dweller(BasicSprite):
    """ This class represents an instance of dweller. """
    def __init__(self, name, texture_path, width, height):
        """ Constructor.

        :param name: dweller's name
        :param texture_path: path to dweller's texture
        :param width: dweller's width [px]
        :param height: dweller's height [px]
        """
        BasicSprite.__init__(self, 0, 0, width, height, texture_path, name)
        self.name = name
