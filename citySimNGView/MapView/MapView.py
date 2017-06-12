import wx
import os
import threading
import json
import uuid
import pygame
import traceback
from Resource import Resources
from RelativePaths import relative_music_path, relative_textures_path
from ResourcesPanel import ResourcesPanel
from BuildingsPanel import BuildingsPanel
from InfoPanel import InfoPanel
from Building import Building
from Consts import BUILDINGS_PANEL_SIZE, RESOURCES_PANEL_SIZE, NAV_ARROW_HEIGHT, NAV_ARROW_WIDTH, FPS, GREEN, RED, \
    PURPLE, FONT, GRASS_TEXTURE, GRASS2_TEXTURE, NAV_ARROW_TEXTURE, FONT_SIZE, TEXT_PANEL_HEIGHT, \
    TEXT_PANEL_WIDTH, MENU_BUTTON_WIDTH, NAVIGATION_PANEL_HEIGHT, NAVIGATION_PANEL_WIDTH, INFO_PANEL_HEIGHT, INFO_PANEL_WIDTH, TEXT_PANEL_FONT_SIZE
from NavigationArrow import NavigationArrow
from UserEventHandlerThread import UserEventHandlerThread
from MapTile import MapTile
import math
from NavigationPanel import NavigationPanel
from Utils import draw_text, draw_text_with_wrapping


class MapView(wx.Panel):
    current_tile = None
    map_tiles = {}
    map_position = (0, 0)

    background = None
    game_screen = None

    resources_panel = None
    buildings_panel = None

    listener_thread = None

    buildings_sprites = pygame.sprite.Group()
    buildings_panel_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    navigation_arrows_sprites = pygame.sprite.Group()
    right_arrow_buildings_panel = None
    left_arrow_buildings_panel = None

    game_on = True
    has_reply_arrived = False
    can_afford_on_building = False
    last_res_info = None

    image = None

    condition = threading.Condition()

    def __init__(self, parent, size, name, sender, music_path=relative_music_path + "TwoMandolins.mp3"):
        # call base class constructor
        wx.Panel.__init__(self, parent=parent, size=size)

        # set class fields
        self.parent = parent
        self.width = size[0]
        self.height = size[1]
        self.screen_height = size[1]
        self.name = name
        self.sender = sender
        self.music_path = music_path

        # bind EVT_SHOW to onShow() function
        self.Bind(wx.EVT_SHOW, self.on_show, self)

        # add buttons
        self.init_buttons()

        style = wx.TE_MULTILINE | wx.TE_READONLY
        self.log = wx.TextCtrl(self, wx.ID_ANY, size=(size[0] * TEXT_PANEL_WIDTH, TEXT_PANEL_HEIGHT * size[1]),
                               style=style, pos=(self.width * NAVIGATION_PANEL_WIDTH + self.width * INFO_PANEL_WIDTH,
                                                 int(size[1] - TEXT_PANEL_HEIGHT * size[1])))
        font = wx.Font(TEXT_PANEL_FONT_SIZE, wx.MODERN, wx.NORMAL, wx.NORMAL, False, FONT)
        self.log.SetFont(font)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.sizer)

        self.del_button_sprite = None

    def init_buttons(self):
        """ Function adding buttons """
        menu_btn = wx.Button(self, label="Menu", pos=(self.width - MENU_BUTTON_WIDTH * self.width,
                                                      self.screen_height - self.screen_height * TEXT_PANEL_HEIGHT),
                             size=(MENU_BUTTON_WIDTH * self.width, self.screen_height * TEXT_PANEL_HEIGHT))
        self.Bind(wx.EVT_BUTTON, self.ret_to_menu, menu_btn)

    def on_show(self, event):
        if event.GetShow():
            print "shown map"
            self.init_view()
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(self.music_path)
                pygame.mixer.music.play()
            except Exception:
                print "Problem with music"
        else:
            try:
                pygame.quit()
            except Exception:
                print "first appearance of MapView: pygame not initialized in map"

    def init_view(self):
        print "Map: initview"
        global pygame
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame  # this has to happen after setting the environment variables.
        pygame.init()
        pygame.display.init()

        # Create background and game_screen
        self.background = pygame.display.set_mode((self.width, self.height))
        self.game_screen = pygame.Surface.copy(self.background)

        # Create resources panel and add it to all sprites
        self.resources_panel = ResourcesPanel(0, 0, self.width - BUILDINGS_PANEL_SIZE * self.width,
                                              RESOURCES_PANEL_SIZE * self.height, self, self.game_screen)
        self.all_sprites.add(self.resources_panel)

        # Create buildings panel and add it to all sprites
        self.buildings_panel = BuildingsPanel(self.width - BUILDINGS_PANEL_SIZE * self.width, 0,
                                              BUILDINGS_PANEL_SIZE * self.width,
                                              self.height - TEXT_PANEL_HEIGHT * self.height, self.game_screen, self)
        self.all_sprites.add(self.buildings_panel)

        # Create navigation panel and add it to all sprites
        self.navigation_panel = NavigationPanel(0, self.height - NAVIGATION_PANEL_HEIGHT * self.height,
                                                NAVIGATION_PANEL_WIDTH * self.width,
                                                NAVIGATION_PANEL_HEIGHT * self.height,
                                                self.game_screen, self.switch_game_tile)
        self.all_sprites.add(self.navigation_panel)

        # Create info panel and add it to all sprites
        self.info_panel = InfoPanel(NAVIGATION_PANEL_WIDTH * self.width, self.height - INFO_PANEL_HEIGHT * self.height,
                                    INFO_PANEL_WIDTH * self.width, INFO_PANEL_HEIGHT * self.height, self.game_screen,
                                    self.delete_building, self.stop_production)
        self.all_sprites.add(self.info_panel)

        # set current player position on map to tile (0,0)
        self.current_tile = MapTile(self.game_screen, self.all_sprites, self.buildings_sprites)
        self.map_tiles[str(self.map_position)] = self.current_tile

        # Add arrows to navigation panel
        self.navigation_arrows_sprites.add(self.navigation_panel.add_navigation_arrows())

        self.panels = [self.resources_panel, self.buildings_panel, self.navigation_panel, self.info_panel]

        # start new thread, that will be listening for player events
        self.game_on = True
        self.listener_thread = UserEventHandlerThread(self)
        self.listener_thread.start()

    def is_building_position_valid(self, new_building, with_info=False):
        """ Check if position of new building is valid """
        if not self.game_screen.get_rect().contains(new_building):
            if with_info:
                self.log.AppendText("Can't place building here - building has to be inside game screen.\n")
            return False
        for b in self.all_sprites.sprites():
            if pygame.sprite.collide_rect(b, new_building):
                if with_info:
                    self.log.AppendText("Can't place building here - there is another building or game panel "
                                        "in that place.\n")
                return False
        return True

    def choose_game_screen_texture(self):
        x, y = self.map_position
        if (abs(x) + abs(y)) % 2 == 0:
            return pygame.image.load(relative_textures_path + self.texture_one)
        else:
            return pygame.image.load(relative_textures_path + self.texture_two)

    def switch_game_tile(self, nav_arrow):
        # save sprites for current position
        self.current_tile.buildings_sprites = self.buildings_sprites
        self.current_tile.all_sprites = self.all_sprites

        # change current position
        if nav_arrow.direction == "Left":
            self.map_position = (self.map_position[0] - 1, self.map_position[1])
        if nav_arrow.direction == "Right":
            self.map_position = (self.map_position[0] + 1, self.map_position[1])
        if nav_arrow.direction == "Up":
            self.map_position = (self.map_position[0], self.map_position[1] + 1)
        if nav_arrow.direction == "Down":
            self.map_position = (self.map_position[0], self.map_position[1] - 1)

        x, y = self.map_position

        # if we are first time in given location create new MapTile
        if not str((x, y)) in self.map_tiles:
            new_game_screen = pygame.Surface.copy(self.background)
            image = self.choose_game_screen_texture()
            image = pygame.transform.scale(image, (self.width, self.height))
            new_game_screen.blit(image, (0, 0))
            map_tile = MapTile(new_game_screen, pygame.sprite.Group(), pygame.sprite.Group())
            self.map_tiles[str((x, y))] = map_tile

        # otherwise just get game_screen of new position
        else:
            map_tile = self.map_tiles[str((x, y))]

        # set current tile
        self.current_tile = map_tile

        # set game_screen to current tile game_screen
        self.game_screen = self.current_tile.game_screen

        # set buildings and all sprites
        self.buildings_sprites = self.current_tile.buildings_sprites
        self.all_sprites = self.current_tile.all_sprites

        # set panel's game_screen, draw panels, add panels to sprites
        self.resources.game_screen = self.game_screen
        for panel in self.panels:
            panel.game_screen = self.game_screen
            panel.draw_panel()
            self.all_sprites.add(panel)

        self.buildings_panel.draw_buildings_in_buildings_panel()
        for nav_arrow in self.navigation_arrows_sprites:
            nav_arrow.game_screen = self.game_screen
            nav_arrow.draw_navigation_arrow()

        # draw position and buildings
        draw_text(0, self.height * RESOURCES_PANEL_SIZE, str(self.map_position), PURPLE, self.game_screen)
        for building in self.buildings_sprites:
            self.game_screen.blit(building.image, building.pos)

# =================================================================================================================== #
# Communication with model
# =================================================================================================================== #

# =================================================================================================================== #
# Sending messages to model
# =================================================================================================================== #

    def ret_to_menu(self, event):
        """ Menu button logic """
        self.map_tiles = {}
        self.buildings_sprites = pygame.sprite.Group()
        self.buildings_panel_sprites = pygame.sprite.Group()
        self.navigation_arrows_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.game_on = False
        self.map_position = (0, 0)
        self.listener_thread.join()

        msg = {}
        msg["To"] = "MapNode"
        msg["Operation"] = "MoveTo"
        msg["Args"] = {}
        msg["Args"]["TargetView"] = "GameMenu"
        msg["Args"]["TargetControlNode"] = "GameMenuNode"
        self.sender.send(json.dumps(msg))

    def place_building(self, building, pos):

        # we have to do this in case of negative incomes
        self.check_if_can_afford(building)
        if not self.can_afford_on_building:
            return

        pos_x, pos_y = pos
        building.pos = pos
        building.rect = building.image.get_rect(topleft=(pos[0], pos[1]))

        # Create sprite for new building
        if self.is_building_position_valid(building, True):
            self.game_screen.blit(building.image, (pos_x, pos_y))
            self.buildings_sprites.add(building)
            self.all_sprites.add(building)

            # Send info to model that we have placed building
            msg = {}
            msg["To"] = "MapNode"
            msg["Operation"] = "placeBuilding"
            msg["Args"] = {}
            msg["Args"]["BuildingName"] = building.name
            msg["Args"]["BuildingId"] = building.id
            stream = json.dumps(msg)
            self.sender.send(stream)
        else:
            draw_text_with_wrapping(pos[0], pos[1], self.width, "Invalid position for building", RED,
                                    self.background)

    def check_if_can_afford(self, building):
        new_building = Building(building.name, uuid.uuid4().__str__(), building.texture, building.resources_cost,
                                building.consumes, building.produces, self.game_screen.get_size(), (0, 0))
        # Send request to model to check if we can afford for this building
        msg = {}
        msg["To"] = "MapNode"
        msg["Operation"] = "canAffordOnBuilding"
        msg["Args"] = {}
        msg["Args"]["BuildingName"] = new_building.name
        msg["Args"]["BuildingId"] = new_building.id
        stream = json.dumps(msg)

        self.condition.acquire()
        self.has_reply_arrived = False
        self.sender.send(stream)
        self.condition.wait()
        self.condition.release()
        return new_building

    def delete_building(self, building_sprite):
        msg = {}
        msg["To"] = "MapNode"
        msg["Operation"] = "deleteBuilding"
        msg["Args"] = {}
        msg["Args"]["BuildingName"] = building_sprite.name
        msg["Args"]["BuildingId"] = building_sprite.id
        stream = json.dumps(msg)
        self.sender.send(stream)

        building_sprite.kill()
        image = self.choose_game_screen_texture()
        image = pygame.transform.scale(image, (self.width, self.height))
        self.game_screen.blit(image, (0, 0))
        for panel in self.panels:
            panel.draw_panel()

        self.info_panel.curr_building = None
        self.buildings_panel.draw_buildings_in_buildings_panel()

        for nav_arrow in self.navigation_arrows_sprites:
            nav_arrow.draw_navigation_arrow()
        draw_text(0, self.height * RESOURCES_PANEL_SIZE, str(self.map_position), PURPLE, self.game_screen)
        for building in self.buildings_sprites:
            self.game_screen.blit(building.image, building.pos)

    def stop_production(self, building_sprite):
        msg = {}
        msg["To"] = "MapNode"
        msg["Operation"] = "stopProduction"
        msg["Args"] = {}
        msg["Args"]["BuildingName"] = building_sprite.name
        msg["Args"]["BuildingId"] = building_sprite.id
        stream = json.dumps(msg)
        self.sender.send(stream)

    def get_building_state(self, building):
        msg = dict()
        msg["To"] = "MapNode"
        msg["Operation"] = "getBuildingState"
        msg["Args"] = {}
        msg["Args"]["BuildingId"] = building.id
        stream = json.dumps(msg)
        self.sender.send(stream)

# =================================================================================================================== #
# Reading messages from model
# =================================================================================================================== #
    def readMsg(self, msg):
        try:
            parsed_msg = json.loads(msg)
            args = parsed_msg["Args"]
        except:
            traceback.print_exc()
            return

        operation = parsed_msg["Operation"]

        if operation == "Init":
            # get textures for map
            self.texture_one = args["Texture One"]
            self.texture_two = args["Texture Two"]

            # set texture for first map tile
            self.image = self.choose_game_screen_texture()
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            self.game_screen.blit(self.image, (0, 0))

            self.info_panel.draw_panel()
            self.buildings_panel.draw_panel()
            self.navigation_panel.draw_panel()
            for nav_arrow in self.navigation_arrows_sprites:
                nav_arrow.draw_navigation_arrow()

            draw_text(0, self.height * RESOURCES_PANEL_SIZE, str(self.map_position), PURPLE, self.game_screen)

            self.buildings_panel.add_buildings_to_buildings_panel(args["buildings"])
            self.resources = Resources(args["resources"], self.game_screen)

            self.resources_dict = self.resources_panel.resources

        elif operation == "canAffordOnBuildingResult":
            # we can draw building with given id
            if args["canAffordOnBuilding"]:
                self.can_afford_on_building = True
            else:
                self.can_afford_on_building = False
                self.log.AppendText("You don't have enough resources to build {}\n".format(args["buildingName"]))
            self.condition.acquire()
            self.has_reply_arrived = True
            self.condition.notify()
            self.condition.release()

        elif operation == "placeBuildingResult" or operation == "deleteBuildingResult":
            # if we placed / deleted building we have to update resources
            self.last_res_info = args["actualRes"]
            self.resources_panel.resources_info = args["actualRes"]
            self.resources_panel.curr_dwellers_amount = args["currDwellersAmount"]
            self.resources_panel.draw_panel()

        elif operation == "Update":
            # update resources values
            self.last_res_info = args
            self.resources_panel.resources_info = args
            self.resources_panel.draw_panel()

        elif operation == "stopProductionResult":
            self.last_res_info = args["actualRes"]
            self.resources_panel.resources_info = args["actualRes"]
            self.resources_panel.draw_panel()
            if self.info_panel.stop_production_button.texture == relative_textures_path + 'Start.png':
                self.info_panel.stop_production_button.set_texture(relative_textures_path + 'StopProduction.png')
            else:
                self.info_panel.stop_production_button.set_texture(relative_textures_path + 'Start.png')
            self.info_panel.redraw_panel(self)

        elif operation == "getBuildingStateResult":
            # For now we only get information if building i running
            self.info_panel.draw_buildings_info(self, args["isRunning"])

        else:
            print "Unknown message"

