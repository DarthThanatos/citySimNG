import wx
import os
import re
import thread
import json
import uuid
import time
import pygame

FPS = 60
GREEN = (0, 150, 0)
YELLOW = (200, 200, 0)
PURPLE = (200, 0, 200)
RESOURCES_PANEL_SIZE = 0.2
BUILDINGS_PANEL_SIZE = 0.3
RESOURCES_PANEL_COLOUR = YELLOW
BUILDINGS_PANEL_COLOUR = PURPLE
RESOURCES_EXAMPLE = ["rock", "0", "gold", "0", "wood", "0"]
LEFT = 1
RIGHT = 3


class MapView(wx.Panel):
    sprites = []
    buildings_sprites = pygame.sprite.Group()
    buildings = []

    def __init__(self, parent, size, name, sender, musicPath="TwoMandolins.mp3"):
        # call base class constructor
        wx.Panel.__init__(self, parent=parent, size=size)

        # set class fields
        self.parent = parent
        self.size_x = size[0]
        self.size_y = size[1]
        self.name = name
        self.sender = sender
        self.musicPath = musicPath
        self.game_on = True
        self.buildings_dict = {}

        # bind EVT_SHOW to onShow() function
        self.Bind(wx.EVT_SHOW, self.onShow, self)

        # add buttons
        self.initButtons()

    def mes(self, msg, color, x, y):
        font = pygame.font.SysFont(None, 25)
        screen_text = font.render(msg, True, color)
        self.window.blit(screen_text, [x, y])

    def mouseListener(self):
        sprite_is_chosen = False
        building = None
        clock = pygame.time.Clock()
        while self.game_on:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                    if sprite_is_chosen:
                        pos = pygame.mouse.get_pos()
                        self.place_building(building, pos)
                        sprite_is_chosen = False
                    else:
                        pos = pygame.mouse.get_pos()
                        clicked_sprites = [s for s in self.buildings_sprites if s.rect.collidepoint(pos)]
                        if len(clicked_sprites) == 1:
                            sprite_is_chosen = True
                            building = clicked_sprites[0]
            self.mes("FPS: " + str(FPS), GREEN, 0, 0)
            pygame.display.flip()
            clock.tick(FPS)
        print "Thread is ending"

        return

    # background = pygame.Surface(self.window.get_size())
    # background.fill((122, 0, 0))
    # shadow = Building(building.name, -1, building.sizeX, building.sizeY, self, pos)
    # shadow_sprite = pygame.sprite.Group(shadow)
    # shadow_sprite.draw(self.window)
    # shadow_pos = pos
    # shadow.update_position(shadow_pos, pos, self)
    # shadow_sprite.update()
    # pygame.display.update()
    # pos = pygame.mouse.get_pos()
    # shadow_pos = shadow.update_position(shadow_pos, pos, self)
    # shadow_sprite.clear(self.window, background)
    # shadow_sprite.update()
    # shadow_sprite.draw(self.window)
    # pygame.display.update()

    def check_buildings_collision(self, new_building):
        """ Check if new building collides with some other one """
        for b in self.buildings_sprites.sprites():
            if pygame.sprite.collide_rect(b, new_building):
                return True
        return False

    def place_building(self, building, pos):
        # Create sprite for new building
        new_building = Building(building.name, uuid.uuid4(), building.size_x,
                                building.size_y, self, False, pos)
        self.buildings_dict[str(new_building.id)] = (new_building, pos)
        if self.check_buildings_collision(new_building):
            print "Collision detected. Can't place building here."
        else:
            # Send request to model to check if we can afford for this building
            stream = "MapNode@PlaceBuilding@{},{}".format(new_building.name, new_building.id)
            self.sender.send(stream)

    def initButtons(self):
        """ Function adding buttons """
        menu_btn = wx.Button(self, label="Menu", pos=(300, 500), size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

    def retToMenu(self, event):
        """ Menu button logic """
        self.game_on = False
        self.sender.send("MapNode@MoveTo@MenuNode")

    def readMsg(self, msg):
        print "Map view got msg", msg
        msg_as_dict = json.loads(msg)
        if "Buildings" in msg_as_dict:
            # fill buildings panel
            self.buildings = msg_as_dict["Buildings"]
            self.buildings_panel.add_buildings_to_buildings_panel(self.buildings, self)
        elif "BuildingID" in msg_as_dict:
            info = ""
            # we can draw building with given id
            if msg_as_dict["CanAfford"]:
                building = self.buildings_dict[msg_as_dict["BuildingID"]][0]
                pos_x = self.buildings_dict[msg_as_dict["BuildingID"]][1][0]
                pos_y = self.buildings_dict[msg_as_dict["BuildingID"]][1][1]
                self.window.fill(RESOURCES_PANEL_COLOUR,
                                 (pos_x, pos_y, building.size_x, building.size_y))
                self.buildings_sprites.add(building)
                for (key, value) in msg_as_dict["actualRes"].iteritems():
                    info += key + " " + str(value) + " "
                self.resources_panel.draw_resources_panel(info, self)
            else:
                for (key, value) in msg_as_dict["actualRes"].iteritems():
                    info += key + " " + str(value) + " "
                self.resources_panel.draw_resources_panel(info, self)
        else:
            # update resources values
            info = ""
            for (key, value) in msg_as_dict.iteritems():
                info += key + " " + str(value) + " "
            self.resources_panel.draw_resources_panel(info, self)

    def onShow(self, event):
        if event.GetShow():
            print "shown map"
            self.initView()
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(os.path.dirname(os.path.abspath(__file__)) + "\\" + self.musicPath)
                pygame.mixer.music.play()

            except Exception:
                print "Problem with music"
        else:
            try:
                pygame.quit()
            except Exception:
                print "first appearance of MapView: pygame not initialized in map"

    def initView(self):
        print "Map: initview"
        global pygame
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame  # this has to happen after setting the environment variables.
        pygame.init()
        pygame.display.init()
        self.window = pygame.display.set_mode((self.size_x, self.size_y))
        self.resources_panel = ResourcesPanel(self.window, 0, self.size_y - RESOURCES_PANEL_SIZE * self.size_y,
                                              self.size_x, RESOURCES_PANEL_SIZE * self.size_y)
        self.resources_panel.draw_resources_panel(" ".join(RESOURCES_EXAMPLE), self)
        self.buildings_panel = BuildingsPanel(self.window, self.size_x - BUILDINGS_PANEL_SIZE * self.size_x, 0,
                                             BUILDINGS_PANEL_SIZE * self.size_x, self.size_y)
        self.buildings_panel.draw_buildings_panel()
        pygame.display.flip()
        # start new thread, that will be listening for player events
        thread.start_new_thread(self.mouseListener, ())


class Building(pygame.sprite.Sprite):
    def __init__(self, name, id, size_x, size_y, window, panel_building=True, pos=()):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.id = id
        self.size_x = size_x
        self.size_y = size_y
        self.window = window

        # This is only building icon in buildings panel
        if panel_building:
            self.image = pygame.Surface([size_x, size_y])
            self.window.fill(RESOURCES_PANEL_COLOUR, (pos[0], pos[1], size_x, size_y))
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        # This is user building, before we draw it we have to check conditions
        else:
            self.image = pygame.Surface([size_x, size_y])
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))


class ResourcesPanel:
    def __init__(self, window, pos_x, pos_y, size_x, size_y):
        self.window = window
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

    def draw_resources_panel(self, resources_info, main_panel):
        self.window.fill(RESOURCES_PANEL_COLOUR, (self.pos_x, self.pos_y, self.size_x, self.size_y))
        main_panel.mes("Resources: " + resources_info, GREEN, self.pos_x, self.pos_y)


class BuildingsPanel:
    def __init__(self, window, pos_x, pos_y, size_x, size_y):
        self.window = window
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.size_x = size_x
        self.size_y = size_y

    def draw_buildings_panel(self):
        self.window.fill(BUILDINGS_PANEL_COLOUR, (self.pos_x, self.pos_y, self.size_x, self.size_y))

    def add_buildings_to_buildings_panel(self, buildings_info, main_panel):
        for (pos, building) in enumerate(buildings_info):
            building_sprite = Building(building["name"], uuid.uuid4(),
                                       building["sizeX"], building["sizeY"], self.window,
                                       pos=(self.pos_x + 60 * (pos % 2), 60 * (pos / 2)))
            main_panel.buildings_sprites.add(building_sprite)
