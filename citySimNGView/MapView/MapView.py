import wx
import os
import threading
import json
import uuid
import pygame
import traceback
from RelativePaths import relative_music_path, relative_textures_path
from ResourcesPanel import ResourcesPanel
from BuildingsPanel import BuildingsPanel
from Building import Building
from Consts import BUILDINGS_PANEL_SIZE, RESOURCES_PANEL_SIZE, NAV_ARROW_HEIGHT, NAV_ARROW_WIDTH, FPS, GREEN, RED, \
    PURPLE, FONT, GRASS_TEXTURE, GRASS2_TEXTURE, NAV_ARROW_TEXTURE, FONT_SIZE, TEXT_PANEL_HEIGHT, \
    TEXT_PANEL_WIDTH, MENU_BUTTON_WIDTH
from NavigationArrow import NavigationArrow
from UserEventHandlerThread import UserEventHandlerThread
from MapTile import MapTile
import math
from NavigationPanel import NavigationPanel


class MapView(wx.Panel):
    current_tile = None
    game_screen_tiles = {}
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
        self.size_x = size[0]
        self.size_y = int(math.ceil(size[1] - TEXT_PANEL_HEIGHT * size[1]))
        self.screen_height = size[1]
        self.name = name
        self.sender = sender
        self.music_path = music_path

        # bind EVT_SHOW to onShow() function
        self.Bind(wx.EVT_SHOW, self.on_show, self)

        # add buttons
        self.init_buttons()

        style = wx.TE_MULTILINE | wx.TE_READONLY | wx.HSCROLL
        self.log = wx.TextCtrl(self, wx.ID_ANY, size=(size[0] * TEXT_PANEL_WIDTH, TEXT_PANEL_HEIGHT * size[1]),
                               style=style, pos=(0, int(size[1] - TEXT_PANEL_HEIGHT * size[1])))
        font = wx.Font(FONT_SIZE, wx.MODERN, wx.NORMAL, wx.NORMAL, False, FONT)
        self.log.SetFont(font)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.sizer)
        # self.log.AppendText("ala ma kota")

    def init_buttons(self):
        """ Function adding buttons """
        menu_btn = wx.Button(self, label="Menu", pos=(self.size_x - MENU_BUTTON_WIDTH * self.size_x,
                                                      self.screen_height - self.screen_height * TEXT_PANEL_HEIGHT),
                             size=(MENU_BUTTON_WIDTH * self.size_x, self.screen_height * TEXT_PANEL_HEIGHT))
        self.Bind(wx.EVT_BUTTON, self.ret_to_menu, menu_btn)

    def ret_to_menu(self, event):
        """ Menu button logic """
        self.game_screen_tiles = {}
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
        self.background = pygame.display.set_mode((self.size_x, self.size_y))
        self.game_screen = pygame.Surface.copy(self.background)


        # Create resources panel and add it to all sprites
        self.resources_panel = ResourcesPanel(self.game_screen, 0, self.size_y - RESOURCES_PANEL_SIZE * self.size_y,
                                              self.size_x - BUILDINGS_PANEL_SIZE * self.size_x,
                                              RESOURCES_PANEL_SIZE * self.size_y, self)
        self.all_sprites.add(self.resources_panel)

        # Create buildings panel, draw it and add it to all sprites
        self.buildings_panel = BuildingsPanel(self.game_screen, self,
                                              self.size_x - BUILDINGS_PANEL_SIZE * self.size_x, 0,
                                              BUILDINGS_PANEL_SIZE * self.size_x,
                                              self.size_y - RESOURCES_PANEL_SIZE * self.size_y)

        self.all_sprites.add(self.buildings_panel)

        self.navigation_panel = NavigationPanel(self.size_x - BUILDINGS_PANEL_SIZE * self.size_x,
                                                self.size_y - RESOURCES_PANEL_SIZE * self.size_y,
                                                BUILDINGS_PANEL_SIZE * self.size_x,
                                                RESOURCES_PANEL_SIZE * self.size_y,
                                                self.game_screen)

        self.all_sprites.add(self.navigation_panel)

        self.current_tile = MapTile(self.game_screen, self.all_sprites, self.buildings_sprites)
        self.game_screen_tiles[str(self.map_position)] = self.current_tile

        # Create and draw arrows for moving map
        self.create_navigation_arrows()

        # start new thread, that will be listening for player events
        self.game_on = True
        self.listener_thread = UserEventHandlerThread(self)
        self.listener_thread.start()

    def create_navigation_arrows(self):
        y = self.resources_panel.pos_y
        x = self.buildings_panel.pos_x
        height = self.resources_panel.size_y
        width = self.buildings_panel.size_x
        middle_y = y + height / 2 - height * NAV_ARROW_HEIGHT / 2
        middle_x = x + width / 2 - width * NAV_ARROW_WIDTH / 2
        max_x = x + width - NAV_ARROW_WIDTH * width
        max_y = y + height - NAV_ARROW_HEIGHT * height

        left_arrow = NavigationArrow(width * NAV_ARROW_WIDTH, height * NAV_ARROW_HEIGHT,
                                     x, middle_y, NAV_ARROW_TEXTURE, 0, self.game_screen, "Left")
        up_arrow = NavigationArrow(width * NAV_ARROW_HEIGHT, height * NAV_ARROW_WIDTH,
                                   middle_x, y, NAV_ARROW_TEXTURE, 270, self.game_screen, "Up")
        right_arrow = NavigationArrow(width * NAV_ARROW_WIDTH, height * NAV_ARROW_HEIGHT, max_x, middle_y,
                                      NAV_ARROW_TEXTURE, 180, self.game_screen, "Right")
        down_arrow = NavigationArrow(width * NAV_ARROW_HEIGHT, height * NAV_ARROW_WIDTH, middle_x, max_y,
                                     NAV_ARROW_TEXTURE, 90, self.game_screen, "Down")

        self.navigation_arrows_sprites = pygame.sprite.Group()
        self.navigation_arrows_sprites.add(left_arrow)
        self.navigation_arrows_sprites.add(up_arrow)
        self.navigation_arrows_sprites.add(right_arrow)
        self.navigation_arrows_sprites.add(down_arrow)

    def mes(self, msg, color, x, y, surface=None, draw=True):
        font = pygame.font.SysFont(FONT, FONT_SIZE)
        screen_text = font.render(msg, True, color)
        if draw:
            if surface is None:
                self.game_screen.blit(screen_text, [x, y])
            else:
                surface.blit(screen_text, [x, y])
        return screen_text.get_size()

    def draw_message_with_wrapping(self, msg, color, x, y, surface):
        font = pygame.font.SysFont(FONT, FONT_SIZE)
        space_width = font.size(' ')[0]  # get space width
        pos_x, pos_y = x, y
        max_width, max_height = self.game_screen.get_size()
        for word in msg.split(" "):
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if pos_x + word_width >= max_width:
                pos_x = x  # Reset the x.
                pos_y += word_height  # Start on new row.
            surface.blit(word_surface, (pos_x, pos_y))
            pos_x += word_width + space_width

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

    def place_building(self, building, pos):
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
            self.draw_message_with_wrapping("Invalid position for building", RED, pos[0], pos[1],
                                            self.background)

    def readMsg(self, msg):
        #print "Map view got msg", msg
        try:
            parsed_msg = json.loads(msg)
            args = parsed_msg["Args"]
        except:
            traceback.print_exc()
            return
        operation = parsed_msg["Operation"]
        if operation == "Init":
            self.texture_one = args["Texture One"]
            self.texture_two = args["Texture Two"]
            print "texture one:",self.texture_one,"texture two", self.texture_two
            print "TEXTURE ONE " + str(self.texture_one)
            self.image = self.choose_game_screen_texture()
            self.image = pygame.transform.scale(self.image, (self.size_x, self.size_y))
            self.game_screen.blit(self.image, (0, 0))

            self.buildings_panel.draw_buildings_panel()
            self.navigation_panel.draw_navigation_panel()
            for nav_arrow in self.navigation_arrows_sprites:
                nav_arrow.draw_navigation_arrow()

            self.mes(str(self.map_position), PURPLE, 0, 0)

            self.buildings_panel.add_buildings_to_buildings_panel(args["buildings"])
            self.resources_panel.add_resources_to_resources_panel(args["resources"])

            #global GRASS_TEXTURE, GRASS2_TEXTURE
            #GRASS_TEXTURE = relative_textures_path + texture_one
            #GRASS2_TEXTURE = relative_textures_path + texture_two
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
            self.last_res_info = args["actualRes"]
            self.resources_panel.draw_resources_panel(args["actualRes"])
        elif operation == "Update":
            # update resources values
            self.last_res_info = args
            self.resources_panel.draw_resources_panel(args)
        else:
            print "Unknown message"

    def choose_game_screen_texture(self):
        x, y = self.map_position
        if (abs(x) + abs(y)) % 2 == 0:
            return pygame.image.load(relative_textures_path + self.texture_one)
        else:
            return pygame.image.load(relative_textures_path + self.texture_two)

    def switch_game_tile(self, nav_arrow):
        x, y = self.map_position
        if nav_arrow.direction == "Left":
            self.map_position = (self.map_position[0] - 1, self.map_position[1])
            if not str((x - 1, y)) in self.game_screen_tiles:
                new_game_screen = pygame.Surface.copy(self.background)
                image = self.choose_game_screen_texture()
                image = pygame.transform.scale(image, (self.size_x, self.size_y))
                new_game_screen.blit(image, (0, 0))
                game_screen_tile = MapTile(new_game_screen, pygame.sprite.Group(), pygame.sprite.Group())
                self.game_screen_tiles[str((x - 1, y))] = game_screen_tile
            else:
                game_screen_tile = self.game_screen_tiles[str((x - 1, y))]

            self.current_tile.buildings_sprites = self.buildings_sprites
            self.current_tile.all_sprites = self.all_sprites
            self.current_tile = game_screen_tile

        if nav_arrow.direction == "Right":
            self.map_position = (self.map_position[0] + 1, self.map_position[1])
            if not str((x + 1, y)) in self.game_screen_tiles:
                new_game_screen = pygame.Surface.copy(self.background)
                image = self.choose_game_screen_texture()
                image = pygame.transform.scale(image, (self.size_x, self.size_y))
                new_game_screen.blit(image, (0, 0))
                game_screen_tile = MapTile(new_game_screen, pygame.sprite.Group(), pygame.sprite.Group())
                self.game_screen_tiles[str((x + 1, y))] = game_screen_tile
            else:
                game_screen_tile = self.game_screen_tiles[str((x + 1, y))]

            self.current_tile.buildings_sprites = self.buildings_sprites
            self.current_tile.all_sprites = self.all_sprites
            self.current_tile = game_screen_tile

        if nav_arrow.direction == "Up":
            self.map_position = (self.map_position[0], self.map_position[1] + 1)
            if not str((x, y + 1)) in self.game_screen_tiles:
                new_game_screen = pygame.Surface.copy(self.background)
                image = self.choose_game_screen_texture()
                image = pygame.transform.scale(image, (self.size_x, self.size_y))
                new_game_screen.blit(image, (0, 0))
                game_screen_tile = MapTile(new_game_screen, pygame.sprite.Group(), pygame.sprite.Group())
                self.game_screen_tiles[str((x, y + 1))] = game_screen_tile
            else:
                game_screen_tile = self.game_screen_tiles[str((x, y + 1))]

            self.current_tile.buildings_sprites = self.buildings_sprites
            self.current_tile.all_sprites = self.all_sprites
            self.current_tile = game_screen_tile

        if nav_arrow.direction == "Down":
            self.map_position = (self.map_position[0], self.map_position[1] - 1)
            if not str((x, y - 1)) in self.game_screen_tiles:
                new_game_screen = pygame.Surface.copy(self.background)
                image = self.choose_game_screen_texture()
                image = pygame.transform.scale(image, (self.size_x, self.size_y))
                new_game_screen.blit(image, (0, 0))
                game_screen_tile = MapTile(new_game_screen, pygame.sprite.Group(), pygame.sprite.Group())
                self.game_screen_tiles[str((x, y - 1))] = game_screen_tile
            else:
                game_screen_tile = self.game_screen_tiles[str((x, y - 1))]

            self.current_tile.buildings_sprites = self.buildings_sprites
            self.current_tile.all_sprites = self.all_sprites
            self.current_tile = game_screen_tile

        self.game_screen = self.current_tile.game_screen
        self.buildings_panel.game_screen = self.game_screen
        self.resources_panel.game_screen = self.game_screen
        self.navigation_panel.game_screen = self.game_screen
        self.navigation_panel.draw_navigation_panel()
        self.buildings_panel.draw_buildings_panel()
        self.buildings_panel.draw_buildings_in_buildings_panel()
        self.resources_panel.draw_resources_panel(self.last_res_info)
        self.create_navigation_arrows()
        for nav_arrow in self.navigation_arrows_sprites:
            nav_arrow.draw_navigation_arrow()
        self.buildings_sprites = self.current_tile.buildings_sprites
        self.all_sprites = self.current_tile.all_sprites
        self.all_sprites.add(self.resources_panel)
        self.all_sprites.add(self.buildings_panel)
        self.mes(str(self.map_position), PURPLE, 0, 0)
        for building in self.buildings_sprites:
            self.game_screen.blit(building.image, building.pos)

    def check_if_can_afford(self, building):
        new_building = Building(building.name, uuid.uuid4().__str__(), building.resources_cost,
                                building.texture, self.game_screen.get_size(), (0, 0))
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
        self.game_screen.blit(self.image, (0, 0))
        self.navigation_panel.draw_navigation_panel()
        self.buildings_panel.draw_buildings_panel()
        self.buildings_panel.draw_buildings_in_buildings_panel()
        self.resources_panel.draw_resources_panel(self.last_res_info)
        for nav_arrow in self.navigation_arrows_sprites:
            nav_arrow.draw_navigation_arrow()
        self.mes(str(self.map_position), PURPLE, 0, 0)
        for building in self.buildings_sprites:
            self.game_screen.blit(building.image, building.pos)


