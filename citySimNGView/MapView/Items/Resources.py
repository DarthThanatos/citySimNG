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
    """ Create dictionary mapping resource name to dictionary with information about resource.

    :param resources_data: list of resources objects
    """
    for resource in resources_data:
        resources[resource.getName()] = {
            'texture_path': resource.getTexturePath(),
            'predecessor': resource.getPredecessor(),
            'successor': resource.getSuccessor()
        }


def draw_resources_info(resources_info, start_x, start_y, max_x, container, resources_sprites=None,
                        resources_sprites_group=None, image_width=0, image_height=0):
    """ Draw resources info with wrapping so that it does not exceed given x value.
    For each resource this function draw first image and then value.

    :param resources_info: dictionary mapping resource name to its value
    :param start_x: initial x position
    :param start_y: initial y position
    :param max_x: x value that info should not exceed
    :param container: container in which info will be drawn
    :param resources_sprites: list containing resources sprites
    :param resources_sprites_group: group of sprites to which add sprites
    :param image_width: resource image width
    :param image_height: resource image height
    :return: y position of line under drawn info
    """
    curr_x, curr_y = start_x, start_y
    text_size = (0, 0)

    for (resource, value) in resources_info.iteritems():
        if resources_sprites:
            resource_sprite = resources_sprites[resource]
        else:
            resource_sprite = Resource(resource, resources[resource]['texture_path'], image_width, image_height)

        # skip if value is 0
        # TODO: we have to take care of this in logic
        if value == 0:
            continue

        # calculate text size for current resource
        text_size = calculate_text_size("{}".format(resources_info[resource]))
        info_width = resource_sprite.image.get_size()[0] + text_size[0]

        if info_width + curr_x > max_x:
            curr_x = start_x
            curr_y += text_size[1]

        # update sprite rect
        if resources_sprites:
            resource_sprite.rect = resource_sprite.image.get_rect(topleft=(curr_x + container.rect.left,
                                                                           curr_y + container.rect.top))
            resources_sprites_group.add(resource_sprite)

        container.surface.blit(resource_sprite.image, (curr_x, curr_y))
        draw_text(curr_x + resource_sprite.image.get_size()[0], curr_y, '{}'.format(resources_info[resource]), GREEN,
                  container.surface)

        curr_x += info_width + RESOURCES_SPACE

    if curr_x == start_x and curr_y == start_y:
        text_size = draw_text(curr_x, curr_y, '-', GREEN, container.surface)

    return curr_y + text_size[1]
