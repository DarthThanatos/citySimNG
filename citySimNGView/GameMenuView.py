import wx
import os
import json
from RelativePaths import relative_music_path,relative_textures_path,relative_text_files_path

class GameMenuView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        wx.Panel.__init__(self, size=size, parent=parent)
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.parent = parent
        self.name = name
        self.size = size
        self.sender = sender

        self.musicPath = musicPath
        self.initMenu()
        self.SetBackgroundColour((255, 255, 255))

    def onShow(self, event):
        # print "Menu on show"
        global pygame
        if event.GetShow():
                print "menu shown"
                # print "menu: setting up music"
                import pygame
                print "Menu:", os.path.dirname(os.path.abspath(__file__))
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(
                    #os.path.dirname(os.path.abspath(__file__)) + "\\" +
                    self.musicPath)
                pygame.mixer.music.play()
        else:
            print "menu hidden"
            try:
                # print "Menu, quitting"
                pygame.quit()
            except Exception:
                # print "menu: problem with pygame quit"
                pass

    def initMenu(self):
        """ This function creates view for menu.
            It creates and sets position for header.
            It creates, binds and sets position for buttons."""
        buttonsSizer = wx.BoxSizer(wx.VERTICAL)
        
        with open(relative_text_files_path + "headerCS.txt", "r+") as headerFile:
            headerTxt = headerFile.read()
            print headerTxt

        # Load, add and set position for header
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerImage = wx.Image(relative_textures_path + "headerCS.jpg", wx.BITMAP_TYPE_JPEG)
        headerBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImage))
        headerSizer.Add(headerBmp)
        buttonsSizer.Add(headerSizer, 0, wx.CENTER)

        # Create buttons
        newgame_btn = wx.Button(self, label="New Game")
        tutorial_btn = wx.Button(self, label="Tutorial")
        exchange_btn = wx.Button(self, label="Exchange")
        ranking_btn = wx.Button(self, label="Ranking")
        load_btn = wx.Button(self, label="Load")
        save_btn = wx.Button(self, label="Save")
        loader_btn = wx.Button(self, label = "Back to Loader")

        # Set space between header and buttons
        buttonsSizer.AddSpacer(50)

        # Set buttons positions
        buttonsSizer.Add(newgame_btn, 0, wx.CENTER | wx.ALL, 5)
        buttonsSizer.Add(tutorial_btn, 0, wx.CENTER)
        buttonsSizer.Add(ranking_btn, 0, wx.CENTER)
        buttonsSizer.Add(exchange_btn, 0, wx.CENTER)
        buttonsSizer.Add(load_btn, 0, wx.CENTER)
        buttonsSizer.Add(save_btn, 0, wx.CENTER)
        buttonsSizer.Add(loader_btn, 0, wx.CENTER)

        # Add logic to buttons
        self.Bind(wx.EVT_BUTTON, self.moveToExchange, exchange_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToNewGame, newgame_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToTutorial, tutorial_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToRanking, ranking_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToLoader, loader_btn)

        self.SetSizer(buttonsSizer)
        buttonsSizer.SetDimension(0, 0, self.size[0], self.size[1])

    def mountMoveToMsg (self, target):
        msg = {}
        msg["To"] = "GameMenuNode"
        msg["Operation"] = "MoveTo"
        msg["Args"] = {}
        msg["Args"]["TargetView"] = target
        msg["Args"]["TargetControlNode"] = target + "Node"
        return json.dumps(msg)

    def moveToNewGame(self, event):
        """ This function switches to map view """
        #self.parent.setView("Map")
        msg = self.mountMoveToMsg("Map")
        self.sender.send(msg)
        #self.sender.send("MenuNode@MoveTo@MapNode")

    def moveToLoader(self, event):
        msg = self.mountMoveToMsg("Loader")
        self.sender.send(msg)

    def moveToExchange(self, event):
        """ This function switches to exchange view """
        #self.parent.setView("Exchange")
        msg = self.mountMoveToMsg("Exchange")
        self.sender.send(msg)
        #self.sender.send("MenuNode@MoveTo@ExchangeNode")

    def moveToTutorial(self, event):
        """ This function switches to tutorial view """
        #self.parent.setView("Tutorial")
        msg = self.mountMoveToMsg("Tutorial")
        self.sender.send(msg)
        #self.sender.send("MenuNode@MoveTo@TutorialNode")

    def moveToRanking(self, event):
        """ This function switches to tutorial view """
        #self.parent.setView("Ranking")
        msg = self.mountMoveToMsg("Ranking")
        self.sender.send(msg)
        #self.sender.send("MenuNode@MoveTo@RankingNode")

    def readMsg(self, msg):
        print "Menu view got msg", msg
