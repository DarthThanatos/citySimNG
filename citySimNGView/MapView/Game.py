import uuid

import pygame
from Converter import Converter
from CreatorView.RelativePaths import relative_textures_path

from Consts import (LEFT, RIGHT, RED, RESOURCES_PANEL_SIZE, BUILDINGS_PANEL_SIZE, NAVIGATION_PANEL_HEIGHT,
                    NAVIGATION_PANEL_WIDTH, TEXT_PANEL_HEIGHT, GREEN, INFO_PANEL_WIDTH, INFO_PANEL_HEIGHT)
from GameThread import GameThread
from Items.GameBuilding import GameBuilding
from Items.Resources import parse_resources_data
from Items.Dwellers import parse_dwellers_data
from MapTile import MapTile
from Panels.BuildingsPanel import BuildingsPanel
from Panels.InfoPanel import InfoPanel
from Panels.NavigationPanel import NavigationPanel
from Panels.ResourcesPanel import ResourcesPanel
from Popups.Popup import Popup
import time


POPUP_WIDTH, POPUP_HEIGHT = 0.2, 0.1


class Game(object):
    """ This class represents an instance of the game. If we need to restart the game we'd just
    need to create a new instance of this class. """
    def __init__(self, width, height, texture_one, texture_two, domestic_buildings_data,
                 industrial_buildings_data, resources_data, dwellers_data,
                 initial_resources_values, initial_resources_incomes,
                 initial_resources_consumption, initial_resources_balance, map_view,
                 available_dwellers):
        """ Constructor. Initialize the game.

        :param width: board width
        :param height: board height
        :param texture_one: texture for map tile pattern 1
        :param texture_two: texture for map tile patter 2
        :param buildings_data: information about buildings available in game
        :param resources_data: information about resources available in game and their starting amount
        """

        # connector with model
        self.map_view = map_view

        # Game board size
        self.board_width = width
        self.board_height = height

        # Create background and game_board
        self.set_display_mode()

        # Set position on map to (0, 0)
        self.map_position_x = 0
        self.map_position_y = 0

        # Create dictionary map position to map tile
        self.tiles = dict()

        # Create sprites groups for new tile
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.panels_sprites = pygame.sprite.Group()
        self.buildings_sprites = pygame.sprite.Group()

        # textures for map tiles
        self.texture_one = texture_one
        self.texture_two = texture_two

        # set texture for first map tile
        self.image = self.choose_map_tile_texture()
        self.image = pygame.transform.scale(self.image, (self.board_width, self.board_height))
        self.game_board = self.image

        # set current player position on map to tile (0,0)
        self.current_tile = MapTile(pygame.Surface.copy(self.game_board), self.game_board, self.all_sprites,
                                    self.buildings_sprites)
        self.tiles["{}:{}".format(self.map_position_x, self.map_position_y)] = self.current_tile

        # parse resources and dwellers data
        parse_resources_data(resources_data)
        parse_dwellers_data(dwellers_data)

        # Initialize game panels
        initial_resources_values = Converter().convertJavaMapToDict(initial_resources_values)
        initial_resources_incomes = Converter().convertJavaMapToDict(initial_resources_incomes)
        initial_resources_consumption = Converter().convertJavaMapToDict(initial_resources_consumption)
        initial_resources_balance = Converter().convertJavaMapToDict(initial_resources_balance)

        self.init_panels(domestic_buildings_data, industrial_buildings_data,
                         initial_resources_values, initial_resources_incomes,
                         initial_resources_consumption, initial_resources_balance,
                         resources_data, available_dwellers)

        # # TODO: probably should get this from model
        self.resources_panel.curr_dwellers_amount = 0

        # initialize variables needed to process events
        self.shadow = None
        self.selected_building = None
        self.clicked_button = None

        self.time = 0
        self.popup = None

        # start new thread that will be responsible for running game
        self.game_on = True
        self.listener_thread = GameThread(self)
        self.listener_thread.start()

    def set_display_mode(self):
        self.background = pygame.display.set_mode((self.board_width, self.board_height))

    def process_events(self):
        """ Process all of the events. """

        for event in pygame.event.get():
            mouse_pos = pygame.mouse.get_pos()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:

                # player has selected building and tries to place it
                if self.shadow is not None:
                    self.shadow.rect.center = mouse_pos
                    self.place_building(self.shadow, self.shadow.rect.left, self.shadow.rect.top)
                    self.shadow = None
                    break

                # player clicked on building in buildings panel ->
                # check if he can afford for it if yes start displaying shadow if no print appropriate info
                clicked_buildings = [b for b in self.buildings_panel.buildings_sprites
                                     if b.rect.collidepoint(mouse_pos)]
                if clicked_buildings:
                    building = clicked_buildings[0]
                    if self.map_view.check_if_can_afford(building) and building.is_enabled:
                        self.shadow = GameBuilding(building.name,
                                                   uuid.uuid4().__str__(),
                                                   building.texture_path,
                                                   building.type,
                                                   building.resources_cost,
                                                   building.consumes,
                                                   building.produces,
                                                   building.required_dwellers,
                                                   building.dwellers_name,
                                                   mouse_pos[0],
                                                   mouse_pos[1],
                                                   building.width,
                                                   building.height)
                    elif not building.is_enabled:
                        self.map_view.log.AppendText(
                            "You have to built all successor first\n")
                    else:
                        self.map_view.log.AppendText(
                            "You don't have enough resources to build {}\n".format(building.name))

                # TODO: find better way to deal with button texture change
                # player clicked on building in map ->
                # display information about building in info panel
                clicked_buildings = [b for b in self.buildings_sprites if b.rect.collidepoint(mouse_pos)]
                if clicked_buildings:
                    self.info_panel.curr_building = clicked_buildings[0]
                    self.set_working_dwellers_for_building(clicked_buildings[0])
                    self.info_panel.prepare_dwellers_info()
                    self.info_panel.create_sprites_for_current_building()
                    self.info_panel.set_stop_production_button_texture()

                clicked_info_panel_buttons = [b for b in self.info_panel.buttons_sprites if
                                              b.rect.collidepoint(mouse_pos)]
                if clicked_info_panel_buttons:

                    # player clicked delete building button in info panel ->
                    # delete current selected building
                    if self.info_panel.del_building_button is not None and \
                            clicked_info_panel_buttons[0] == self.info_panel.del_building_button:
                        self.clicked_button = self.info_panel.del_building_button
                        self.clicked_button.click_button(self.info_panel.curr_building)

                    # player clicked stop production button in info panel ->
                    # stop production in current selected building
                    if self.info_panel.stop_production_button is not None and \
                            clicked_info_panel_buttons[0] == self.info_panel.stop_production_button:
                        self.clicked_button = self.info_panel.stop_production_button
                        self.clicked_button.click_button(self.info_panel.curr_building.id)

                # player clicked arrow in buildings panel ->
                # scroll building panel
                if self.buildings_panel.left_arrow.rect.collidepoint(mouse_pos):
                    self.clicked_button = self.buildings_panel.left_arrow
                    self.clicked_button.click_button()
                if self.buildings_panel.right_arrow.rect.collidepoint(mouse_pos):
                    self.clicked_button = self.buildings_panel.right_arrow
                    self.clicked_button.click_button()

                # player clicked arrow in resources panel ->
                # scroll resources panel
                if self.resources_panel.left_arrow.rect.collidepoint(mouse_pos):
                    self.clicked_button = self.resources_panel.left_arrow
                    self.clicked_button.click_button()
                if self.resources_panel.right_arrow.rect.collidepoint(mouse_pos):
                    self.clicked_button = self.resources_panel.right_arrow
                    self.clicked_button.click_button()

                # player clicked navigation arrow in navigation panel ->
                # go to new map tile
                clicked_nav_arrows = [na for na in self.navigation_panel.navigation_arrows_sprites if
                                      na.rect.collidepoint(mouse_pos)]
                if clicked_nav_arrows:
                    self.clicked_button = clicked_nav_arrows[0]
                    self.clicked_button.click_button(clicked_nav_arrows[0])

            # user released left mouse button
            if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                if self.clicked_button is not None:
                    self.clicked_button.release_button()
                    self.clicked_button = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                if self.shadow is not None:
                    self.shadow = None

            if event.type == pygame.MOUSEMOTION:
                sprites = [s for s in self.all_sprites.sprites() if s.rect.collidepoint(mouse_pos)]
                if sprites:
                    # get the sprite that was last added to all_sprites
                    sprite = sprites[-1]
                    try:
                        inner_sprites = [s for s in sprite.all_sprites.sprites() if s.rect.collidepoint(mouse_pos)]
                    except AttributeError:
                        pass
                    else:
                        if inner_sprites:
                            print inner_sprites
                            sprite = inner_sprites[-1]

                    if not self.popup or sprite != self.popup.sprite:
                        if sprite in self.buildings_panel.buildings_sprites:
                            self.popup = sprite.popup
                        else:
                            self.popup = Popup(mouse_pos[0], mouse_pos[1] + pygame.mouse.get_cursor()[0][1],
                                               sprite, POPUP_WIDTH * self.board_width, POPUP_HEIGHT * self.board_height,
                                               self.game_board)
                    elif self.popup and sprite == self.popup.sprite and sprite not in self.buildings_panel.buildings_sprites:
                        self.popup.pos_x, self.popup.pos_y = mouse_pos[0], mouse_pos[1] + pygame.mouse.get_cursor()[0][1]
                        self.popup.timer = time.time()
                else:
                    self.popup = None

    def update(self):
        """ Update all elements before they will be drawn. """
        mouse_pos = pygame.mouse.get_pos()

        if self.shadow is not None:
            self.shadow.rect.center = pygame.mouse.get_pos()
            if self.is_building_position_valid(self.shadow):
                self.shadow.image.fill(GREEN)
            else:
                self.shadow.image.fill(RED)

        if self.popup and self.popup.sprite not in self.buildings_panel.buildings_sprites:
            self.popup.pos_x, self.popup.pos_y = mouse_pos[0], mouse_pos[1] + pygame.mouse.get_cursor()[0][1]
            self.popup.rect = self.popup.surface.get_rect(midtop=(self.popup.pos_x, self.popup.pos_y))

    def display_frame(self):
        """ In this function all elements are drawn. """
        self.game_board.blit(self.current_tile.image, (0, 0))

        for panel in self.panels_sprites:
            panel.draw()

        for building in self.buildings_sprites:
            building.draw(self.game_board, building.pos_x, building.pos_y)

        if self.popup and self.shadow is None:
            self.popup.draw()

        # draw building's shadow
        if self.shadow is not None:
            self.game_board.blit(self.shadow.image, (self.shadow.rect.left, self.shadow.rect.top))

        # draw game board
        self.background.blit(self.game_board, (0, 0))

    def init_panels(self, domestic_buildings_data, industrial_buildings_data,
                    initial_resources_values, initial_resources_incomes,
                    initial_resources_consumption, initial_resources_balance,
                    resources_data, available_dwellers):
        """ Create and initialize all game panels. Add panels to appropriate sprite group.

        :param buildings_data: information about buildings available in game
        :param initial_resources_values: initial values for all resources
        :param initial_resources_incomes: initial incomes for all resources
        :param resources_data: list of dictionaries. Each dictionary contains following information about resource:
        name, texture path, predecessor and successor.
        """
        # Create resources panel
        self.resources_panel = ResourcesPanel(0, 0, self.board_width - BUILDINGS_PANEL_SIZE * self.board_width,
                                              RESOURCES_PANEL_SIZE * self.board_height, self.game_board,
                                              initial_resources_values, initial_resources_incomes,
                                              initial_resources_consumption, initial_resources_balance, resources_data,
                                              available_dwellers)
        self.panels_sprites.add(self.resources_panel)
        self.all_sprites.add(self.resources_panel)

        # Create buildings panel
        self.buildings_panel = BuildingsPanel(
            self.board_width - BUILDINGS_PANEL_SIZE * self.board_width,
            0,
            BUILDINGS_PANEL_SIZE * self.board_width,
            self.board_height - TEXT_PANEL_HEIGHT * self.board_height,
            self.game_board,
            domestic_buildings_data,
            industrial_buildings_data,
            self.resources_panel.pos_y,
            self.resources_panel.height)

        self.panels_sprites.add(self.buildings_panel)
        self.all_sprites.add(self.buildings_panel)

        # Create navigation panel
        self.navigation_panel = NavigationPanel(0, self.board_height - NAVIGATION_PANEL_HEIGHT * self.board_height,
                                                NAVIGATION_PANEL_WIDTH * self.board_width,
                                                NAVIGATION_PANEL_HEIGHT * self.board_height, self.game_board,
                                                self.switch_game_tile)
        self.panels_sprites.add(self.navigation_panel)
        self.all_sprites.add(self.navigation_panel)

        # Create info panel
        self.info_panel = InfoPanel(NAVIGATION_PANEL_WIDTH * self.board_width,
                                    self.board_height - INFO_PANEL_HEIGHT * self.board_height,
                                    INFO_PANEL_WIDTH * self.board_width, INFO_PANEL_HEIGHT * self.board_height,
                                    self.game_board, self.delete_building, self.map_view.stop_production)
        self.panels_sprites.add(self.info_panel)
        self.all_sprites.add(self.info_panel)

    def choose_map_tile_texture(self):
        """ Function choosing texture for current map tile.

        :return: image for current map tile
        """
        if (abs(self.map_position_x) + abs(self.map_position_y)) % 2 == 0:
            return pygame.image.load(relative_textures_path + self.texture_one)
        else:
            return pygame.image.load(relative_textures_path + self.texture_two)

    # TODO: should log panel be in map view??
    def is_building_position_valid(self, building, with_info=False):
        """ Function checking if position of building is valid.

        :param building: building whose position will be checked
        :param with_info: tells if info about wrong position should be printed in log panel
        :return: True if building position is valid and False if it is not
        """
        if not self.game_board.get_rect().contains(building):
            if with_info:
                self.map_view.log.AppendText("Can't place {} here - building has to be inside "
                                             "game screen.\n".format(building.name))
            return False
        for b in self.all_sprites.sprites():
            if pygame.sprite.collide_rect(b, building):
                if with_info:
                    self.map_view.log.AppendText("Can't place {} here - there is another building or game panel "
                                                 "in that place.\n".format(building.name))
                return False
        return True

    def place_building(self, building, pos_x, pos_y):
        """ Function placing building. It checks all requirements. After placing building appropriate message is sent
         to model.

        :param building: sprite of building that will be placed
        :param pos_x: x position of new building
        :param pos_y: y position of new building
        """
        # check if player can afford to place this building
        if not self.map_view.check_if_can_afford(self.shadow):
            return

        # update building's position and image
        building.pos_x = pos_x
        building.pos_y = pos_y
        building.load_texture()

        # check if building's position is valid
        if not self.is_building_position_valid(building, True):
            return

        self.buildings_sprites.add(building)
        self.all_sprites.add(building)
        self.map_view.erected_building(building)
        self.info_panel.curr_building = building
        self.info_panel.create_sprites_for_current_building()
        self.info_panel.prepare_dwellers_info()

    def switch_game_tile(self, nav_arrow):
        """ Function changing position on map. It saves sprites for current location. Then, if player is first time
        in given location it creates new map tile, otherwise it loads appropriate map tile and sprites.
        Then it updates position in navigation panel.

        :param nav_arrow: navigation arrow that has been clicked
        """
        # save sprites for current position
        self.current_tile.buildings_sprites = self.buildings_sprites
        self.current_tile.all_sprites = self.all_sprites

        # change current position
        if self.navigation_panel.arrow_direction[nav_arrow.texture_rotation] == "Left":
            self.map_position_x -= 1
        if self.navigation_panel.arrow_direction[nav_arrow.texture_rotation] == "Right":
            self.map_position_x += 1
        if self.navigation_panel.arrow_direction[nav_arrow.texture_rotation] == "Up":
            self.map_position_y += 1
        if self.navigation_panel.arrow_direction[nav_arrow.texture_rotation] == "Down":
            self.map_position_y -= 1

        # if we are first time in given location create new MapTile
        if not "{}:{}".format(self.map_position_x, self.map_position_y) in self.tiles:
            image = self.choose_map_tile_texture()
            image = pygame.transform.scale(image, (self.board_width, self.board_height))
            map_tile = MapTile(pygame.Surface.copy(image), image, pygame.sprite.Group(), pygame.sprite.Group())
            self.tiles["{}:{}".format(self.map_position_x, self.map_position_y)] = map_tile

        # otherwise just get game_board of new position
        else:
            map_tile = self.tiles["{}:{}".format(self.map_position_x, self.map_position_y)]

        # set current tile
        self.current_tile = map_tile

        # set buildings and all sprites
        self.buildings_sprites = self.current_tile.buildings_sprites
        self.all_sprites = self.current_tile.all_sprites

        # update map position in navigation panel
        self.navigation_panel.map_position_x = self.map_position_x
        self.navigation_panel.map_position_y = self.map_position_y

        # set panel's game_screen, draw panels, add panels to sprites
        for panel in self.panels_sprites:
            self.all_sprites.add(panel)

    def delete_building(self, building):
        """ Delete building. Remove it from sprites groups and redraw game board.

        :param building: building that will be deleted
        """
        building.kill()
        self.info_panel.curr_building = None
        self.info_panel.buttons_sprites = pygame.sprite.Group()
        self.map_view.deleted_building(building.id)

    def set_working_dwellers_for_building(self, building):
        self.map_view.set_dwellers_working_in_building(building.id)
