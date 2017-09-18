import json

import wx
import wx.grid as gridlib

from utils.RelativePaths import relative_music_path


class RankingView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        #ScrolledPanel.__init__(self, size=size, parent=parent, style=wx.SIMPLE_BORDER)
        wx.Panel.__init__(self, size=size, parent=parent)
        self.parent = parent
        self.name = name
        self.sender = sender

        self.size = size
        self.musicPath = musicPath

        self.usersList = []

        self.labelFont =  wx.Font(19, wx.FONTFAMILY_SCRIPT, 
        wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.rankingFont = wx.Font(18, wx.FONTFAMILY_SCRIPT, 
        wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        

        self.centerSizer = wx.BoxSizer(wx.VERTICAL)

        self.centerSizer.AddSpacer(10)
        menu_btn = wx.Button(self, label="Menu")
        self.centerSizer.AddSpacer(10)
        self.centerSizer.Add(menu_btn, 0, wx.CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

        self.centerSizer.AddSpacer(10)
        ln = wx.StaticLine(self, -1)
        self.centerSizer.Add(ln, 0, wx.EXPAND)

        ctrlMsgField = wx.StaticText(self, label="Ranking")
        self.centerSizer.AddSpacer(20)
        self.centerSizer.Add(ctrlMsgField, 0, wx.CENTER)
        self.centerSizer.AddSpacer(15)

        self.simpleGrid = gridlib.Grid(self)
        self.simpleGrid.CreateGrid(len(self.usersList), 3)
        self.simpleGrid.SetColLabelValue(0, "User name")
        self.simpleGrid.SetColLabelValue(1, "Money")
        self.simpleGrid.SetColLabelValue(2, "Nr of games")
        self.simpleGrid.SetLabelFont(self.labelFont)
        self.simpleGrid.SetDefaultCellFont(self.rankingFont)

        self.centerSizer.Add(self.simpleGrid, 0, wx.CENTER)
        gridHeight = self.size[1]-180
        self.simpleGrid.SetMaxSize(wx.Size(self.size[0], gridHeight))
        self.centerSizer.Layout()
    
        self.centerSizer.SetDimension(0, 0, self.size[0], self.size[1])
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        #self.SetupScrolling()

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
        print "Table will be filled"
        self.simpleGrid.Hide()
        nrOfRows = self.simpleGrid.GetNumberRows()
        for i in range(nrOfRows):
            self.simpleGrid.DeleteRows()

        print "len: " + str(len(self.usersList)) + "\n"
        for i in range(len(self.usersList)):
            self.simpleGrid.AppendRows()
            for j in range(3):
                value = str(self.usersList[i][j])
                self.simpleGrid.SetCellValue(i, j, value)

        self.simpleGrid.AutoSizeColumns()
        self.simpleGrid.AutoSizeRows()
        self.simpleGrid.ShowScrollbars(wx.SHOW_SB_NEVER,wx.SHOW_SB_DEFAULT)
        self.simpleGrid.DisableDragGridSize()
        self.simpleGrid.DisableDragRowSize()
        self.simpleGrid.DisableDragColSize()
        self.simpleGrid.DisableDragColMove()
        self.simpleGrid.EnableEditing(False)
        self.simpleGrid.Show()
        self.centerSizer.Layout()


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
            self.usersList = []
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
