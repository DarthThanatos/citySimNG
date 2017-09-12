import json

import wx

from utils.JSONMonter import JSONMonter
from utils.PygameOnShowUtil import PygameOnShowUtil
from utils.RelativePaths import relative_music_path, relative_textures_path, relative_text_files_path


class MainMenuView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender=None):
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
        self.addLogicToButtonsPy4J()
        self.initRootSizer()
        self.SetBackgroundColour((255, 255, 255))

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self.headerSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(50)
        self.addButtonsToSizer(rootSizer)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])

    def printHeader(self):
        with open(relative_text_files_path + "headerCS.txt", "r+") as headerFile:
            headerTxt = headerFile.read()
            print headerTxt

    def createButtons(self):
        # Create buttons
        self.newgame_btn = wx.Button(self, label="Load and mount New Game")
        self.creator_btn = wx.Button(self, label="Creator")
        self.exit_btn = wx.Button(self, label="Exit")

    def initHeaderSizer(self):
        self.headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerImage = wx.Image(relative_textures_path + "headerCS.jpg", wx.BITMAP_TYPE_JPEG)
        headerBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImage))
        self.headerSizer.Add(headerBmp)

    def addButtonsToSizer(self, buttonsSizer):
        # Set buttons positions
        buttonsSizer.Add(self.newgame_btn, 0, wx.CENTER | wx.ALL, 5)
        buttonsSizer.Add(self.creator_btn, 0, wx.CENTER | wx.ALL)
        buttonsSizer.Add(self.exit_btn, 0, wx.CENTER | wx.ALL, 5)

    def addLogicToButtonsSockets(self):
        # Add logic to buttons using plain sockets
        self.Bind(wx.EVT_BUTTON, self.closeButton, self.exit_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToCreator, self.creator_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToNewGame, self.newgame_btn)

    def addLogicToButtonsPy4J(self):
        # Add logic to buttons using Py4J API
        self.Bind(wx.EVT_BUTTON, self.onExitSystem, self.exit_btn)
        self.Bind(wx.EVT_BUTTON, self.onGoToCreator, self.creator_btn)
        self.Bind(wx.EVT_BUTTON, self.onGoToLoader, self.newgame_btn)

    def onGoToLoader(self, event):
        self.sender.entry_point.getMainMenuPresenter().goToLoader()

    def onGoToCreator(self, event):
        self.sender.entry_point.getMainMenuPresenter().goToCreator()

    def onExitSystem(self, event):
        self.sender.entry_point.getMainMenuPresenter().exitSystem()
        self.Close(True)
        self.parent.closeWindow(None)

    def closeButton(self, event):
        """ This function defines logic for exit button. """
        self.sender.send(json.dumps(JSONMonter().mountExitMsg()))
        self.Close(True)
        self.parent.closeWindow(None)

    def moveToNewGame(self, event):
        """ This function switches to map view """
        msg = JSONMonter().mountMoveToMsg("MainMenuNode","Loader")
        self.sender.send(msg)

    def moveToCreator(self, event):
        """ This function switches to creator view """
        msg = JSONMonter().mountMoveToMsg("MainMenuNode","Creator")
        self.sender.send(msg)

    def onShow(self, event):
        PygameOnShowUtil(self.musicPath).switch_music_on_show_changed(event)

    def readMsg(self, msg):
        pass
