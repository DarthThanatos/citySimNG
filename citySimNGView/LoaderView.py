import wx
import json
from uuid import uuid4
from RelativePaths import relative_music_path, relative_textures_path
from CreatorView.GraphsSpaces import GraphsSpaces

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
        self.initLoader()

    def onShow(self, event):
        global pygame
        if event.GetShow():
            import pygame
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(
                self.musicPath)
            pygame.mixer.music.play()
        else:
            try:
                pygame.quit()
            except Exception:
                pass

    def initLoader(self):
        self.initHeaderSizer()
        self.initRulesSelector()
        self.createButtons()
        # self.bindSocketButtons()
        self.bindButtons()
        self.initGraphSpaces()
        self.initMainSizer()
        self.SetBackgroundColour((255, 255, 255))

    def initHeaderSizer(self):
        # Load, add and set position for header
        self.headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerImage = wx.Image(relative_textures_path + "headerCS.jpg", wx.BITMAP_TYPE_JPEG)
        headerBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImage))
        self.headerSizer.Add(headerBmp)

    def initRulesSelector(self):
        # Create dependencies selector
        self.ruleSetsList = []
        self.ruleSelector = wx.ListBox(self,  choices=self.ruleSetsList)

    def initGraphSpaces(self):
        self.graphsSpaces = GraphsSpaces(self)

    def createButtons(self):
        self.menu_btn = wx.Button(self, label="Main Menu")
        self.new_game_btn = wx.Button(self, label = "New Game Menu")
        self.show_graph_btn = wx.Button(self, label = "Show Graph")

    def initMainSizer(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.headerSizer, 0, wx.CENTER)
        mainSizer.Add(self.ruleSelector, 0, wx.CENTER)
        mainSizer.AddSpacer(50)
        mainSizer.Add(self.new_game_btn, 0, wx.CENTER | wx.ALL, 5)
        mainSizer.Add(self.show_graph_btn, 0, wx.CENTER)
        mainSizer.Add(self.menu_btn, 0, wx.CENTER | wx.ALL, 5)
        mainSizer.AddSpacer(30)
        mainSizer.Add(self.graphsSpaces,0,wx.CENTER)
        self.SetSizer(mainSizer)
        mainSizer.SetDimension(0, 0, self.size[0], self.size[1])
        mainSizer.Layout()

    def bindButtons(self):
        self.Bind(wx.EVT_BUTTON, self.goToMenu, self.menu_btn)
        self.Bind(wx.EVT_BUTTON, self.goToNewGameMenu, self.new_game_btn)
        self.Bind(wx.EVT_BUTTON, self.onShowGraphClicked, self.show_graph_btn)

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

    def bindSocketButtons(self):
        self.Bind(wx.EVT_BUTTON, self.moveToMenu, self.menu_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToNewGameMenu, self.new_game_btn)
        self.Bind(wx.EVT_BUTTON, self.showGraph, self.show_graph_btn)

    def showGraph(self, evt):
        setChosen = self.ruleSelector.GetStringSelection()
        print "SetChosen:",setChosen
        if setChosen == "": return

        msg = {}
        msg["To"] = "LoaderNode"
        msg["Operation"] = "ShowGraph"
        msg["Args"] = {}
        msg["Args"]["SetChosen"] = setChosen
        self.sender.send(json.dumps(msg))

    def mountMoveToMsg (self, target):
        msg = {}
        msg["To"] = "LoaderNode"
        msg["Operation"] = "MoveTo"
        msg["Args"] = {}
        msg["Args"]["TargetView"] = target
        msg["Args"]["TargetControlNode"] = target + "Node"
        return json.dumps(msg)

    def moveToNewGameMenu(self, event):
        setChosen = self.ruleSelector.GetStringSelection()
        print "SetChosen:",setChosen
        if setChosen == "": return
        operationId = uuid4().__str__()
        self.ackMsgs[operationId] = False
        msg = {}
        msg["To"] = "LoaderNode"
        msg["Operation"] = "Select"
        msg["Args"] = {}
        msg["Args"]["SetChosen"] = setChosen
        msg["Args"]["UUID"] = operationId
        self.sender.send(json.dumps(msg))
        while not self.ackMsgs[operationId]: pass
        print "Select block ended"
        # ^ wait for controller confirmation
        moveToMsg = self.mountMoveToMsg("GameMenu")
        self.sender.send(moveToMsg)

    def moveToMenu(self, event):
        msg = self.mountMoveToMsg("MainMenu")
        self.sender.send(msg)

    def readMsg(self, msg):
        msgObj = json.loads(msg)
        operation = msgObj["Operation"]
        if operation == "Init":
            ruleSetsList = msgObj["Args"]["DependenciesNames"]
            self.displayPossibleDependenciesSets(ruleSetsList)
        if operation == "SelectConfirm":
            operationId = msgObj["Args"]["UUID"]
            self.ackMsgs[operationId] = True
        if operation == "ShowGraphRes":
            self.displayDependenciesGraph(msgObj["Args"]["Graph"])