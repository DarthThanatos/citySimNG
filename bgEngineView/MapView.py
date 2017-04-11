import wx
import os


class MapViewCenterPart(wx.Panel):
    def __init__(self, parent, ID, tplSize, musicPath="TwoMandolins.mp3"):
        self.parent = parent
        self.ID = ID 
        self.tplSize = tplSize
        self.musicPath = musicPath
        wx.Panel.__init__(self, self.parent, self.ID, size=self.tplSize)

    def onShow(self, event):
        if event.GetShow():
            print "shown map"
            self.initView()
            try:        
                pygame.mixer.init()
                pygame.mixer.music.load(self.musicPath)
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
        self.color = (255, 0, 0)
        self.rect = (10, 10, 100, 100)
        window.fill(self.color, self.rect)
        self.color = (0, 255, 0)
        self.rect = (120, 10, 100, 100)
        window.fill(self.color, self.rect)
        self.color = (0, 0, 255)
        self.rect = (10, 120, 100, 100)
        window.fill(self.color, self.rect)
        self.color = (255, 255, 0)
        self.rect = (120, 120, 100, 100)
        window.fill(self.color, self.rect)
        pygame.display.flip()
        pygame.display.update()


class MapView(wx.Panel):
    def __init__(self, parent, size, name):  
        wx.Panel.__init__(self, parent=parent, size=size)
        self.name = name
        self.parent = parent

        self.initButtons()
        self.center = MapViewCenterPart(self, -1, (300, 300))
        self.Bind(wx.EVT_SHOW, self.center.onShow, self)
        #self.initMenuBar()

    def initButtons(self):
        # Add menu button
        menu_btn = wx.Button(self, label="Menu", pos=(300, 10), size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

    def retToMenu(self, event):
        self.parent.setView("Menu")

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
