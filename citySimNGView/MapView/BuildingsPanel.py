import uuid
import pygame
from RelativePaths import relative_textures_path
from Building import Building
from Consts import BUILDINGS_PANEL_TEXTURE, ARROW_BUTTON_WIDTH, ARROW_BUTTON_HEIGHT, BUILDINGS_PANEL_RIGHT_ARROW_X, \
    BUILDINGS_PANEL_ARROW_Y, BUILDINGS_PANEL_LEFT_ARROW_X, BUILDING_SIZE, SPACE


class BuildingsPanel(pygame.sprite.Sprite):
    def __init__(self, game_screen, main_panel, pos_x, pos_y, size_x, size_y):
        pygame.sprite.Sprite.__init__(self)
        self.game_screen = game_screen
        self.main_panel = main_panel
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.buildings_info = None
        self.page = 1
        self.page_buildings = {}
        self.last_page = 1

        self.image = pygame.image.load(BUILDINGS_PANEL_TEXTURE)
        self.image = pygame.transform.scale(self.image, (int(self.size_x), int(self.size_y)))
        self.rect = self.image.get_rect(topleft=(self.pos_x, self.pos_y))

        self.right_arrow_image = pygame.image.load(relative_textures_path + 'RightArrow.png')
        self.right_arrow_image = pygame.transform.scale(self.right_arrow_image, (int(ARROW_BUTTON_WIDTH * self.size_x),
                                                        int(ARROW_BUTTON_HEIGHT * self.size_y)))
        self.right_arrow_rect = self.right_arrow_image.get_rect(topleft=(self.pos_x + BUILDINGS_PANEL_RIGHT_ARROW_X * self.size_x,
                                                                         BUILDINGS_PANEL_ARROW_Y * self.size_y))

        self.left_arrow_image = pygame.image.load(relative_textures_path + 'LeftArrow.png')
        self.left_arrow_image = pygame.transform.scale(self.left_arrow_image, (int(ARROW_BUTTON_WIDTH * self.size_x),
                                                       int(ARROW_BUTTON_HEIGHT * self.size_y)))
        self.left_arrow_rect = self.left_arrow_image.get_rect(topleft=(self.pos_x + BUILDINGS_PANEL_LEFT_ARROW_X * self.size_x,
                                                              BUILDINGS_PANEL_ARROW_Y * self.size_y))

    def draw_buildings_panel(self):
        self.game_screen.blit(self.image, (self.pos_x, self.pos_y))

        self.game_screen.blit(self.right_arrow_image, (self.pos_x + BUILDINGS_PANEL_RIGHT_ARROW_X * self.size_x,
                                                       BUILDINGS_PANEL_ARROW_Y * self.size_y))
        self.main_panel.right_arrow_buildings_panel = self.right_arrow_rect

        self.game_screen.blit(self.left_arrow_image, (self.pos_x + BUILDINGS_PANEL_LEFT_ARROW_X * self.size_x,
                                                      BUILDINGS_PANEL_ARROW_Y * self.size_y))
        self.main_panel.left_arrow_buildings_panel = self.left_arrow_rect

    def add_buildings_to_buildings_panel(self, buildings_info):
            width, height = self.game_screen.get_size()
            building_no = 0
            for building in buildings_info:
                if (BUILDING_SIZE * height) * (building_no / 2 + 1) + SPACE * (building_no / 2) > BUILDINGS_PANEL_ARROW_Y * self.size_y:
                    self.page += 1
                    building_no = 0
                    self.last_page = self.page
                resource_cost_string = ""
                for (resource, value) in building["resourcesCost"].iteritems():
                    resource_cost_string += "{}: {} ; ".format(resource, value)
                building_sprite = Building(building["name"], uuid.uuid4().__str__(), resource_cost_string,
                                           building["texturePath"], (width, height),
                                           pos=(self.pos_x + BUILDING_SIZE * width * (building_no % 2) + (building_no % 2 + 1) * SPACE,
                                                BUILDING_SIZE * height * (building_no / 2) + SPACE * (building_no / 2)))
                if str(self.page) in self.page_buildings:
                    self.page_buildings[str(self.page)].append(building_sprite)
                else:
                    self.page_buildings[str(self.page)] = [building_sprite]
                building_no += 1
            self.page = 1
            self.draw_buildings_in_buildings_panel()

    def draw_buildings_in_buildings_panel(self):
        self.main_panel.buildings_panel_sprites = pygame.sprite.Group()
        for building in self.page_buildings[str(self.page)]:
            self.game_screen.blit(building.image, (building.pos[0], building.pos[1]))
            self.main_panel.buildings_panel_sprites.add(building)

    def scroll_building_panel_right(self):
        if self.page < self.last_page:
            self.page += 1
            self.draw_buildings_panel()
            self.draw_buildings_in_buildings_panel()

    def scroll_building_panel_left(self):
        if self.page > 1:
            self.page -= 1
            self.draw_buildings_panel()
            self.draw_buildings_in_buildings_panel()
