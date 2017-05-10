import wx
import os
import threading
import json
import uuid
import pygame
import traceback


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

DEFAULT_BUILDING_TEXTURE = "Textures\\DefaultBuilding.jpg"
DEFAULT_RESOURCE_TEXTURE = "Textures\\DefaultBuilding.jpg"


class MapView(wx.Panel):
    background = None
    game_screen = None
    resources_panel = None
    buildings_panel = None
    listener_thread = None
    buildings_sprites = pygame.sprite.Group()
    buildings_panel_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    right_arrow_buildings_panel = None
    left_arrow_buildings_panel = None
    buildings_dict = {}
    game_on = True
    resources_initialized = False

    def __init__(self, parent, size, name, sender, music_path="music/TwoMandolins.mp3"):
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
        self.buildings_sprites = pygame.sprite.Group()
        self.game_on = False
        self.resources_initialized = False
        self.listener_thread.join()
        #self.sender.send("MapNode@MoveTo@MenuNode")
        msg = {}
        msg["To"] = "MapNode"
        msg["Operation"] = "MoveTo"
        msg["Args"] = {}
        msg["Args"]["TargetView"] = "Menu"
        msg["Args"]["TargetControlNode"] = "MenuNode"
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
        image = pygame.image.load("Textures\\Grass.png")
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

        # start new thread, that will be listening for player events
        self.game_on = True
        self.listener_thread = UserEventHandlerThread(self)
        self.listener_thread.start()

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
        # Create sprite for new building
        new_building = Building(building.name, uuid.uuid4().__str__(), building.resources_cost,
                                building.texture, self.game_screen, pos)
        self.buildings_dict[str(new_building.id)] = (new_building, pos)
        if self.is_building_position_valid(new_building):
            # Send request to model to check if we can afford for this building
            msg = {}
            msg["To"] = "MapNode"
            msg["Operation"] = "PlaceBuilding"
            msg["Args"] = {}
            msg["Args"]["BuildingName"] = new_building.name 
            msg["Args"]["BuildingId"] = new_building.id
            stream = json.dumps(msg)
            #stream = "MapNode@PlaceBuilding@{},{}".format(new_building.name, new_building.id)
            self.sender.send(stream)
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
            if msg_as_dict["canAfford"]:
                building = self.buildings_dict[msg_as_dict["buildingID"]][0]
                pos_x = self.buildings_dict[msg_as_dict["buildingID"]][1][0]
                pos_y = self.buildings_dict[msg_as_dict["buildingID"]][1][1]
                self.game_screen.blit(building.image, (pos_x, pos_y))
                self.buildings_sprites.add(building)
                self.all_sprites.add(building)
                self.resources_panel.draw_resources_panel(msg_as_dict["actualRes"], self)
            else:
                self.resources_panel.draw_resources_panel(msg_as_dict["actualRes"], self)
        else:
            # update resources values
            self.resources_panel.draw_resources_panel(msg_as_dict, self)


class Resource(pygame.sprite.Sprite):
    def __init__(self, name, texture_path, game_screen):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.texture_path = texture_path
        self.game_screen = game_screen

        width, height = self.game_screen.get_size()
        try:
            self.image = pygame.image.load(self.texture_path)
        except Exception:
            self.texture_path = DEFAULT_RESOURCE_TEXTURE
            self.image = pygame.image.load(self.texture_path)
        self.image = self.image.convert_alpha()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (int(width * RESOURCE_SIZE),
                                                         int(height * RESOURCE_SIZE)))


class ResourcesPanel(pygame.sprite.Sprite):
    def __init__(self, game_screen, pos_x, pos_y, size_x, size_y):
        pygame.sprite.Sprite.__init__(self)
        self.game_screen = game_screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.rect = None
        self.resources = {}

    def draw_resources_panel(self, resources_info, main_panel):
        image = pygame.image.load('Textures\\BuildingsPanelTexture.jpg')
        image = pygame.transform.scale(image, (int(self.size_x), int(self.size_y)))
        self.rect = image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.game_screen.blit(image, (self.pos_x, self.pos_y))
        pos_x = 0
        for (resource, info) in resources_info.iteritems():
            image = self.resources[resource].image
            self.game_screen.blit(image, (pos_x, self.pos_y))
            text_size = main_panel.mes(resource + ": " + str(info) + " ", GREEN,
                                       pos_x + image.get_size()[0] + RESOURCES_SPACE, self.pos_y)
            pos_x += text_size[0] + image.get_size()[0] + RESOURCES_SPACE

    def add_resources_to_resources_panel(self, resources_info):
        for (i, resource) in enumerate(resources_info):
            resource_sprite = Resource(resource["name"], resource["texturePath"], self.game_screen)
            self.resources[resource["name"]] = resource_sprite


class Building(pygame.sprite.Sprite):
    def __init__(self, name, id, resources_cost, texture, game_screen, pos=()):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.id = id
        self.resources_cost = resources_cost
        self.texture = texture
        self.game_screen = game_screen
        self.pos = pos

        width, height = self.game_screen.get_size()
        try:
            self.image = pygame.image.load(self.texture)
        except Exception:
            self.texture = DEFAULT_BUILDING_TEXTURE
            self.image = pygame.image.load(self.texture)
        self.image = pygame.transform.scale(self.image, (int(width * BUILDING_SIZE),
                                                         int(height * BUILDING_SIZE)))
        self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))


class BuildingsPanel(pygame.sprite.Sprite):
    buildings_info = None
    page = 1
    page_buildings = {}
    last_page = 1

    def __init__(self, game_screen, main_panel, pos_x, pos_y, size_x, size_y):
        pygame.sprite.Sprite.__init__(self)
        self.game_screen = game_screen
        self.main_panel = main_panel
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y
        self.rect = None

    def draw_buildings_panel(self):
        image = pygame.image.load('Textures\\BuildingsPanelTexture.jpg')
        image = pygame.transform.scale(image, (int(self.size_x), int(self.size_y)))
        self.rect = image.get_rect(topleft=(self.pos_x, self.pos_y))
        self.game_screen.blit(image, (self.pos_x, self.pos_y))

        image = pygame.image.load('Textures\\RightArrow.png')
        image = pygame.transform.scale(image, (int(ARROW_BUTTON_WIDTH * self.size_x),
                                               int(ARROW_BUTTON_HEIGHT * self.size_y)))
        right_arrow_rect = image.get_rect(topleft=(self.pos_x + RIGHT_ARROW_BUTTON_X * self.size_x,
                                          ARROW_BUTTON_Y * self.size_y))
        self.game_screen.blit(image, (self.pos_x + RIGHT_ARROW_BUTTON_X * self.size_x,
                                      ARROW_BUTTON_Y * self.size_y))
        self.main_panel.right_arrow_buildings_panel = right_arrow_rect

        image = pygame.image.load('Textures\\LeftArrow.png')
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
                    print self.map_view.left_arrow_buildings_panel
                    pos = pygame.mouse.get_pos()
                    print pos
                    if sprite_is_chosen:
                        shadow.rect.center = pos
                        shadow.update()
                        self.map_view.place_building(building, (shadow.rect.left, shadow.rect.top))
                        sprite_is_chosen = False
                    else:
                        clicked_sprites = [s for s in self.map_view.buildings_panel_sprites if s.rect.collidepoint(pos)]
                        if len(clicked_sprites) == 1:
                            sprite_is_chosen = True
                            building = clicked_sprites[0]
                            shadow = Building(building.name, building.id, building.resources_cost,
                                              building.texture, self.map_view.background, pos)
                            shadow.image.fill(RED)
                        if self.map_view.left_arrow_buildings_panel.collidepoint(pos):
                            self.map_view.buildings_panel.scroll_building_panel_left()
                        if self.map_view.right_arrow_buildings_panel.collidepoint(pos):
                            self.map_view.buildings_panel.scroll_building_panel_right()
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
