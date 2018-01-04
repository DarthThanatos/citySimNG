"""
    This module contains dictionary mapping resource name to resource object
    and functions facilitating operations on resources.
"""
from MapView.Items.Resource import Resource
from MapView.Utils import calculate_text_size, draw_text
from MapView.Consts import YELLOW, RESOURCES_SPACE, FONT_SIZE

resources = dict()


def parse_resources_data(resources_data):
    """ Create dictionary mapping resource name to dictionary with information
    about resource.

    :param resources_data: list of resources objects
    """
    for resource in resources_data:
        resources[resource.getName()] = {
            'texture_path': resource.getTexturePath(),
            'predecessor': resource.getPredecessor(),
            'successor': resource.getSuccessor()
        }


def draw_items_info(items_info, start_x, start_y, max_x, container,
                    items_sprites=None, items_sprites_group=None,
                    image_width=0, image_height=0, color=YELLOW,
                    space=RESOURCES_SPACE, font_size=FONT_SIZE):
    """ Draw item info with wrapping so that it does not exceed given x value.
    For each item this function draw first image and then value.

    :param items_info: dictionary mapping item name to its value
    :param start_x: initial x position
    :param start_y: initial y position
    :param max_x: x value that info should not exceed
    :param container: container in which info will be drawn
    :param items_sprites: list containing items sprites
    :param items_sprites_group: group of sprites to which add sprites
    :param image_width: item image width
    :param image_height: item image height
    :return: y position of line under drawn info
    """
    curr_x, curr_y = start_x, start_y
    text_size = (0, 0)

    for (item_name, value) in items_info.iteritems():
        if items_sprites:
            item_sprite = items_sprites[item_name]
        else:
            item_sprite = Resource(item_name,
                                   resources[item_name]['texture_path'],
                                   image_width, image_height)

        # skip if value is 0
        if value == 0:
            continue

        # calculate text size for current resource
        text_size = calculate_text_size("{}".format(items_info[item_name]),
                                        FONT_SIZE)
        info_width = item_sprite.image.get_size()[0] + text_size[0]

        if info_width + curr_x > max_x:
            curr_x = start_x
            curr_y += max(text_size[1], image_height)

        # update sprite rect
        if items_sprites:
            item_sprite.rect = item_sprite.image.get_rect(
                topleft=(curr_x + container.rect.left,
                         curr_y + container.rect.top))
            items_sprites_group.add(item_sprite)

        container.surface.blit(item_sprite.image, (curr_x, curr_y))
        draw_text(curr_x + item_sprite.image.get_size()[0] + space/2, curr_y,
                  '{}'.format(items_info[item_name]), color,
                  container.surface, FONT_SIZE)

        curr_x += info_width + 3/2 * space

    if curr_x == start_x and curr_y == start_y:
        text_size = draw_text(curr_x, curr_y, '-', color, container.surface)

    return curr_x + space, curr_y + max(text_size[1], image_height)


