class MapTile:
    def __init__(self, game_screen, all_sprites, buildings_sprites):
        self.left = None
        self.up = None
        self.right = None
        self.down = None
        self.game_screen = game_screen
        self.all_sprites = all_sprites
        self.buildings_sprites = buildings_sprites
