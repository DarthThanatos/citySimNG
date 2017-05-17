import wx
import wx.grid as gridlib
from wx.lib.scrolledpanel import ScrolledPanel
import os
import json
import csv
from RelativePaths import relative_music_path

class RankingView(ScrolledPanel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        ScrolledPanel.__init__(self, size=size, parent=parent, style=wx.SIMPLE_BORDER)
        self.parent = parent
        self.name = name
        self.sender = sender

        self.size = size
        self.musicPath = musicPath

        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.SetupScrolling()

        with open('resources\\TextFiles\\users.csv', 'r') as f:
            reader = csv.reader(f)
            self.usersList = list(reader)

        self.initRanking()
        self.SetBackgroundColour((255, 255, 255))        

    def onShow(self, event):
        # print "Menu on show"
        global pygame
        if event.GetShow():
            # print "menu: setting up music"
            print "userList length is "+ str(self.usersList.__len__()) +"\n"
            import pygame
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(
                #os.path.dirname(os.path.abspath(__file__)) + "\\" +
                self.musicPath)
            pygame.mixer.music.play()
        else:
            try:
                # print "Menu, quitting"
                pygame.quit()
            except Exception:
                # print "menu: problem with pygame quit"
                pass

    def initRanking(self):
        """ This function creates view for ranking, sets essential buttons' properties - 
            positions and size. It also binds logic to them."""

        ranking_info = [
            "ranking"
            ]
        centerSizer = wx.BoxSizer(wx.VERTICAL)
        ctrlMsgField = wx.StaticText(self, label=ranking_info[0])
        centerSizer.Add(ctrlMsgField, 0, wx.CENTER)

        simpleGrid = gridlib.Grid(self)
        simpleGrid.CreateGrid(len(self.usersList), 3)
        simpleGrid.SetColLabelValue(0, "User name")
        simpleGrid.SetColLabelValue(1, "Money")
        simpleGrid.SetColLabelValue(2, "Nr of games")

        for i in range(len(self.usersList)):
            for j in range(3):
                simpleGrid.SetCellValue(i, j, self.usersList[i][j]) 
        simpleGrid.EnableEditing(False)
        centerSizer.Add(simpleGrid, 0, wx.CENTER)

        centerSizer.AddSpacer(30)
        ln = wx.StaticLine(self, -1)
        centerSizer.Add(ln, 0, wx.EXPAND)

        menu_btn = wx.Button(self, label="Menu")
        centerSizer.AddSpacer(30)
        centerSizer.Add(menu_btn, 0, wx.CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

        centerSizer.SetDimension(0, 0, self.size[0], self.size[1])
        self.SetSizer(centerSizer)


    def retToMenu(self, event):
        """ This function returns to Menu view """
        #self.parent.setView("Menu")
        #self.sender.send("RankingNode@MoveTo@MenuNode")
        msg = {}
        msg["To"] = "RankingNode"
        msg["Operation"] = "MoveTo"
        msg["Args"] = {}
        msg["Args"]["TargetView"] = "GameMenu"
        msg["Args"]["TargetControlNode"] = "GameMenuNode"
        self.sender.send(json.dumps(msg))

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
        print "Ranking view got msg", msg
