import wx
import os
import re
import threading
import json
import uuid
import time
import pygame

FPS = 60
GREEN = (0, 150, 0)
YELLOW = (200, 200, 0)
PURPLE = (200, 0, 200)
RESOURCES_PANEL_SIZE = 0.2
BUILDINGS_PANEL_SIZE = 0.15
RESOURCES_PANEL_COLOUR = YELLOW
BUILDINGS_PANEL_COLOUR = PURPLE
RESOURCES_EXAMPLE = ["rock", "0", "gold", "0", "wood", "0"]
LEFT = 1
RIGHT = 3
DEFAULT_BUILDING_TEXTURE = "Textures\\DefaultBuilding.jpg"
BUILDING_SIZE = 0.05
SPACE = 20


class MapView(wx.Panel):
    buildings_sprites = pygame.sprite.Group()
    buildings = []

    def __init__(self, parent, size, name, sender, music_path="TwoMandolins.mp3"):
        # call base class constructor
        wx.Panel.__init__(self, parent=parent, size=size)

        # set class fields
        self.parent = parent
        self.size_x = size[0]
        self.size_y = size[1]
        self.name = name
        self.sender = sender
        self.music_path = music_path
        self.game_on = True
        self.buildings_dict = {}

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
        self.listener_thread.join()
        self.sender.send("MapNode@MoveTo@MenuNode")

    def on_show(self, event):
        if event.GetShow():
            print "shown map"
            self.init_view()
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(os.path.dirname(os.path.abspath(__file__)) + "\\" + self.music_path)
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
        self.background = pygame.display.set_mode((self.size_x, self.size_y))
        self.game_screen = pygame.Surface.copy(self.background)
        image = pygame.image.load("Textures\\Grass.png")
        image = pygame.transform.scale(image, (self.size_x, self.size_y))
        self.game_screen.blit(image, (0, 0))
        self.resources_panel = ResourcesPanel(self.game_screen, 0, self.size_y - RESOURCES_PANEL_SIZE * self.size_y,
                                              self.size_x, RESOURCES_PANEL_SIZE * self.size_y)
        self.resources_panel.draw_resources_panel(" ".join(RESOURCES_EXAMPLE), self)
        self.buildings_panel = BuildingsPanel(self.game_screen, self.size_x - BUILDINGS_PANEL_SIZE * self.size_x, 0,
                                              BUILDINGS_PANEL_SIZE * self.size_x, self.size_y)
        self.buildings_panel.draw_buildings_panel()

        # start new thread, that will be listening for player events
        self.game_on = True
        self.listener_thread = UserEventHandlerThread(self)
        self.listener_thread.start()

    def mes(self, msg, color, x, y):
        font = pygame.font.SysFont(None, 25)
        screen_text = font.render(msg, True, color)
        self.game_screen.blit(screen_text, [x, y])

    def check_buildings_collision(self, new_building):
        """ Check if new building collides with some other one """
        for b in self.buildings_sprites.sprites():
            if pygame.sprite.collide_rect(b, new_building):
                return True
        return False

    def place_building(self, building, pos):
        # Create sprite for new building
        new_building = Building(building.name, uuid.uuid4(), building.texture, self.game_screen, False, pos)
        self.buildings_dict[str(new_building.id)] = (new_building, pos)
        if self.check_buildings_collision(new_building):
            print "Collision detected. Can't place building here."
        else:
            # Send request to model to check if we can afford for this building
            stream = "MapNode@PlaceBuilding@{},{}".format(new_building.name, new_building.id)
            self.sender.send(stream)

    def readMsg(self, msg):
        print "Map view got msg", msg
        msg_as_dict = json.loads(msg)
        if "buildings" in msg_as_dict:
            # fill buildings panel
            self.buildings = msg_as_dict["buildings"]
            self.buildings_panel.add_buildings_to_buildings_panel(self.buildings, self)
        elif "buildingID" in msg_as_dict:
            info = ""
            # we can draw building with given id
            if msg_as_dict["canAfford"]:
                building = self.buildings_dict[msg_as_dict["buildingID"]][0]
                pos_x = self.buildings_dict[msg_as_dict["buildingID"]][1][0]
                pos_y = self.buildings_dict[msg_as_dict["buildingID"]][1][1]
                self.game_screen.blit(building.image, (pos_x, pos_y))
                self.buildings_sprites.add(building)
                for (key, value) in msg_as_dict["actualRes"].iteritems():
                    info += key + ": " + str(value) + " "
                self.resources_panel.draw_resources_panel(info, self)
            else:
                for (key, value) in msg_as_dict["actualRes"].iteritems():
                    info += key + ": " + str(value) + " "
                self.resources_panel.draw_resources_panel(info, self)
        else:
            # update resources values
            info = ""
            for (key, value) in msg_as_dict.iteritems():
                info += key + ": " + str(value) + " "
            self.resources_panel.draw_resources_panel(info, self)


class Building(pygame.sprite.Sprite):
    def __init__(self, name, id, texture, game_screen, panel_building=True, pos=()):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.id = id
        self.texture = texture
        self.game_screen = game_screen

        width, height = self.game_screen.get_size()
        # This is only building icon in buildings panel
        if panel_building:
            # self.image = pygame.Surface([size_x, size_y])
            try:
                self.image = pygame.image.load(self.texture)
            except Exception:
                self.texture = DEFAULT_BUILDING_TEXTURE
                self.image = pygame.image.load(self.texture)
            self.image = pygame.transform.scale(self.image, (int(width * BUILDING_SIZE),
                                                             int(height * BUILDING_SIZE)))
            self.game_screen.blit(self.image, (pos[0], pos[1]))
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        # This is user building, before we draw it we have to check conditions
        else:
            self.image = pygame.image.load(texture)
            self.image = pygame.transform.scale(self.image, (int(width * BUILDING_SIZE),
                                                             int(height * BUILDING_SIZE)))
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))


class ResourcesPanel:
    def __init__(self, game_screen, pos_x, pos_y, size_x, size_y):
        self.game_screen = game_screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

    def draw_resources_panel(self, resources_info, main_panel):
        image = pygame.image.load('Textures\\BuildingsPanelTexture.jpg')
        image = pygame.transform.scale(image, (int(self.size_x), int(self.size_y)))
        self.game_screen.blit(image, (self.pos_x, self.pos_y))
        main_panel.mes("Resources: " + resources_info, GREEN, self.pos_x, self.pos_y)


class BuildingsPanel:
    def __init__(self, game_screen, pos_x, pos_y, size_x, size_y):
        self.game_screen = game_screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

    def draw_buildings_panel(self):
        image = pygame.image.load('Textures\\BuildingsPanelTexture.jpg')
        image = pygame.transform.scale(image, (int(self.size_x), int(self.size_y)))
        self.game_screen.blit(image, (self.pos_x, self.pos_y))

    def add_buildings_to_buildings_panel(self, buildings_info, main_panel):
        width, height = self.game_screen.get_size()
        for (pos, building) in enumerate(buildings_info):
            building_sprite = Building(building["name"], uuid.uuid4(), building["texture"],
                                       self.game_screen,
                                       pos=(self.pos_x + BUILDING_SIZE * width * (pos % 2) + (pos % 2) * SPACE,
                                            BUILDING_SIZE * height * (pos / 2) + SPACE * (pos / 2)))
            main_panel.buildings_sprites.add(building_sprite)


class UserEventHandlerThread(threading.Thread):
    def __init__(self, mapView):
        threading.Thread.__init__(self)
        self.mapView = mapView

    def run(self):
        sprite_is_chosen = False
        building = None
        clock = pygame.time.Clock()
        while self.mapView.game_on:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    pos = pygame.mouse.get_pos()
                    if sprite_is_chosen:
                        shadow.rect.center = pos
                        shadow.update()
                        self.mapView.place_building(building, (shadow.rect.left, shadow.rect.top))
                        sprite_is_chosen = False
                    else:
                        clicked_sprites = [s for s in self.mapView.buildings_sprites if s.rect.collidepoint(pos)]
                        if len(clicked_sprites) == 1:
                            sprite_is_chosen = True
                            building = clicked_sprites[0]
                            shadow = Building(building.name, building.id, building.texture,
                                              self.mapView.background, False, pos)
                            shadow.image.fill(RESOURCES_PANEL_COLOUR)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == RIGHT:
                    if sprite_is_chosen:
                        sprite_is_chosen = False

            pos = pygame.mouse.get_pos()
            self.mapView.mes("FPS: " + str(FPS), GREEN, 0, 0)
            self.mapView.background.blit(self.mapView.game_screen, (0, 0))
            if sprite_is_chosen:
                shadow.rect.center = pos
                shadow.update()
                self.mapView.background.blit(shadow.image, (shadow.rect.left, shadow.rect.top))
            pygame.display.flip()
            clock.tick(FPS)
