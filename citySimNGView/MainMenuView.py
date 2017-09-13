import json

import wx

from utils.ButtonsFactory import ButtonsFactory
from utils.JSONMonter import JSONMonter
from utils.OnShowUtil import OnShowUtil
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
        self.printHeader()
        self.initRootSizer()
        self.SetBackgroundColour((255, 255, 255))

    def printHeader(self):
        with open(relative_text_files_path + "headerCS.txt", "r+") as headerFile:
            headerTxt = headerFile.read()
            print headerTxt

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self.newHeaderSizer(), 0, wx.CENTER)
        rootSizer.AddSpacer(50)
        rootSizer.Add(self.newButtonsSizer(), 0, wx.CENTER)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])

    def newHeaderBmp(self):
        headerImage = wx.Image(relative_textures_path + "headerCS.jpg", wx.BITMAP_TYPE_JPEG)
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImage))

    def newHeaderSizer(self):
        self.headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.headerSizer.Add(self.newHeaderBmp())
        return self.headerSizer

    def newLoaderButton(self):
        self.loader_btn = ButtonsFactory().newButton(self, "Load and mount New Game", self.onGoToLoader)
        return self.loader_btn

    def newCreatorButton(self):
        self.creator_btn = ButtonsFactory().newButton(self, "Creator", self.onGoToCreator)
        return self.creator_btn

    def newExitButton(self):
        self.exit_btn = ButtonsFactory().newButton(self, "Exit", self.onExitSystem)
        return self.exit_btn

    def newButtonsSizer(self):
        self.buttons_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttons_vertical_sizer.Add(self.newLoaderButton(), 0, wx.CENTER | wx.ALL, 5)
        self.buttons_vertical_sizer.Add(self.newCreatorButton(), 0, wx.CENTER | wx.ALL)
        self.buttons_vertical_sizer.Add(self.newExitButton(), 0, wx.CENTER | wx.ALL, 5)
        return self.buttons_vertical_sizer

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

    def moveToLoader(self, event):
        """ This function switches to map view """
        msg = JSONMonter().mountMoveToMsg("MainMenuNode","Loader")
        self.sender.send(msg)

    def moveToCreator(self, event):
        """ This function switches to creator view """
        msg = JSONMonter().mountMoveToMsg("MainMenuNode","Creator")
        self.sender.send(msg)

    def onShow(self, event):
        OnShowUtil().switch_music_on_show_changed(event, self.musicPath)

    def readMsg(self, msg):
        pass
