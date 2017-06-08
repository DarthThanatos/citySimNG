import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, width, height, texture, panel, action):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.width = width
        self.height = height
        self.texture = texture
        self.panel = panel
        self.action = action
        self.args = None

        self.image = pygame.image.load(texture)
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))

    def click_button(self, map_view, *args):
        self.image = pygame.transform.scale(self.image, (self.width/2, self.height/2))
        self.rect = self.image.get_rect(center=self.rect.center)
        self.panel.redraw_panel(map_view)
        self.args = args

    def release_button(self, map_view):
        self.action(*self.args)
        self.image = pygame.image.load(self.texture)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.panel.redraw_panel(map_view)


