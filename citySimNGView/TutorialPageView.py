import wx
import os
import json
from wx.lib.scrolledpanel import ScrolledPanel
from RelativePaths import relative_music_path, relative_textures_path

class TutorialPageView(ScrolledPanel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        ScrolledPanel.__init__(self, size=size, parent=parent, style=wx.SIMPLE_BORDER)
        #pozniej w inicie trzeba bedzie dostarczyc pierwszy indeks danych, jaki ma sie wyswietlic
        #dane beda jakims jsonem, osobno importowanym (ale tylko tu)

        self.parent = parent
        self.name = name
        self.sender = sender

        self.size = size
        self.musicPath = musicPath
        #self.SetBackgroundColour((255, 255, 255))
        self.pageID = 0
        self.tutorialContent = [
        " Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac ex accumsan, commodo tortor a, rhoncus mauris. Mauris gravida vulputate tellus, nec ullamcorper augue pharetra non. Sed ut justo venenatis, ultrices mi gravida, commodo odio. Nulla eu fermentum sem. Proin lobortis dolor ac augue facilisis aliquam. Mauris condimentum metus purus. Duis condimentum sollicitudin diam eget tincidunt. Proin venenatis, lorem et finibus imperdiet, elit ex gravida augue, a rutrum libero odio commodo magna. Proin tempus nec nisi viverra tincidunt. Duis gravida laoreet bibendum. Nulla finibus purus ante. Maecenas sit amet pharetra tellus. Nam vitae velit quam. Duis vel tempus massa. Nam rhoncus sapien quis nulla dictum blandit varius vitae orci.",
        "Quisque congue fermentum dui. Proin et augue elementum, dignissim lectus sagittis, maximus urna. Aenean vel elit porta, mollis sem quis, iaculis erat. Aliquam quis odio at nunc tempus mollis eget nec quam. Donec in metus vulputate, egestas urna eu, interdum erat. Sed suscipit consequat ullamcorper. Sed ac dignissim arcu. Pellentesque placerat maximus turpis. Maecenas non ante tellus. Quisque vitae euismod arcu. Fusce ullamcorper gravida lacus, id porta neque scelerisque nec. Curabitur tortor nibh, maximus a nulla sit amet, ornare ullamcorper justo. Ut lectus dolor, finibus quis sodales eu, porta ut sapien. Aliquam ligula libero, rutrum a sapien et, scelerisque imperdiet mauris.",
        "Cras at tellus mi. Donec id venenatis magna, at consequat eros. Pellentesque ac magna egestas, consectetur nulla in, semper ligula. Aliquam porttitor consequat enim, sit amet semper mauris. Etiam cursus feugiat lacinia. Quisque suscipit feugiat dui ac aliquam. Quisque pellentesque vulputate orci vel semper. Ut congue sodales facilisis. Donec dui arcu, accumsan et accumsan id, cursus vel lectus. Maecenas est erat, sollicitudin ut metus molestie, sollicitudin ornare libero. Donec ac scelerisque tortor. Nam pretium erat ut aliquet laoreet. Cras nec turpis volutpat, suscipit nisi in, interdum massa. In feugiat arcu nibh, ut semper tellus ornare eget. Sed lobortis diam ut sapien facilisis, non volutpat sapien tristique."]
        self.contentField = wx.StaticText(self, label=self.tutorialContent[self.pageID])

        self.centerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftSizer = wx.BoxSizer(wx.VERTICAL)

        #all bitmaps for buttons
        leftArrow = wx.Bitmap(relative_textures_path + "leftBlueArrow.png", wx.BITMAP_TYPE_ANY)
        rightArrow = wx.Bitmap(relative_textures_path + "rightBlueArrow.png", wx.BITMAP_TYPE_ANY)
        leftLittleArrow = wx.Bitmap(relative_textures_path + "leftGreenArrow.png", wx.BITMAP_TYPE_ANY)
        rightLittleArrow = wx.Bitmap(relative_textures_path + "rightGreenArrow.png", wx.BITMAP_TYPE_ANY)
        contentsImg = wx.Bitmap(relative_textures_path + "small_notepad2.png", wx.BITMAP_TYPE_ANY)
        
        #all needed buttons
        leftArrowBtn = wx.BitmapButton(self, bitmap=leftArrow,
            size=(leftArrow.GetWidth(), leftArrow.GetHeight()))
        rightArrowBtn = wx.BitmapButton(self, bitmap=rightArrow,
            size=(rightArrow.GetWidth(), rightArrow.GetHeight()))
        leftLittleArrowBtn = wx.BitmapButton(self, bitmap=leftLittleArrow,
            size=(leftLittleArrow.GetWidth(), leftLittleArrow.GetHeight()))
        rightLittleArrowBtn = wx.BitmapButton(self, bitmap=rightLittleArrow,
            size=(rightLittleArrow.GetWidth(), rightLittleArrow.GetHeight()))
        contentsBtn = wx.BitmapButton(self, bitmap=contentsImg,
            size=(contentsImg.GetWidth(), contentsImg.GetHeight()))

        #place for right image
        helperImg = wx.Image(relative_textures_path + "Grass.jpg", wx.BITMAP_TYPE_ANY)
        helperBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(helperImg))


        
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerSizer.Add(headerBitmap)
        self.centerSizer.Add(headerSizer, 0, wx.CENTER)
        self.centerSizer.AddSpacer(80)
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
