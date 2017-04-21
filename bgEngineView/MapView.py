import wx
import os
import re
import thread


RESOURCES_PANEL_POSITION = (0, 400)
RESOURCES_PANEL_SIZE = (300, 100)
RESOURCES_PANEL_COLOUR = (255, 255, 0)
BUILDINGS_PANEL_SIZE = (400, 0, 100, 300)
BUILDINGS_PANEL_COLOUR = (255, 0, 255)
RESOURCES_EXAMPLE = ["rock", "0", "gold", "0", "wood", "0"]
LEFT = 1


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


class MapView(wx.Panel):
    sprites = []
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
                clicked_sprites = [s for s in self.sprites if s.rect.collidepoint(pos)]
                for sprite in clicked_sprites:
                    print "Clicked sprite " + sprite.to_string()

    def initButtons(self):
        """ Function adding buttons """
        menu_btn = wx.Button(self, label="Menu", pos=(300, 500), size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

    def retToMenu(self, event):
        """ Menu button logic """
        self.sender.send("MapNode@MoveTo@MenuNode")

    def readMsg(self, msg):
        print "Map view got msg", msg
        values = msg
        values = re.split(',|{|}|=', values)
        values = [x for x in values if len(x) > 0]
        info = " ".join(values)
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
        window = pygame.display.set_mode(self.size)
        self.addRect(window, (255, 0, 0), (10, 10, 100, 100))
        self.addRect(window, (0, 255, 0), (120, 10, 100, 100))
        self.addRect(window, (0, 0, 255), (10, 120, 100, 100))
        self.addRect(window, (255, 255, 0), (120, 120, 100, 100))
        self.addBuildingsPanel(window)
        self.addBuildingsToBuildingsPanel(window)
        pygame.display.flip()
        pygame.display.update()
        thread.start_new_thread(self.mouseListener, ())

    def addRect(self, window, color, position):
        window.fill(color, position)

    def addBuildingsPanel(self, window):
        self.addRect(window, BUILDINGS_PANEL_COLOUR, BUILDINGS_PANEL_SIZE)

    def addBuildingsToBuildingsPanel(self, window):
        self.sprites.append(Building(window, self))


import pygame


class Building(pygame.sprite.Sprite):
    def __init__(self, window, mapView):
        super(pygame.sprite.Sprite).__init__(pygame.sprite.Sprite)
        self.rect = pygame.Surface([50, 50]).get_rect(topleft=(400, 10))
        mapView.addRect(window, RESOURCES_PANEL_COLOUR, (400, 10, 50, 50))

    def to_string(self):
        return "ala ma kota"