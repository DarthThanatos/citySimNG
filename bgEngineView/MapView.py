import wx
import os
import re
import thread
import json


RESOURCES_PANEL_POSITION = (0, 400)
RESOURCES_PANEL_SIZE = (300, 100)
RESOURCES_PANEL_COLOUR = (255, 255, 0)
BUILDINGS_PANEL_SIZE = (400, 0, 100, 300)
BUILDINGS_PANEL_COLOUR = (255, 0, 255)
RESOURCES_EXAMPLE = ["rock", "0", "gold", "0", "wood", "0"]
LEFT = 1
RIGHT = 3


class MapViewResourcesPanel(wx.Panel):
    def __init__(self, parent, ID, panelPos, panelSize):
        self.parent = parent
        self.panelSize = panelSize
        self.ID = ID

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

import pygame

class MapView(wx.Panel):
    sprites = []
    buildings_sprites = pygame.sprite.Group()
    buildings = []

    def __init__(self, parent, size, name, sender, musicPath="TwoMandolins.mp3"):
        wx.Panel.__init__(self, parent=parent, size=size)
        self.name = name
        self.parent = parent
        self.sender = sender
        self.musicPath = musicPath
        self.size = size

        self.Bind(wx.EVT_SHOW, self.onShow, self)

        # add buttons
        self.initButtons()

        # add resources panel
        self.resourcesPanel = MapViewResourcesPanel(self, -1, RESOURCES_PANEL_POSITION,
                                                    RESOURCES_PANEL_SIZE)
        self.resourcesPanel.Show()

    def mouseListener(self):
        while True:
            event = pygame.event.poll()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                pos = pygame.mouse.get_pos()
                print "You pressed the left mouse button"
                clicked_sprites = [s for s in self.buildings_sprites if s.rect.collidepoint(pos)]
                for sprite in clicked_sprites:
                    print "Clicked sprite " + sprite.name
                if len(clicked_sprites) > 0:
                    #background = pygame.Surface(self.window.get_size())
                    #background.fill((122, 0, 0))
                    sprite_is_chosen = True
                    building = clicked_sprites[0]
                    # shadow = Building(building.name, -1, building.sizeX, building.sizeY, self, pos)
                    # shadow_sprite = pygame.sprite.Group(shadow)
                    # shadow_sprite.draw(self.window)
                    # shadow_pos = pos
                    # shadow.update_position(shadow_pos, pos, self)
                    # shadow_sprite.update()
                    # pygame.display.update()
                    while sprite_is_chosen:
                        event = pygame.event.poll()
                        # pos = pygame.mouse.get_pos()
                        # shadow_pos = shadow.update_position(shadow_pos, pos, self)
                        # shadow_sprite.clear(self.window, background)
                        # shadow_sprite.update()
                        # shadow_sprite.draw(self.window)
                        # pygame.display.update()
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT:
                            pos = pygame.mouse.get_pos()
                            print "Mouse pos " + str(pos[0]) + " " + str(pos[1])
                            self.place_building(clicked_sprites[0], pos)
                            sprite_is_chosen = False

    def check_buildings_collision(self, new_building):
        """ Check if new building collides with some other one """
        for b in self.buildings_sprites.sprites():
            if pygame.sprite.collide_rect(b, new_building):
                return True
        return False

    def place_building(self, building, pos):
        # Create sprite for new building
        new_building = Building(building.name, -1, building.sizeX, building.sizeY, self, pos)
        if self.check_buildings_collision(new_building):
            print "Collision detected"
        else:
            # Send request to model to check if we can afford for this building
            self.sender.send("MapNode@PlaceBuilding@" + new_building.name)
            self.addRect(RESOURCES_PANEL_COLOUR, (pos[0], pos[1], new_building.sizeX, new_building.sizeY))
            self.buildings_sprites.add(new_building)
        pygame.display.update()

    def initButtons(self):
        """ Function adding buttons """
        menu_btn = wx.Button(self, label="Menu", pos=(300, 500), size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

    def retToMenu(self, event):
        """ Menu button logic """
        self.sender.send("MapNode@MoveTo@MenuNode")

    def readMsg(self, msg):
        print "Map view got msg", msg
        print msg
        dict = json.loads(msg)
        if "Buildings" in dict:
            self.buildings = dict["Buildings"]
            self.addBuildingsToBuildingsPanel()
        elif False:
            # case for building checking
            pass
        else:
            info = ""
            for (key, value) in dict.iteritems():
                info += key + " " + str(value) + " "
            self.resourcesPanel.updateResources(info)

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
        self.window = pygame.display.set_mode(self.size)
        self.addRect((255, 0, 0), (10, 10, 100, 100))
        self.addRect((0, 255, 0), (120, 10, 100, 100))
        self.addRect((0, 0, 255), (10, 120, 100, 100))
        self.addRect((255, 255, 0), (120, 120, 100, 100))
        self.addBuildingsPanel()
        pygame.display.flip()
        pygame.display.update()
        thread.start_new_thread(self.mouseListener, ())

    def addRect(self, color, position):
        self.window.fill(color, position)

    def addBuildingsPanel(self):
        self.addRect(BUILDINGS_PANEL_COLOUR, BUILDINGS_PANEL_SIZE)

    def addBuildingsToBuildingsPanel(self):
        for (i, b) in enumerate(self.buildings):
            # self.sprites.append(Building(b["name"], i, b["sizeX"], b["sizeY"], self))
            b_sprite = Building(b["name"], i, b["sizeX"], b["sizeY"], self)
            self.buildings_sprites.add(b_sprite)
            # b_sprite.draw()
        pygame.display.update()


import pygame


class Building(pygame.sprite.Sprite):

    def __init__(self, name, id, sizeX, sizeY, mapView, pos=()):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.id = id
        self.sizeX = sizeX
        self.sizeY = sizeY
        if len(pos) == 0:
            self.image = pygame.Surface([sizeX, sizeY])
            # self.image.fill(RESOURCES_PANEL_COLOUR)
            mapView.window.fill(RESOURCES_PANEL_COLOUR, (400 + id % 2 * 60, 10 + id / 2 * 60, sizeX, sizeY))
            self.rect = self.image.get_rect(topleft=(400 + id % 2 * 60, 10 + id / 2 * 60))
            # mapView.addRect(RESOURCES_PANEL_COLOUR, (400 + id % 2 * 60, 10 + id / 2 * 60, sizeX, sizeY))
        if len(pos) > 0:
            self.image = pygame.Surface([sizeX, sizeY])
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]))

    def update_position(self, pos, mouse_pos, mapView):
        self.rect = self.image.get_rect(topleft=(mouse_pos[0], mouse_pos[1] ))
        return mouse_pos[0], mouse_pos[1]