import uuid
import pygame
from RelativePaths import relative_textures_path
from Building import Building

FONT = "Comic Sans MS"
FPS = 60
LEFT = 1
RIGHT = 3
RED = (150, 0, 0)
GREEN = (0, 150, 0)
YELLOW = (200, 200, 0)
PURPLE = (200, 0, 200)
WHITE = (255, 255, 255)

RESOURCES_PANEL_SIZE = 0.2
BUILDINGS_PANEL_SIZE = 0.15
ARROW_BUTTON_WIDTH = 0.3
RIGHT_ARROW_BUTTON_X = 0.6
LEFT_ARROW_BUTTON_X = 0.1
ARROW_BUTTON_HEIGHT = 0.1
ARROW_BUTTON_Y = 0.7
BUILDING_SIZE = 0.05
RESOURCE_SIZE = 0.03
SPACE = 20
RESOURCES_SPACE = 10


DEFAULT_BUILDING_TEXTURE = relative_textures_path + "DefaultBuilding.jpg"


class BuildingsPanel(pygame.sprite.Sprite):
    def __init__(self, game_screen, main_panel, pos_x, pos_y, size_x, size_y):
        pygame.sprite.Sprite.__init__(self)
        self.game_screen = game_screen
        self.main_panel = main_panel
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.rect = None
        self.buildings_info = None
        self.page = 1
        self.page_buildings = {}
        self.last_page = 1

    def draw_buildings_panel(self):
        image = pygame.image.load(relative_textures_path + 'BuildingsPanelTexture.jpg')
        image = pygame.transform.scale(image, (int(self.size_x), int(self.size_y)))
        self.rect = image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.game_screen.blit(image, (self.pos_x, self.pos_y))

        image = pygame.image.load(relative_textures_path + 'RightArrow.png')
        image = pygame.transform.scale(image, (int(ARROW_BUTTON_WIDTH * self.size_x),
                                               int(ARROW_BUTTON_HEIGHT * self.size_y)))
        right_arrow_rect = image.get_rect(topleft=(self.pos_x + RIGHT_ARROW_BUTTON_X * self.size_x,
                                          ARROW_BUTTON_Y * self.size_y))
        self.game_screen.blit(image, (self.pos_x + RIGHT_ARROW_BUTTON_X * self.size_x,
                                      ARROW_BUTTON_Y * self.size_y))
        self.main_panel.right_arrow_buildings_panel = right_arrow_rect

        image = pygame.image.load(relative_textures_path + 'LeftArrow.png')
        image = pygame.transform.scale(image, (int(ARROW_BUTTON_WIDTH * self.size_x),
                                               int(ARROW_BUTTON_HEIGHT * self.size_y)))
        left_arrow_rect = image.get_rect(topleft=(self.pos_x + LEFT_ARROW_BUTTON_X * self.size_x,
                                         ARROW_BUTTON_Y * self.size_y))
        self.game_screen.blit(image, (self.pos_x + LEFT_ARROW_BUTTON_X * self.size_x,
                                      ARROW_BUTTON_Y * self.size_y))
        self.main_panel.left_arrow_buildings_panel = left_arrow_rect

    def add_buildings_to_buildings_panel(self, buildings_info):
            width, height = self.game_screen.get_size()
            pos = 0
            for building in buildings_info:
                if (BUILDING_SIZE * height) * (pos / 2 + 1) + SPACE * (pos / 2) > ARROW_BUTTON_Y * self.size_y:
                    self.page += 1
                    pos = 0
                    self.last_page = self.page
                resource_cost_string = ""
                for (resource, value) in building["resourcesCost"].iteritems():
                    resource_cost_string += "{}: {} ; ".format(resource, value)
                building_sprite = Building(building["name"], uuid.uuid4().__str__(), resource_cost_string,
                                           building["texturePath"], self.game_screen,
                                           pos=(self.pos_x + BUILDING_SIZE * width * (pos % 2) + (pos % 2 + 1) * SPACE,
                                                BUILDING_SIZE * height * (pos / 2) + SPACE * (pos / 2)))
                if str(self.page) in self.page_buildings:
                    self.page_buildings[str(self.page)].append(building_sprite)
                else:
                    self.page_buildings[str(self.page)] = [building_sprite]
                pos += 1
            self.page = 1
            self.draw()

    def draw(self):
        self.main_panel.buildings_panel_sprites = pygame.sprite.Group()
        for building in self.page_buildings[str(self.page)]:
            self.game_screen.blit(building.image, (building.pos[0], building.pos[1]))
            self.main_panel.buildings_panel_sprites.add(building)

    def scroll_building_panel_right(self):
        if self.page < self.last_page:
            self.page += 1
            self.draw_buildings_panel()
            self.draw()

    def scroll_building_panel_left(self):
        if self.page > 1:
            self.page -= 1
            self.draw_buildings_panel()
            self.draw()
