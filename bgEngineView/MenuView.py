import wx
import os


class MenuView(wx.Panel):
    def __init__(self, parent, size, name, musicPath="TwoMandolins.mp3", sender = None):
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
                pygame.mixer.music.load(os.path.dirname(os.path.abspath(__file__)) + "\\" + self.musicPath)
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
        
        with open("header.txt", "r+") as headerFile:
            headerTxt = headerFile.read()
            print headerTxt

        # Load, add and set position for header
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerImage = wx.Image("header.jpg", wx.BITMAP_TYPE_JPEG)
        headerBmp = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImage))
        headerSizer.Add(headerBmp)
        buttonsSizer.Add(headerSizer, 0, wx.CENTER)

        # Create buttons
        newgame_btn = wx.Button(self, label="New Game")
        creator_btn = wx.Button(self, label="Creator")
        tutorial_btn = wx.Button(self, label="Tutorial")
        exchange_btn = wx.Button(self, label="Exchange")
        load_btn = wx.Button(self, label="Load")
        save_btn = wx.Button(self, label="Save")
        exit_btn = wx.Button(self, label="Exit")

        # Set space between header and buttons
        buttonsSizer.AddSpacer(50)

        # Set buttons positions
        buttonsSizer.Add(newgame_btn, 0, wx.CENTER | wx.ALL, 5)
        buttonsSizer.Add(creator_btn, 0, wx.CENTER | wx.ALL)
        buttonsSizer.Add(tutorial_btn, 0, wx.CENTER)
        buttonsSizer.Add(exchange_btn, 0, wx.CENTER)
        buttonsSizer.Add(load_btn, 0, wx.CENTER)
        buttonsSizer.Add(save_btn, 0, wx.CENTER)
        buttonsSizer.Add(exit_btn, 0, wx.CENTER | wx.ALL, 5)

        # Add logic to buttons
        self.Bind(wx.EVT_BUTTON, self.closeButton, exit_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToCreator, creator_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToExchange, exchange_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToNewGame, newgame_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToTutorial, tutorial_btn)

        self.SetSizer(buttonsSizer)
        buttonsSizer.SetDimension(0, 0, self.size[0], self.size[1])

    def closeButton(self, event):
        """ This function defines logic for exit button. """
        self.sender.send("MenuNode@Exit")
        self.Close(True)
        self.parent.closeWindow(None)

    def moveToNewGame(self, event):
        """ This function switches to map view """
        #self.parent.setView("Map")
        self.sender.send("MenuNode@MoveTo@MapNode")

    def moveToCreator(self, event):
        """ This function switches to creator view """
        #self.parent.setView("Creator")
        self.sender.send("MenuNode@MoveTo@CreatorNode")

    def moveToExchange(self, event):
        """ This function switches to exchange view """
        #self.parent.setView("Exchange")
        self.sender.send("MenuNode@MoveTo@ExchangeNode")

    def moveToTutorial(self, event):
        """ This function switches to tutorial view """
        #self.parent.setView("Tutorial")
        self.sender.send("MenuNode@MoveTo@TutorialNode")

    def readMsg(self, msg):
        print "Menu view got msg", msg
