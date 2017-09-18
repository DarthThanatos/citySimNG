class MapTile:
    """ This class represents an instance of map tile. """
    def __init__(self, image, game_board, all_sprites, buildings_sprites):
        """ Constructor.

        :param image: map tile's empty image
        :param game_board: map tile's game board
        :param all_sprites: sprites located in given map tile
        :param buildings_sprites: buildings sprites located in given map tile
        """
        self.image = image
        self.game_board = game_board
        self.all_sprites = all_sprites
        self.buildings_sprites = buildings_sprites
