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
RESOURCES_PANEL_POSITION = (0, 400)
RESOURCES_PANEL_SIZE = 0.2
RESOURCES_PANEL_COLOUR = YELLOW
BUILDINGS_PANEL_SIZE = 0.3
BUILDINGS_PANEL_COLOUR = PURPLE
RESOURCES_EXAMPLE = ["rock", "0", "gold", "0", "wood", "0"]
LEFT = 1
RIGHT = 3


class MapViewResourcesPanel(wx.Panel):
    def __init__(self, parent, ID, panelPos, panelSize):
        self.parent = parent
        self.ID = ID
        self.panelSize = panelSize

        # resources
        self.resourcesValues = RESOURCES_EXAMPLE
        self.resourcesInfo = " ".join(self.resourcesValues)

        # create panel for resources
        wx.Panel.__init__(self, self.parent, self.ID, size=self.panelSize, pos=panelPos)
        self.SetBackgroundColour(RESOURCES_PANEL_COLOUR)

        # display information about resources
        self.centerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.resourcesField = wx.StaticText(self, label=self.resourcesInfo)
        self.centerSizer.Add(self.resourcesField, 0, wx.EXPAND, 5)

    def updateResources(self, info):
        self.resourcesField = wx.StaticText(self, label=info)
        self.centerSizer.Add(self.resourcesField, 0, wx.EXPAND, 5)
        self.Update()


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

        # bind EVT_SHOW to onShow() function
        self.Bind(wx.EVT_SHOW, self.onShow, self)

        # add buttons
        self.initButtons()

        # add resources panel
        # self.resourcesPanel = MapViewResourcesPanel(self, -1, (0, self.size_y - RESOURCES_PANEL_SIZE * self.size_y),
                          #                           (self.size_x, RESOURCES_PANEL_SIZE * self.size_y))
        # self.resourcesPanel.Show()

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
        new_building = Building(building.name, uuid.uuid4(), building.sizeX,
                                building.sizeY, self, False, pos)
        if self.check_buildings_collision(new_building):
            print "Collision detected. Can't place building here."
        else:
            # Send request to model to check if we can afford for this building
            stream = "MapNode@PlaceBuilding@{},{}".format(new_building.name, new_building.id)
            self.sender.send(stream)
            self.addRect(RESOURCES_PANEL_COLOUR,
                         (pos[0], pos[1], new_building.sizeX, new_building.sizeY))
            self.buildings_sprites.add(new_building)

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
            self.addBuildingsToBuildingsPanel()
        elif False:
            # we can draw building with given id
            info = ""
            for (key, value) in msg_as_dict.iteritems():
                info += key + " " + str(value) + " "
            self.updateResources(info)
        else:
            # update resources values
            info = ""
            for (key, value) in msg_as_dict.iteritems():
                info += key + " " + str(value) + " "
            self.updateResources(info)

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
        self.addBuildingsPanel()
        self.addResourcesPanel()
        pygame.display.flip()
        # pygame.display.update()
        # start new thread, that will be listening for player events
        thread.start_new_thread(self.mouseListener, ())



    def addRect(self, color, position):
        self.window.fill(color, position)

    def addBuildingsPanel(self):
        self.window.fill(BUILDINGS_PANEL_COLOUR,
                         (self.size_x - BUILDINGS_PANEL_SIZE * self.size_x, 0,
                          BUILDINGS_PANEL_SIZE * self.size_x, self.size_y))

    def addResourcesPanel(self):
        self.window.fill(RESOURCES_PANEL_COLOUR,
                         (0, self.size_y - RESOURCES_PANEL_SIZE * self.size_y,
                          self.size_x, RESOURCES_PANEL_SIZE * self.size_y))
        resourcesValues = RESOURCES_EXAMPLE
        resourcesInfo = " ".join(resourcesValues)
        self.mes("Resources: " + resourcesInfo, GREEN, 0, self.size_y - RESOURCES_PANEL_SIZE * self.size_y)

    def addBuildingsToBuildingsPanel(self):
        for (pos, building) in enumerate(self.buildings):
            building_sprite = Building(building["name"], uuid.uuid4(),
                                       building["sizeX"], building["sizeY"], self,
                                       pos=(self.size_x - BUILDINGS_PANEL_SIZE * self.size_x + 60 * (pos % 2),
                                            60 * (pos / 2)))
            self.buildings_sprites.add(building_sprite)
        pygame.display.update()

    def updateResources(self, info):
        self.window.fill(RESOURCES_PANEL_COLOUR,
                         (0, self.size_y - RESOURCES_PANEL_SIZE * self.size_y,
                          self.size_x, RESOURCES_PANEL_SIZE * self.size_y))
        self.mes("Resources: " + info, GREEN, 0, self.size_y - RESOURCES_PANEL_SIZE * self.size_y)
        pygame.display.update()


class Building(pygame.sprite.Sprite):

    def __init__(self, name, id, sizeX, sizeY, mapView, panel_building=True, pos=()):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.id = id
        self.sizeX = sizeX
        self.sizeY = sizeY

        # This is only building icon i buildings panel
        if panel_building:
            self.image = pygame.Surface([sizeX, sizeY])
            mapView.window.fill(RESOURCES_PANEL_COLOUR, (pos[0], pos[1], sizeX, sizeY))
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))
        # This is user building, before we draw it we have to check conditions
        else:
            self.image = pygame.Surface([sizeX, sizeY])
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))

    def update_position(self, pos, mouse_pos, mapView):
        self.rect = self.image.get_rect(topleft=(mouse_pos[0], mouse_pos[1] ))
        return mouse_pos[0], mouse_pos[1]