import pygame
from Resource import Resource
from Consts import GREEN, RESOURCES_SPACE, RESOURCES_PANEL_TEXTURE


class ResourcesPanel(pygame.sprite.Sprite):
    def __init__(self, game_screen, pos_x, pos_y, size_x, size_y):
        pygame.sprite.Sprite.__init__(self)
        self.game_screen = game_screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.resources = {}

        self.image = pygame.image.load(RESOURCES_PANEL_TEXTURE)
        self.image = pygame.transform.scale(self.image, (int(self.size_x), int(self.size_y)))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

    def draw_resources_panel(self, resources_info, main_panel):
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))
        pos_x = 0
        for (resource, info) in resources_info.iteritems():
            image = self.resources[resource].image
            self.game_screen.blit(image, (pos_x, self.pos_y))
            text_size = main_panel.mes("{}: {} ".format(resource, info), GREEN,
                                       pos_x + image.get_size()[0] + RESOURCES_SPACE, self.pos_y)
            pos_x += text_size[0] + image.get_size()[0] + RESOURCES_SPACE

    def add_resources_to_resources_panel(self, resources_info):
        for (i, resource) in enumerate(resources_info):
            resource_sprite = Resource(resource["name"], resource["texturePath"], self.game_screen.get_size())
            self.resources[resource["name"]] = resource_sprite
