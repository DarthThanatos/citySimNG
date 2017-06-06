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

        centerSizer = wx.BoxSizer(wx.VERTICAL)

        menu_btn = wx.Button(self, label="Menu")
        centerSizer.AddSpacer(30)
        centerSizer.Add(menu_btn, 0, wx.CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

        ctrlMsgField = wx.StaticText(self, label="Ranking")
        centerSizer.AddSpacer(20)
        centerSizer.Add(ctrlMsgField, 0, wx.CENTER)
        centerSizer.AddSpacer(15)

        simpleGrid = gridlib.Grid(self)
        simpleGrid.CreateGrid(len(self.usersList), 3)
        simpleGrid.SetColLabelValue(0, "User name")
        simpleGrid.SetColLabelValue(1, "Money")
        simpleGrid.SetColLabelValue(2, "Nr of games")

        print "Table will be filled"
        #print "dlugosc: " + str(len(self.usersList))
        #for i in range(len(self.usersList)):
      #      for j in range(3):
      #          value = str(self.usersList[i][j])
       #         print "wartosc: " + str(self.usersList[i][j])
                #simpleGrid.SetCellValue(i, j, value)
        simpleGrid.SetCellValue(0,0,"jakis")
        simpleGrid.SetCellValue(0,1,31301)
        simpleGrid.SetCellValue(0,2,1)
        simpleGrid.EnableEditing(False)
        centerSizer.Add(simpleGrid, 0, wx.CENTER)

        centerSizer.AddSpacer(30)
        ln = wx.StaticLine(self, -1)
        centerSizer.Add(ln, 0, wx.EXPAND)

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

        try:
            jsonObj = json.loads(msg)
            operation = jsonObj["Operation"]
            args = jsonObj["Args"]
            if operation == "FetchList":
                for x in args:
                    row = []
                    row.append(x["userName"])
                    row.append(x["money"])
                    row.append(x["nrOfGames"])

                    self.usersList.append(row)
               # print "self.usersList: \n"
                #print self.usersList
                self.initRanking()
            else:
                print "Unknown operation\n"

        except:
            traceback.print_exc()
            msg2 = {}
            msg2["To"] = "RankingNode"
            msg2["Operation"] = "MoveTo"
            msg2["Args"] = {}
            msg2["Args"]["TargetView"] = "GameMenu"
            msg2["Args"]["TargetControlNode"] = "GameMenuNode"
            self.sender.send(json.dumps(msg2))
