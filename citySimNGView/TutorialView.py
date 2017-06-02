import wx
import os
import json
from wx.lib.scrolledpanel import ScrolledPanel
from RelativePaths import relative_music_path, relative_textures_path

class TutorialView(ScrolledPanel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        ScrolledPanel.__init__(self, size=size, parent=parent, style=wx.SIMPLE_BORDER)

        self.parent = parent
        self.name = name
        self.sender = sender

        self.size = size
        self.musicPath = musicPath
        #self.SetBackgroundColour((255, 255, 255))
        self.tutorialInfo = "Welcome to our tutorial! If you'd like to find out what are all the functionalities of this cutting-edge game engine, you're in the right place :)"
        self.welcomeField = wx.StaticText(self, label=self.tutorialInfo)

        self.centerSizer = wx.BoxSizer(wx.VERTICAL)

        #self.ctrlMsgField = wx.StaticText(self, label=self.tutorial_info[self.pageID])
        headerImg = wx.Image(relative_textures_path + "Tutorial.png", wx.BITMAP_TYPE_ANY)
        headerBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImg))
        
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerSizer.Add(headerBitmap)
        self.centerSizer.AddSpacer(10)
        self.centerSizer.Add(headerSizer, 0, wx.CENTER)
        self.centerSizer.AddSpacer(50)
        self.centerSizer.Add(self.welcomeField, 0, wx.CENTER)
        self.centerSizer.AddSpacer(20)
        self.content = [
            {
                'name': 'item1',
                'id': 1
            },
            {
                'name': 'item2',
                'id': 2
            },
            {
                'name': 'item3',
                'id': 3
            },
            {
                'name': 'item4',
                'id': 4
            },
            {
                'name': 'item5',
                'id': 5
            }
        ]
        #ponizej graf zaleznosci - skierowany
        self.initContentList()
        self.centerSizer.SetDimension(0, 0, self.size[0], self.size[1])

        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.SetupScrolling()
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

    def initContentList(self):
        """ This function creates content list and buttons, sets theirs positions and size and
            binds logic to them."""
        leftBox = wx.BoxSizer(wx.VERTICAL)
        rightBox = wx.BoxSizer(wx.VERTICAL)
        contentBox = wx.BoxSizer(wx.HORIZONTAL)
        arrow = wx.Bitmap(relative_textures_path+"rightGreenArrow.png", wx.BITMAP_TYPE_ANY)

        contentSize = len(self.content)
        contentHalf = contentSize // 2 + 1
        for i in range(contentHalf):
            elemField = wx.StaticText(self, label=self.content[i]['name'])
            arrowButton = wx.BitmapButton(self, bitmap=arrow, 
                size=(arrow.GetWidth(), arrow.GetHeight()))
            tmpBox = wx.BoxSizer(wx.HORIZONTAL)
            tmpBox.Add(elemField)
            tmpBox.AddSpacer(10)
            tmpBox.Add(arrowButton)
            leftBox.Add(tmpBox)
            leftBox.AddSpacer(20)

        
        for i in range(contentHalf, contentSize):
            elemField = wx.StaticText(self, label=self.content[i]['name'])
            arrowButton = wx.BitmapButton(self, bitmap=arrow, 
                size=(arrow.GetWidth(), arrow.GetHeight()))
            tmpBox = wx.BoxSizer(wx.HORIZONTAL)
            tmpBox.Add(elemField)
            tmpBox.AddSpacer(10)
            tmpBox.Add(arrowButton)
            rightBox.Add(tmpBox)
            rightBox.AddSpacer(20)
        contentBox.Add(leftBox)
        contentBox.AddSpacer(20)
        contentBox.Add(rightBox)
        self.centerSizer.Add(contentBox, 0, wx.CENTER) 
        self.centerSizer.AddSpacer(20)
        ln = wx.StaticLine(self, -1)
        self.centerSizer.Add(ln, 0, wx.EXPAND)

        menu_btn = wx.Button(self, label="Menu")
        self.centerSizer.AddSpacer(30)
        self.centerSizer.Add(menu_btn, 0, wx.CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

    def retToMenu(self, event):
        """ This function returns to Menu view """
        #self.parent.setView("Menu")
        #self.sender.send("TutorialNode@MoveTo@MenuNode")
        msg = {}
        msg["To"] = "TutorialNode"
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
        print "Tutorial view got msg", msg
