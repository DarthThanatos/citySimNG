import wx
import os
import re

RESOURCES_PANEL_POSITION = (0, 400)
RESOURCES_PANEL_SIZE = (300, 100)
RESOURCES_PANEL_COLOUR = (255, 255, 0)
RESOURCES_EXAMPLE = ["rock", "0", "gold", "0", "wood", "0"]


class MapViewCenterPart(wx.Panel):
    def __init__(self, parent, ID, tplSize, musicPath="TwoMandolins.mp3"):
        self.parent = parent
        self.tplSize = tplSize
        self.musicPath = musicPath
        wx.Panel.__init__(self, self.parent, size=self.tplSize)

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
        import pygame   # this has to happen after setting the environment variables.
        pygame.init()
        pygame.display.init()
        window = pygame.display.set_mode(self.tplSize)
        self.addRect(window, (255, 0, 0), (10, 10, 100, 100))
        self.addRect(window, (0, 255, 0), (120, 10, 100, 100))
        self.addRect(window, (0, 0, 255), (10, 120, 100, 100))
        self.addRect(window, (255, 255, 0), (120, 120, 100, 100))
        pygame.display.flip()
        pygame.display.update()

    def addRect(self, window, color, position):
        self.color = color
        self.rect = position
        window.fill(self.color, self.rect)

    def updateView(self):
        pygame.display.flip()
        pygame.display.update()


class MapViewResourcesPanel(wx.Panel):
    def __init__(self, parent, ID, panelPos, panelSize, musicPath="TwoMandolins.mp3"):
        self.parent = parent
        self.panelSize = panelSize
        self.musicPath = musicPath
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
    def __init__(self, parent, size, name, sender):
        wx.Panel.__init__(self, parent=parent, size=size)
        self.name = name
        self.parent = parent
        self.sender = sender

        # add buttons
        self.initButtons()

        # add center part
        self.center = MapViewCenterPart(self, -1, (300, 300))
        self.Bind(wx.EVT_SHOW, self.center.onShow, self)
        self.center.Show()

        # add resources panel
        self.resourcesPanel = MapViewResourcesPanel(self, -1, RESOURCES_PANEL_POSITION,
                                                    RESOURCES_PANEL_SIZE)
        self.resourcesPanel.Show()

    def initButtons(self):
        """ Function adding buttons """
        menu_btn = wx.Button(self, label="Menu", pos=(300, 500), size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

    def retToMenu(self, event):
        """ Menu button logic """
        self.sender.send("MapNode@MoveTo@MenuNode")

    def initMenuBar(self):
        status = self.CreateStatusBar()
        menuBar = wx.MenuBar()

        first = wx.Menu()
        second = wx.Menu()
        
        first.Append(wx.NewId(), "New window", "This is a new Window")
        first.Append(wx.NewId(), "Open...", "This will open a new Window")
        
        menuBar.Append(first, "File")
        menuBar.Append(second, "Edit")
        
        self.SetMenuBar(menuBar)

    def readMsg(self, msg):
        print "Map view got msg", msg
        values = msg
        import re
        values = re.split(',|{|}|=', values)
        values = [x for x in values if len(x) > 0]
        info = " ".join(values)
        self.resourcesPanel.updateResources(info)



