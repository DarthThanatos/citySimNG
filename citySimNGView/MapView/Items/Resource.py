from CreatorView.RelativePaths import relative_textures_path
from MapView.CustomSprites.BasicSprite import BasicSprite


class Resource(BasicSprite):
    """ This class represents an instance of resource. """
    def __init__(self, name, texture_path, width, height):
        """ Constructor.

        :param name: resources's name
        :param texture_path: path to resource's texture
        """
        BasicSprite.__init__(self, 0, 0, width, height, texture_path, name)
        self.name = name
