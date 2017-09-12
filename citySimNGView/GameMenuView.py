import wx

from utils.PygameOnShowUtil import PygameOnShowUtil
from utils.JSONMonter import JSONMonter
from utils.RelativePaths import relative_music_path,relative_textures_path,relative_text_files_path

class GameMenuView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        wx.Panel.__init__(self, size=size, parent=parent)
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.parent = parent
        self.name = name
        self.size = size
        self.sender = sender
        self.musicPath = musicPath
        self.initMenu()

    def initMenu(self):
        """ This function creates view for menu.
            It creates and sets position for header.
            It creates, binds and sets position for buttons."""
        self.printHeader()
        self.initHeaderSizer()
        self.createButtons()
        self.bindButtons()
        self.initRootSizer()
        self.SetBackgroundColour((255, 255, 255))

    def bindButtons(self):
        # Add logic to buttons
        self.Bind(wx.EVT_BUTTON, self.goToExchange, self.exchange_btn)
        self.Bind(wx.EVT_BUTTON, self.goToNewGame, self.newgame_btn)
        self.Bind(wx.EVT_BUTTON, self.goToTutorial, self.tutorial_btn)
        self.Bind(wx.EVT_BUTTON, self.goToRanking, self.ranking_btn)
        self.Bind(wx.EVT_BUTTON, self.goToLoader, self.loader_btn)

    def goToExchange(self,event):
        self.sender.entry_point.getGameMenuPresenter().goToExchange()

    def goToNewGame(self, event):
        self.sender.entry_point.getGameMenuPresenter().goToNewGame()

    def goToTutorial(self, event):
        self.sender.entry_point.getGameMenuPresenter().goToTutorial()

    def goToRanking(self, event):
        self.sender.entry_point.getGameMenuPresenter().goToRanking()

    def goToLoader(self,event):
        self.sender.entry_point.getGameMenuPresenter().goToLoader()

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self.headerSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(50)
        rootSizer.Add(self.newgame_btn, 0, wx.CENTER | wx.ALL, 5)
        rootSizer.Add(self.tutorial_btn, 0, wx.CENTER)
        rootSizer.Add(self.ranking_btn, 0, wx.CENTER)
        rootSizer.Add(self.exchange_btn, 0, wx.CENTER)
        rootSizer.Add(self.load_btn, 0, wx.CENTER)
        rootSizer.Add(self.save_btn, 0, wx.CENTER)
        rootSizer.Add(self.loader_btn, 0, wx.CENTER)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])

    def initHeaderSizer(self):
        # Load, add and set position for header
        self.headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerImage = wx.Image(relative_textures_path + "headerCS.jpg", wx.BITMAP_TYPE_JPEG)
        headerBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImage))
        self.headerSizer.Add(headerBmp)

    def printHeader(self):
        with open(relative_text_files_path + "headerCS.txt", "r+") as headerFile:
            headerTxt = headerFile.read()
            print headerTxt

    def createButtons(self):
        self.newgame_btn = wx.Button(self, label="New Game")
        self.tutorial_btn = wx.Button(self, label="Tutorial")
        self.exchange_btn = wx.Button(self, label="Exchange")
        self.ranking_btn = wx.Button(self, label="Ranking")
        self.load_btn = wx.Button(self, label="Load")
        self.save_btn = wx.Button(self, label="Save")
        self.loader_btn = wx.Button(self, label="Back to Loader")

    def bindSocketButtons(self):
        # Add logic to buttons
        self.Bind(wx.EVT_BUTTON, self.moveToExchange, self.exchange_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToNewGame, self.newgame_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToTutorial, self.tutorial_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToRanking, self.ranking_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToLoader, self.loader_btn)

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

    def moveToRanking(self, event):
        """ This function switches to tutorial view """
        msg = JSONMonter().mountMoveToMsg("GameMenuNode", "Ranking")
        self.sender.send(msg)

    def onShow(self, event):
        PygameOnShowUtil(self.musicPath).switch_music_on_show_changed(event)

    def readMsg(self, msg):
        pass
