import pygame
from MapView.Consts import DEFAULT_BUILDING_TEXTURE, WHITE


class Building(pygame.sprite.Sprite):
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
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.id = id
        self.texture_path = texture_path
        self.resources_cost = resource_cost
        self.consumes = consumes
        self.produces = produces
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height

        self.is_running = True

        self.load_image()

    def load_image(self):
        """ Load texture for building from file, scale it and get it's rect. """
        try:
            self.image = pygame.image.load(self.texture_path)
        except Exception:
            self.texture_path = DEFAULT_BUILDING_TEXTURE
            self.image = pygame.image.load(self.texture_path)
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

