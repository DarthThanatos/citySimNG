from uuid import uuid4

import wx

from CreatorView.GraphsSpaces import GraphsSpaces
from utils.ButtonsFactory import ButtonsFactory
from utils.JSONMonter import JSONMonter
from utils.OnShowUtil import OnShowUtil
from utils.RelativePaths import relative_music_path, relative_textures_path
from utils.SocketMsgReader.LoaderMsgReader import LoaderMsgReader


class LoaderView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender=None):
        wx.Panel.__init__(self, size=size, parent=parent)
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.parent = parent
        self.name = name
        self.size = size
        self.sender = sender
        self.ackMsgs = {}
        self.musicPath = musicPath
        self.initMainSizer()
        self.SetBackgroundColour((255, 255, 255))


    def initMainSizer(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.newHeaderSizer(), 0, wx.CENTER)
        mainSizer.Add(self.newRulesSelector(), 0, wx.CENTER)
        mainSizer.AddSpacer(50)
        mainSizer.Add(self.newButtonsSizer(), 0, wx.CENTER | wx.ALL, 5)
        mainSizer.AddSpacer(30)
        mainSizer.Add(self.newGraphSpaces(),0,wx.CENTER)
        self.SetSizer(mainSizer)
        mainSizer.SetDimension(0, 0, self.size[0], self.size[1])
        mainSizer.Layout()

    def newHeaderBmp(self):
        headerImage = wx.Image(relative_textures_path + "headerCS.jpg", wx.BITMAP_TYPE_JPEG)
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImage))

    def newHeaderSizer(self):
        # Load, add and set position for header
        self.headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.headerSizer.Add(self.newHeaderBmp())
        return self.headerSizer

    def newButtonsSizer(self):
        self.buttons_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.buttons_vertical_sizer.Add(self.newGameButton(), 0, wx.CENTER | wx.ALL, 15)
        self.buttons_vertical_sizer.Add(self.newShowGraphButton(), 0, wx.CENTER, 0)
        self.buttons_vertical_sizer.Add(self.newMenuButton(), 0, wx.CENTER, 0)
        return self.buttons_vertical_sizer

    def newRulesSelector(self):
        # Create dependencies selector
        self.ruleSetsList = []
        self.ruleSelector = wx.ListBox(self,  choices=self.ruleSetsList)
        return self.ruleSelector

    def newGraphSpaces(self):
        self.graphsSpaces = GraphsSpaces(self)
        return self.graphsSpaces

    def newGameButton(self):
        self.new_game_btn = ButtonsFactory().newButton(self, "Game Menu", self.goToNewGameMenu)
        return self.new_game_btn

    def newShowGraphButton(self):
        self.show_graph_btn = ButtonsFactory().newButton(self, "Show Graph", self.onShowGraphClicked)
        return self.show_graph_btn

    def newMenuButton(self):
        self.menu_btn = ButtonsFactory().newButton(self, "MainMenu", self.goToMenu)
        return self.menu_btn

    def goToMenu(self, event):
        self.sender.entry_point.getLoaderPresenter().goToMainMenu()

    def goToNewGameMenu(self, event):
        chosenSet = self.ruleSelector.GetStringSelection()
        if chosenSet == "": return
        self.sender.entry_point.getLoaderPresenter().selectDependenciesGraph(chosenSet)
        self.sender.entry_point.getLoaderPresenter().goToGameMenu()

    def onShowGraphClicked(self, event):
        chosenSet = self.ruleSelector.GetStringSelection()
        self.sender.entry_point.getLoaderPresenter().onShowGraph(chosenSet)

    def displayDependenciesGraph(self, jsonGraph):
        # input - jsonGraph : dict
        self.graphsSpaces.resetViewFromJSON(jsonGraph)

    def displayPossibleDependenciesSets(self, ruleSetsList):
        self.ruleSetsList = ruleSetsList
        self.ruleSelector.Set(self.ruleSetsList)

    def showGraph(self, evt):
        setChosen = self.ruleSelector.GetStringSelection()
        if setChosen == "": return
        self.sender.send(JSONMonter().mountShowGraphMsg(setChosen))

    def moveToNewGameMenu(self, event):
        setChosen = self.ruleSelector.GetStringSelection()
        if setChosen == "": return
        self.sendAndWaitSelectMsg(setChosen)
        self.moveToGameMenu()

    def sendAndWaitSelectMsg(self, setChosen):
        operationId = uuid4().__str__()
        self.ackMsgs[operationId] = False
        self.sender.send(JSONMonter().mountSelectMsg(setChosen, operationId))
        # wait for controller confirmation
        while not self.ackMsgs[operationId]: pass

    def moveToGameMenu(self):
        moveToMsg = JSONMonter().mountMoveToMsg("LoaderNode", "GameMenu")
        self.sender.send(moveToMsg)

    def moveToMenu(self, event):
        msg = JSONMonter().mountMoveToMsg("LoaderNode", "MainMenu")
        self.sender.send(msg)

    def onShow(self, event):
        OnShowUtil().switch_music_on_show_changed(event,self.musicPath)

    def readMsg(self, msg):
        LoaderMsgReader(self).reactOnMsg(msg)