import pygame
from RelativePaths import relative_textures_path
from Utils import calculate_text_size, draw_text
from Consts import GREEN, RESOURCES_SPACE

DEFAULT_RESOURCE_TEXTURE = relative_textures_path + "DefaultBuilding.jpg"
RESOURCE_SIZE = 0.03
WHITE = (255, 255, 255)


class Resource(pygame.sprite.Sprite):
    def __init__(self, name, texture_path, game_screen_size):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.texture_path = texture_path
        self.game_screen_size = game_screen_size

        # TODO: THIS IS WRONG...
        width, height = self.game_screen_size
        self.width, self.height = int(width * RESOURCE_SIZE), int(height * RESOURCE_SIZE)
        try:
            self.image = pygame.image.load(self.texture_path)
        except Exception:
            self.texture_path = DEFAULT_RESOURCE_TEXTURE
            self.image = pygame.image.load(self.texture_path)
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (int(width * RESOURCE_SIZE),
                                                         int(height * RESOURCE_SIZE)))


class Resources:
    def __init__(self, resources_info, game_screen):
        self.resources = {}
        self.game_screen = game_screen
        for resource in resources_info:
            resource_sprite = Resource(resource["name"], resource["texturePath"], game_screen.get_size())
            self.resources[resource["name"]] = resource_sprite

    def draw_resources_info(self, resources_info, pos_x, pos_y, max_x, mes, game_screen=None):
        """

        :param resources_info: dictionary resource: value
        :param pos_x: start value for x coordinate
        :param pos_y: start value for y coordinate
        :param max_x: max value for x coordinate
        :param mes: message that will be printed before resources info
        :param game_screen: game screen on which draw info
        :return: y coordinate of first line below info
        """
        if game_screen is None:
            game_screen = self.game_screen

        text_size = (0, 0)
        mes_width, mes_height = draw_text(pos_x, pos_y, mes, GREEN, game_screen)
        curr_x = pos_x + mes_width + RESOURCES_SPACE
        for (resource, value) in resources_info.iteritems():
            # TODO: we have to take care of this in logic
            if value == 0:
                continue

            # get image for current resource
            image = self.resources[resource].image

            # calculate text size for current resource
            text_size = calculate_text_size("{}".format(resources_info[resource]))
            info_width = image.get_size()[0] + text_size[0]

            if info_width + curr_x > max_x:
                curr_x = pos_x
                pos_y += text_size[1]

            game_screen.blit(image, (curr_x, pos_y))
            draw_text(curr_x + image.get_size()[0] + RESOURCES_SPACE, pos_y,
                      "{}".format(resources_info[resource]), GREEN, game_screen)
            curr_x += info_width + RESOURCES_SPACE
        return pos_y + text_size[1]
