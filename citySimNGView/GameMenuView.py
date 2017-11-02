import wx

from CurrentPricesPanel import CurrentPricesPanel
from utils import LogMessages
from utils.ButtonsFactory import ButtonsFactory
from utils.OnShowUtil import OnShowUtil
from utils.JSONMonter import JSONMonter
from utils.RelativePaths import relative_music_path,relative_textures_path

class GameMenuView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        wx.Panel.__init__(self, size=size, parent=parent)
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.parent = parent
        self.name = name
        self.size = size
        self.sender = sender
        self.musicPath = musicPath
        self.initRootSizer()
        self.SetBackgroundColour((0, 0, 0))

    def goToExchange(self,event):
        self.sender.entry_point.getGameMenuPresenter().goToExchange()

    def goToNewGame(self, event):
        self.sender.entry_point.getGameMenuPresenter().goToNewGame()

    def goToTutorial(self, event):
        self.sender.entry_point.getGameMenuPresenter().goToTutorial()

    def goToLoader(self,event):
        self.sender.entry_point.getGameMenuPresenter().goToLoader()

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self.newHeaderSizer(), 0, wx.CENTER)
        rootSizer.AddSpacer(50)
        rootSizer.Add(self.newCurrentPricesPanel(),  0, wx.CENTER)
        rootSizer.AddSpacer(50)
        rootSizer.Add(self.newButtonsSizer(), 0, wx.CENTER)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])

    def newCurrentPricesPanel(self):
        self.currentPricesPanel = CurrentPricesPanel(self)
        return self.currentPricesPanel

    def newHeaderBmp(self):
        headerImage = wx.Image(relative_textures_path + "headerCS_black.png", wx.BITMAP_TYPE_PNG)
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImage))

    def newHeaderSizer(self):
        # Load, add and set position for header
        self.headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.headerSizer.Add(self.newHeaderBmp())
        return self.headerSizer

    def newButtonsSizer(self):
        self.buttons_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttons_vertical_sizer.Add(self.newGameButton(), 0, wx.CENTER | wx.ALL, 15)
        self.buttons_vertical_sizer.Add(self.newTutorialButton(), 0, wx.CENTER, 0)
        self.buttons_vertical_sizer.Add(self.newExchangeButton(), 0, wx.CENTER, 0)
        self.buttons_vertical_sizer.Add(self.newLoadButton(), 0, wx.CENTER, 0)
        self.buttons_vertical_sizer.Add(self.newSaveButton(), 0, wx.CENTER, 0)
        self.buttons_vertical_sizer.Add(self.newLoaderButton(), 0, wx.CENTER, 0)
        return self.buttons_vertical_sizer

    def newGameButton(self):
        self.newgame_btn = ButtonsFactory().newButton(self, "Game", self.goToNewGame, hint = LogMessages.GAME_BTN_HINT, size=(100,-1))
        return self.newgame_btn

    def newTutorialButton(self):
        self.tutorial_btn = ButtonsFactory().newButton(self, "Tutorial", self.goToTutorial, hint = LogMessages.TUTORIAL_BTN_HINT, size=(100,-1))
        return self.tutorial_btn

    def newExchangeButton(self):
        self.exchange_btn = ButtonsFactory().newButton(self, "Exchange", self.goToExchange, hint = LogMessages.EXCHANGE_BTN_HINT, size=(100,-1))
        return self.exchange_btn

    def newLoadButton(self):
        self.load_btn =  ButtonsFactory().newButton(self, "Load", size=(100,-1))
        return self.load_btn

    def newSaveButton(self):
        self.save_btn =  ButtonsFactory().newButton(self, "Save", size=(100,-1))
        return self.save_btn

    def newLoaderButton(self):
        self.loader_btn = ButtonsFactory().newButton(self, "Back to Loader", self.goToLoader, hint = LogMessages.MENU_BTN_HINT, size=(100,-1))
        return self.loader_btn

    def moveToNewGame(self, event):
        """ This function switches to map view """
        msg = JSONMonter().mountMoveToMsg("GameMenuNode", "Map")
        self.sender.send(msg)

    def moveToLoader(self, event):
        msg = JSONMonter().mountMoveToMsg("GameMenuNode", "Loader")
        self.sender.send(msg)

    def moveToExchange(self, event):
        """ This function switches to exchange view """
        msg = JSONMonter().mountMoveToMsg("GameMenuNode", "Exchange")
        self.sender.send(msg)

    def moveToTutorial(self, event):
        """ This function switches to tutorial view """
        msg = JSONMonter().mountMoveToMsg("GameMenuNode", "Tutorial")
        self.sender.send(msg)

    def onShow(self, event):
        OnShowUtil().switch_music_on_show_changed(event, self.musicPath)
        if not event.GetShow(): self.currentPricesPanel.cleanup()

    def animateCurrentPrices(self, currentPricesDict):
        self.currentPricesPanel.animateCurrentPrices(currentPricesDict)

    def readMsg(self, msg):
        pass
