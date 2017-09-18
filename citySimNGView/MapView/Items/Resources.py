"""
    This module contains dictionary mapping resource name to resource object and functions facilitating operations
    on resources.
"""
from MapView.Items.Resource import Resource
from MapView.Utils import calculate_text_size, draw_text
from MapView.Consts import GREEN, RESOURCES_SPACE
import pygame

resources = dict()


def parse_resources_data(resources_data):
    """ Parse information about resources available in game sent by model.

    :param resources_data: list of dictionaries. Each dictionary contains following information about resource:
    name, texture path, predecessor and successor.
    """
    for resource in resources_data:
        resource_sprite = Resource(resource.getName(), resource.getTexturePath())
        resources[resource.getName()] = resource_sprite


def draw_resources_info(resources_info, start_x, start_y, max_x, surface, image_width, image_height):
    """ Draw resources info with wrapping so that it does not exceed given x value.
    For each resource this function draw first image and then value.

    :param resources_info: dictionary mapping resource name to its value
    :param start_x: initial x position
    :param start_y: initial y position
    :param max_x: x value that info should not exceed
    :param surface: surface on which info should be drawn
    :param image_width:
    :param image_height:
    :return:
    """
    curr_x, curr_y = start_x, start_y
    text_size = (0, 0)

    for (resource, value) in resources_info.iteritems():

        # skip if value is 0
        # TODO: we have to take care of this in logic
        if value == 0:
            continue

        # get image for current resource and scale it
        image = resources[resource].image
        image = pygame.transform.scale(image, (image_width, image_height))

        # calculate text size for current resource
        text_size = calculate_text_size("{}".format(resources_info[resource]))
        info_width = image.get_size()[0] + text_size[0]

        if info_width + curr_x > max_x:
            curr_x = start_x
            curr_y += text_size[1]

        surface.blit(image, (curr_x, curr_y))
        draw_text(curr_x + image.get_size()[0], curr_y, '{}'.format(resources_info[resource]), GREEN, surface)
        curr_x += info_width + RESOURCES_SPACE

    return curr_y + text_size[1]
