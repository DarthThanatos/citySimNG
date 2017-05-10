import wx
import os


import matplotlib
matplotlib.use("Agg")
import matplotlib.backends.backend_agg as agg
import pylab


class ExchangeViewCenterPart(wx.Panel):
    def __init__(self, parent, ID, tplSize, musicPath="music/TwoMandolins.mp3"):
        self.parent = parent
        self.ID = ID 
        self.tplSize = tplSize
        self.musicPath = musicPath
        wx.Panel.__init__(self, self.parent, self.ID, size=self.tplSize)

    def onShow(self, event):
        if event.GetShow(): 
            print "shown exchange"
            self.initView()
            try:        
                pygame.mixer.init()
                pygame.mixer.music.load(
                    #os.path.dirname(os.path.abspath(__file__))+ "\\" +
                    self.musicPath)
                pygame.mixer.music.play()
            except Exception:
                print "Problem with music"
        else:
            try:
                print "exch: quitting"
                pygame.quit()
            except Exception:
                print "first appearance of ExchangeView: pygame not initialized in exch"

    def initView(self):
        global pygame
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame   # this has to happen after setting the environment variables.
        pygame.init()
        pygame.display.init()
        window = pygame.display.set_mode(self.tplSize)
        print "exch: tplsize", self.tplSize
        self.color = (255, 0, 0)
        self.rect = (10, 10, 100, 100)
        window.fill(self.color, self.rect)
        pygame.display.flip()

        fig = pylab.figure(dpi=100, figsize=[3, 3])
        ax = fig.gca()
        ax.plot([1, 2, 4])
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        size = canvas.get_width_height()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        window.blit(surf, (0, 0))
        pygame.display.flip()


class ExchangeView(wx.Panel):
    def __init__(self, parent, size, name, sender):
        wx.Panel.__init__(self, parent=parent, size=size)
        self.name = name
        self.parent = parent
        self.sender = sender
        #self.center = ExchangeViewCenterPart(self, -1, (300, 300))

        self.initButtons()
        #self.Bind(wx.EVT_SHOW, self.center.onShow, self)
        #self.initMenuBar()

    def initButtons(self):
        """ This function creates buttons, sets theirs positions and size and
            binds logic to them."""
        menu_btn = wx.Button(self, label="Menu", pos=(300, 10), size=(60, 30))
        buy_btn = wx.Button(self, label="Buy", pos=(100, 300), size=(60, 30))
        sell_btn = wx.Button(self, label="Sell", pos=(160, 300), size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)
        self.Bind(wx.EVT_BUTTON, self.buyGoods, buy_btn)
        self.Bind(wx.EVT_BUTTON, self.sellGoods, sell_btn)

    def retToMenu(self, event):
        """ This function returns to Menu view """
        #self.parent.setView("Menu")
        self.sender.send("ExchangeNode@MoveTo@MenuNode")

    def buyGoods(self, event):
        pass

    def sellGoods(self, event):
        pass

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
        print "Exchange view got msg", msg
