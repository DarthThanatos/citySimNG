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
    PURPLE, RIGHT, LEFT, FONT
from NavigationArrow import NavigationArrow


# ------------------------------------------ Main class --------------------------------------------------------------#

class MapView(wx.Panel):
    background = None
    game_screen = None
    game_screen_tiles = {}
    resources_panel = None
    buildings_panel = None
    listener_thread = None
    buildings_sprites = pygame.sprite.Group()
    buildings_panel_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    navigation_arrows_sprites = pygame.sprite.Group()
    right_arrow_buildings_panel = None
    left_arrow_buildings_panel = None
    buildings_dict = {}
    game_on = True
    resources_initialized = False
    condition = threading.Condition()

    def __init__(self, parent, size, name, sender, music_path=relative_music_path + "TwoMandolins.mp3"):
        # call base class constructor
        wx.Panel.__init__(self, parent=parent, size=size)

        # set class fields
        self.parent = parent
        self.size_x = size[0]
        self.size_y = size[1]
        self.name = name
        self.sender = sender
        self.music_path = music_path

        # bind EVT_SHOW to onShow() function
        self.Bind(wx.EVT_SHOW, self.on_show, self)

        # add buttons
        self.init_buttons()

    def init_buttons(self):
        """ Function adding buttons """
        menu_btn = wx.Button(self, label="Menu", pos=(self.size_x - BUILDINGS_PANEL_SIZE * self.size_x,
                                                      self.size_y - RESOURCES_PANEL_SIZE * self.size_y),
                             size=(BUILDINGS_PANEL_SIZE * self.size_x, RESOURCES_PANEL_SIZE * self.size_y))
        self.Bind(wx.EVT_BUTTON, self.ret_to_menu, menu_btn)

    def ret_to_menu(self, event):
        """ Menu button logic """
        self.background = None
        self.game_screen = None
        self.game_screen_tiles = {}
        self.resources_panel = None
        self.buildings_panel = None
        self.buildings_sprites = pygame.sprite.Group()
        self.buildings_panel_sprites = pygame.sprite.Group()
        self.navigation_arrows_sprites = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.right_arrow_buildings_panel = None
        self.left_arrow_buildings_panel = None
        self.buildings_dict = {}
        self.game_on = False
        self.resources_initialized = False
        self.listener_thread.join()
        self.listener_thread = None
        #self.sender.send("MapNode@MoveTo@MenuNode")
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
                pygame.mixer.music.load(
                    #os.path.dirname(os.path.abspath(__file__)) + "\\" +
                    self.music_path)
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
        image = pygame.image.load(relative_textures_path + "Grass.png")
        image = pygame.transform.scale(image, (self.size_x, self.size_y))
        self.game_screen.blit(image, (0, 0))

        # Create resources panel and add it to all sprites
        self.resources_panel = ResourcesPanel(self.game_screen, 0, self.size_y - RESOURCES_PANEL_SIZE * self.size_y,
                                              self.size_x, RESOURCES_PANEL_SIZE * self.size_y)
        self.all_sprites.add(self.resources_panel)

        # Create buildings panel, draw it and add it to all sprites
        self.buildings_panel = BuildingsPanel(self.game_screen, self,
                                              self.size_x - BUILDINGS_PANEL_SIZE * self.size_x, 0,
                                              BUILDINGS_PANEL_SIZE * self.size_x, self.size_y)
        self.buildings_panel.draw_buildings_panel()
        self.all_sprites.add(self.buildings_panel)

        self.current_tile = GameTile(self.game_screen, self.all_sprites, self.buildings_sprites)

        # Create arrows for moving map
        self.create_navigation_arrows()

        # start new thread, that will be listening for player events
        self.game_on = True
        self.listener_thread = UserEventHandlerThread(self)
        self.listener_thread.start()

    def create_navigation_arrows(self):
        left_arrow = NavigationArrow(self.size_x * NAV_ARROW_WIDTH, self.size_y * NAV_ARROW_HEIGHT,
                                     0, 0.5 * self.size_y, relative_textures_path + 'LeftArrow.png', 0,
                                     self.game_screen, "Left")
        up_arrow = NavigationArrow(self.size_x * NAV_ARROW_WIDTH, self.size_y * NAV_ARROW_HEIGHT,
                                   0.5 * self.size_x, 0, relative_textures_path + 'LeftArrow.png', 270,
                                   self.game_screen, "Up")
        right_arrow = NavigationArrow(self.size_x * NAV_ARROW_WIDTH, self.size_y * NAV_ARROW_HEIGHT,
                                      self.size_x - self.size_x * NAV_ARROW_WIDTH - self.size_x * BUILDINGS_PANEL_SIZE,
                                      0.5 * self.size_y, relative_textures_path + 'LeftArrow.png', 180,
                                      self.game_screen, "Right")
        down_arrow = NavigationArrow(self.size_x * NAV_ARROW_WIDTH, self.size_y * NAV_ARROW_HEIGHT, 0.5 * self.size_x,
                                     self.size_y - self.size_y * NAV_ARROW_HEIGHT - self.size_y * RESOURCES_PANEL_SIZE,
                                     relative_textures_path + 'LeftArrow.png', 90, self.game_screen, "Down")
        self.navigation_arrows_sprites = pygame.sprite.Group()
        self.navigation_arrows_sprites.add(left_arrow)
        self.navigation_arrows_sprites.add(up_arrow)
        self.navigation_arrows_sprites.add(right_arrow)
        self.navigation_arrows_sprites.add(down_arrow)

    def mes(self, msg, color, x, y, surface=None):
        font = pygame.font.SysFont(FONT, 25)
        screen_text = font.render(msg, True, color)
        if surface is None:
            self.game_screen.blit(screen_text, [x, y])
        else:
            surface.blit(screen_text, [x, y])
        return screen_text.get_size()

    def draw_message_with_wrapping(self, msg, color, x, y, surface):
        font = pygame.font.SysFont(FONT, 25)
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

    def is_building_position_valid(self, new_building):
        """ Check if position of new building is valid """
        if not self.game_screen.get_rect().contains(new_building):
            return False
        for b in self.all_sprites.sprites():
            if pygame.sprite.collide_rect(b, new_building):
                return False
        return True

    def place_building(self, building, pos):
        pos_x, pos_y = pos
        building.pos = pos
        building.rect = building.image.get_rect(topleft=(pos[0], pos[1]))
        # Create sprite for new building
        if self.is_building_position_valid(building):
            self.game_screen.blit(building.image, (pos_x, pos_y))
            self.buildings_sprites.add(building)
            self.all_sprites.add(building)
            # Send request to model to check if we can afford for this building
            msg = {}
            msg["To"] = "MapNode"
            msg["Operation"] = "placeBuilding"
            msg["Args"] = {}
            msg["Args"]["BuildingName"] = building.name
            msg["Args"]["BuildingId"] = building.id
            stream = json.dumps(msg)
            self.sender.send(stream)
            # self.resources_panel.draw_resources_panel(msg_as_dict["actualRes"], self)
        else:
            self.draw_message_with_wrapping("Invalid position for building", RED, pos[0], pos[1],
                                            self.background)

    def readMsg(self, msg):
        print "Map view got msg", msg
        try:
            fullMsg = json.loads(msg)
            msg_as_dict = fullMsg["Args"]
        except:
            traceback.print_exc()
            return
        if "buildings" in msg_as_dict:
            # fill buildings panel
            self.buildings = msg_as_dict["buildings"]
            self.buildings_panel.add_buildings_to_buildings_panel(self.buildings)
            self.resources_panel.add_resources_to_resources_panel(msg_as_dict["resources"])
            self.resources_initialized = True
        elif "buildingID" in msg_as_dict:
            # we can draw building with given id
            if msg_as_dict["canAffordOnBuilding"]:
                self.can_afford = True
            else:
                self.can_afford = False
            self.condition.acquire()
            self.is_reply_arrived = True
            self.condition.notify()
            self.condition.release()
        elif "actualRes" in msg_as_dict:
            self.last_res_info = msg_as_dict["actualRes"]
            self.resources_panel.draw_resources_panel(msg_as_dict["actualRes"], self)
        else:
            # update resources values
            self.last_res_info = msg_as_dict
            self.resources_panel.draw_resources_panel(msg_as_dict, self)

    def switch_game_tile(self, nav_arrow):
        if nav_arrow.direction == "Left":
            print "Left arrow clicked"
            if self.current_tile.left is None:
                print "Create new tile"
                new_game_screen = pygame.Surface.copy(self.background)
                image = pygame.image.load(relative_textures_path + "Grass.png")
                image = pygame.transform.scale(image, (self.size_x, self.size_y))
                new_game_screen.blit(image, (0, 0))
                new_game_screen_tile = GameTile(new_game_screen, pygame.sprite.Group(), pygame.sprite.Group())
                self.current_tile.left = new_game_screen_tile
                new_game_screen_tile.right = self.current_tile
            self.current_tile.buildings_sprites = self.buildings_sprites
            self.current_tile.all_sprites = self.all_sprites
            self.current_tile = self.current_tile.left

        if nav_arrow.direction == "Right":
            if self.current_tile.right is None:
                new_game_screen = pygame.Surface.copy(self.background)
                image = pygame.image.load(relative_textures_path + "Grass.png")
                image = pygame.transform.scale(image, (self.size_x, self.size_y))
                new_game_screen.blit(image, (0, 0))
                new_game_screen_tile = GameTile(new_game_screen, pygame.sprite.Group(), pygame.sprite.Group())
                self.current_tile.right = new_game_screen_tile
                new_game_screen_tile.left = self.current_tile
            self.current_tile.buildings_sprites = self.buildings_sprites
            self.current_tile.all_sprites = self.all_sprites
            self.current_tile = self.current_tile.right

        if nav_arrow.direction == "Up":
            if self.current_tile.up is None:
                new_game_screen = pygame.Surface.copy(self.background)
                image = pygame.image.load(relative_textures_path + "Grass.png")
                image = pygame.transform.scale(image, (self.size_x, self.size_y))
                new_game_screen.blit(image, (0, 0))
                new_game_screen_tile = GameTile(new_game_screen, pygame.sprite.Group(), pygame.sprite.Group())
                self.current_tile.up = new_game_screen_tile
                new_game_screen_tile.down = self.current_tile
            self.current_tile.buildings_sprites = self.buildings_sprites
            self.current_tile.all_sprites = self.all_sprites
            self.current_tile = self.current_tile.up

        if nav_arrow.direction == "Down":
            if self.current_tile.down is None:
                new_game_screen = pygame.Surface.copy(self.background)
                image = pygame.image.load(relative_textures_path + "Grass.png")
                image = pygame.transform.scale(image, (self.size_x, self.size_y))
                new_game_screen.blit(image, (0, 0))
                new_game_screen_tile = GameTile(new_game_screen, pygame.sprite.Group(), pygame.sprite.Group())
                self.current_tile.down = new_game_screen_tile
                new_game_screen_tile.up = self.current_tile
            self.current_tile.buildings_sprites = self.buildings_sprites
            self.current_tile.all_sprites = self.all_sprites
            self.current_tile = self.current_tile.down

        self.game_screen = self.current_tile.game_screen
        self.buildings_panel.game_screen = self.game_screen
        self.resources_panel.game_screen = self.game_screen
        self.buildings_panel.draw_buildings_panel()
        self.buildings_panel.draw()
        self.resources_panel.draw_resources_panel(self.last_res_info, self)
        self.create_navigation_arrows()
        self.buildings_sprites = self.current_tile.buildings_sprites
        self.all_sprites = self.current_tile.all_sprites
        for building in self.buildings_sprites:
            self.game_screen.blit(building.image, building.pos)

    def check_if_can_afford(self, building):
        new_building = Building(building.name, uuid.uuid4().__str__(), building.resources_cost,
                                building.texture, self.game_screen, (0, 0))
        self.buildings_dict[str(new_building.id)] = new_building
        # Send request to model to check if we can afford for this building
        msg = {}
        msg["To"] = "MapNode"
        msg["Operation"] = "canAffordOnBuilding"
        msg["Args"] = {}
        msg["Args"]["BuildingName"] = new_building.name
        msg["Args"]["BuildingId"] = new_building.id
        stream = json.dumps(msg)
        # stream = "MapNode@PlaceBuilding@{},{}".format(new_building.name, new_building.id)
        self.condition.acquire()
        self.is_reply_arrived = False
        self.sender.send(stream)
        self.condition.wait()
        self.condition.release()
        return new_building


class GameTile:
    def __init__(self, game_screen, all_sprites, buildings_sprites):
        self.left = None
        self.up = None
        self.right = None
        self.down = None
        self.game_screen = game_screen
        self.all_sprites = all_sprites
        self.buildings_sprites = buildings_sprites


class UserEventHandlerThread(threading.Thread):
    def __init__(self, map_view):
        threading.Thread.__init__(self)
        self.map_view = map_view

    def run(self):
        sprite_is_chosen = False
        building = None
        clock = pygame.time.Clock()
        while self.map_view.game_on:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    pos = pygame.mouse.get_pos()
                    if sprite_is_chosen:
                        shadow.rect.center = pos
                        shadow.update()
                        self.map_view.place_building(building, (shadow.rect.left, shadow.rect.top))
                        sprite_is_chosen = False
                    else:
                        clicked_sprites = [s for s in self.map_view.buildings_panel_sprites if s.rect.collidepoint(pos)]
                        if len(clicked_sprites) == 1:
                            building = self.map_view.check_if_can_afford(clicked_sprites[0])
                            if self.map_view.can_afford:
                                sprite_is_chosen = True
                                shadow = Building(building.name, building.id, building.resources_cost,
                                                  building.texture, self.map_view.background, pos)
                                shadow.image.fill(RED)
                        if self.map_view.left_arrow_buildings_panel.collidepoint(pos):
                            self.map_view.buildings_panel.scroll_building_panel_left()
                        if self.map_view.right_arrow_buildings_panel.collidepoint(pos):
                            self.map_view.buildings_panel.scroll_building_panel_right()
                        clicked_nav_arrows = [s for s in self.map_view.navigation_arrows_sprites if s.rect.collidepoint(pos)]
                        if len(clicked_nav_arrows) == 1:
                            self.map_view.switch_game_tile(clicked_nav_arrows[0])
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                    if sprite_is_chosen:
                        sprite_is_chosen = False

            pos = pygame.mouse.get_pos()
            self.map_view.mes("FPS: " + str(FPS), PURPLE, 0, 0)
            self.map_view.background.blit(self.map_view.game_screen, (0, 0))
            if sprite_is_chosen:
                shadow.rect.center = pos
                shadow.update()
                if self.map_view.is_building_position_valid(shadow):
                    shadow.image.fill(GREEN)
                else:
                    shadow.image.fill(RED)
                self.map_view.background.blit(shadow.image, (shadow.rect.left, shadow.rect.top))
            if not sprite_is_chosen:
                for sprite in self.map_view.buildings_panel_sprites:
                    if sprite.rect.collidepoint(pos):
                        self.map_view.draw_message_with_wrapping(str(sprite.resources_cost), GREEN,
                                                                 pos[0], pos[1],
                                                                 self.map_view.background)
            pygame.display.flip()
            clock.tick(FPS)
