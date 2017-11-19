import pygame
from MapView.Consts import DEFAULT_TEXTURE, WHITE

DEFAULT_TEXTURE_PATH = DEFAULT_TEXTURE


class BasicSprite(pygame.sprite.DirtySprite):
    """ This class represents an instance of basic sprite."""
    def __init__(self, pos_x, pos_y, width, height, texture_path, popup_text,
                 texture_rotation=0, rect_point='topleft'):
        """ Constructor.

        :param pos_x: x position [px] - this should be absolute pos x on screen
        :param pos_y: y position [px] - this should be absolute pos y on screen
        :param width: width [px] -> will be cast to integer
        :param height: height [px] -> will be cast to integer
        :param texture_path: path to texture
        :param popup_text: text displayed in popup
        :param texture_rotation: angle of texture rotation
        :param rect_point: keyword argument used to get image rect
        """
        pygame.sprite.DirtySprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = int(width)
        self.height = int(height)
        self.texture_path = texture_path
        self.popup_text = popup_text
        self.texture_rotation = texture_rotation

        self.load_texture(texture_rotation)
        self.set_rect(rect_point)

    def load_texture(self, texture_rotation=0):
        """ Load texture from file, scale it. """
        try:
            self.image = pygame.image.load(self.texture_path)
        except Exception:
            print 'Could not find texture: {}. Loading default texture.'.\
                format(self.texture_path)
            self.texture_path = DEFAULT_TEXTURE_PATH
            self.image = pygame.image.load(self.texture_path)
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.rotate(self.image, texture_rotation)
        self.image = pygame.transform.scale(self.image,
                                            (self.width, self.height))

    def set_rect(self, rect_point='topleft'):
        kw = {rect_point: (self.pos_x, self.pos_y)}
        self.rect = self.image.get_rect(**kw)

    # TODO: probably blit shouldn't be in rect position
    def draw(self, surface):
        surface.blit(self.image, self.rect)
