from MapView.Consts import GREEN, RESOURCES_SPACE, FONT_SIZE
from MapView.Utils import calculate_text_size, draw_text

from MapView.Items.Dweller import Dweller

dwellers = dict()


def parse_dwellers_data(dwellers_data):
    """ Create dictionary mapping dweller name to dictionary with information about dweller.

    :param dwellers_data: list of dwellers objects
    """
    for dweller in dwellers_data:
        dwellers[dweller.getName()] = {
            'texture_path': dweller.getTexturePath(),
            'predecessor': dweller.getPredecessor(),
            'successor': dweller.getSuccessor()
        }


def draw_dwellers_info(dwellers_name, dwellers_info, start_x, start_y,
                       container, dweller_sprite=None, image_width=0,
                       image_height=0, color=GREEN, font_size=FONT_SIZE):
    curr_x, curr_y = start_x, start_y

    if not dweller_sprite:
        dweller_sprite = Dweller(dwellers_name,
                                 dwellers[dwellers_name]['texture_path'],
                                 image_width, image_height)

    text_size = calculate_text_size("{}".format(dwellers_info), FONT_SIZE)

    # update sprite rect
    dweller_sprite.rect = dweller_sprite.image.get_rect(topleft=(
        curr_x + container.rect.left, curr_y + container.rect.top))

    container.surface.blit(dweller_sprite.image, (start_x, start_y))
    draw_text(start_x + dweller_sprite.image.get_size()[0] + RESOURCES_SPACE/2,
              start_y, '{}'.format(dwellers_info), color, container.surface,
              FONT_SIZE)

    return start_y + max(text_size[1], image_height)
