import wx
import wx.grid as gridlib
import os
import json
from RelativePaths import relative_music_path

class RankingView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        wx.Panel.__init__(self, size=size, parent=parent)
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.parent = parent
        self.name = name
        self.sender = sender

        self.size = size
        self.musicPath = musicPath
        self.initRanking()
        self.SetBackgroundColour((255, 255, 255))        

    def onShow(self, event):
        # print "Menu on show"
        global pygame
        if event.GetShow():
            # print "menu: setting up music"
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
        simpleGrid.CreateGrid(20, 3)
        simpleGrid.SetColLabelValue(0, "User")
        simpleGrid.SetColLabelValue(1, "Money")
        simpleGrid.SetColLabelValue(2, "Nr of games")
        centerSizer.Add(simpleGrid, 0, wx.CENTER)

        menu_btn = wx.Button(self, label="Menu")
        centerSizer.AddSpacer(50)
        centerSizer.Add(menu_btn, 0, wx.CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

        self.SetSizer(centerSizer)
        centerSizer.SetDimension(0, 0, self.size[0], self.size[1])



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
