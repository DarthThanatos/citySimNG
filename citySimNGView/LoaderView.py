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
        self.SetBackgroundColour((255, 255, 255))

    def initLoader(self):
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # Load, add and set position for header
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerImage = wx.Image(relative_textures_path + "headerCS.jpg", wx.BITMAP_TYPE_JPEG)
        headerBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImage))
        headerSizer.Add(headerBmp)
        mainSizer.Add(headerSizer, 0, wx.CENTER)

        # Create dependencies selector
        self.ruleSetsList = []
        self.ruleSelector = wx.ListBox(self,  choices=self.ruleSetsList)
        mainSizer.Add(self.ruleSelector, 0, wx.CENTER)
        # Set space between dialog and exit button
        mainSizer.AddSpacer(50)

        menu_btn = wx.Button(self, label="Main Menu")
        new_game_btn = wx.Button(self, label = "New Game Menu")
        show_graph_btn = wx.Button(self, label = "Show Graph")

        self.Bind(wx.EVT_BUTTON, self.moveToMenu, menu_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToNewGameMenu, new_game_btn)
        self.Bind(wx.EVT_BUTTON, self.showGraph, show_graph_btn)

        mainSizer.Add(new_game_btn, 0, wx.CENTER | wx.ALL, 5)
        mainSizer.Add(show_graph_btn, 0, wx.CENTER)
        mainSizer.Add(menu_btn, 0, wx.CENTER | wx.ALL, 5)

        mainSizer.AddSpacer(30)
        self.graphsSpaces = GraphsSpaces(self)
        mainSizer.Add(self.graphsSpaces,0,wx.CENTER)

        self.SetSizer(mainSizer)
        mainSizer.SetDimension(0, 0, self.size[0], self.size[1])
        mainSizer.Layout()

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
            self.ruleSetsList = ruleSetsList
            self.ruleSelector.Set(self.ruleSetsList)
        if operation == "SelectConfirm":
            operationId = msgObj["Args"]["UUID"]
            self.ackMsgs[operationId] = True
        if operation == "ShowGraphRes":
            self.graphsSpaces.resetViewFromJSON(msgObj["Args"]["Graph"])

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