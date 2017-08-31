import pygame

from Button import Button


class NavigationArrow(Button):
    """ This class represents an instance of navigation arrow. """
    def __init__(self, pos_x, pos_y, width, height, texture_path, rotation, direction, panel, action):
        """ Constructor.

        :param pos_x: x position on screen
        :param pos_y: y position on screen
        :param width: arrow's width
        :param height: arrow's height
        :param texture_path: path to arrow's texture
        :param rotation: arrow's rotation angle
        :param direction: arrow's direction
        :param panel: panel in which arrow is located
        :param action: action performed when arrow is released
        """
        Button.__init__(self, pos_x, pos_y, width, height, texture_path, action, panel)
        self.rotation = rotation
        self.direction = direction

        self.image = pygame.image.load(texture_path)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def release_button(self):
        """ Perform appropriate action and restore button to normal size. """
        self.action(*self.args)
        self.image = pygame.image.load(self.texture)
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
