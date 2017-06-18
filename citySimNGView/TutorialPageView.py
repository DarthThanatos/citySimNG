import wx
import os
import json
from RelativePaths import relative_music_path, relative_textures_path

class TutorialPageView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        wx.Panel.__init__(self, size=size, parent=parent)
        self.parent = parent
        self.name = name
        self.sender = sender

        self.size = size
        self.musicPath = musicPath
        #self.SetBackgroundColour((255, 255, 255))
        self.subPage = 0
        self.nrOfSubpages = 3

        self.tutorialContent = [
        " Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac ex accumsan, commodo tortor a, rhoncus mauris. Mauris gravida vulputate tellus, nec ullamcorper augue pharetra non. Sed ut justo venenatis, ultrices mi gravida, commodo odio. Nulla eu fermentum sem. Proin lobortis dolor ac augue facilisis aliquam. Mauris condimentum metus purus. Duis condimentum sollicitudin diam eget tincidunt. Proin venenatis, lorem et finibus imperdiet, elit ex gravida augue, a rutrum libero odio commodo magna. Proin tempus nec nisi viverra tincidunt. Duis gravida laoreet bibendum. Nulla finibus purus ante. Maecenas sit amet pharetra tellus. Nam vitae velit quam. Duis vel tempus massa. Nam rhoncus sapien quis nulla dictum blandit varius vitae orci.",
        "Quisque congue fermentum dui. Proin et augue elementum, dignissim lectus sagittis, maximus urna. Aenean vel elit porta, mollis sem quis, iaculis erat. Aliquam quis odio at nunc tempus mollis eget nec quam. Donec in metus vulputate, egestas urna eu, interdum erat. Sed suscipit consequat ullamcorper. Sed ac dignissim arcu. Pellentesque placerat maximus turpis. Maecenas non ante tellus. Quisque vitae euismod arcu. Fusce ullamcorper gravida lacus, id porta neque scelerisque nec. Curabitur tortor nibh, maximus a nulla sit amet, ornare ullamcorper justo. Ut lectus dolor, finibus quis sodales eu, porta ut sapien. Aliquam ligula libero, rutrum a sapien et, scelerisque imperdiet mauris.",
        "Cras at tellus mi. Donec id venenatis magna, at consequat eros. Pellentesque ac magna egestas, consectetur nulla in, semper ligula. Aliquam porttitor consequat enim, sit amet semper mauris. Etiam cursus feugiat lacinia. Quisque suscipit feugiat dui ac aliquam. Quisque pellentesque vulputate orci vel semper. Ut congue sodales facilisis. Donec dui arcu, accumsan et accumsan id, cursus vel lectus. Maecenas est erat, sollicitudin ut metus molestie, sollicitudin ornare libero. Donec ac scelerisque tortor. Nam pretium erat ut aliquet laoreet. Cras nec turpis volutpat, suscipit nisi in, interdum massa. In feugiat arcu nibh, ut semper tellus ornare eget. Sed lobortis diam ut sapien facilisis, non volutpat sapien tristique."]

        self.contentField = wx.TextCtrl(parent = self, id=-1, 
            size=(self.size[0]//2-20, self.size[1]//2), 
            style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.contentField.SetValue(self.tutorialContent[self.subPage])

        self.tutorialPageFont = wx.Font(20, wx.FONTFAMILY_SCRIPT, 
            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.contentField.SetFont(self.tutorialPageFont)

        self.maxNrOfHyperlinks = 10
        self.hyperlinkCtrls = []
        self.hyperlinks = []
        self.Bind(wx.EVT_HYPERLINK, self.moveToPage, self)
        #nie wychodzi z eventem, strona sie laduje, a nie powinna xD
        

        self.centerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.topBtnSizer =  wx.BoxSizer(wx.HORIZONTAL)
        self.bottomBtnSizer = wx.BoxSizer(wx.HORIZONTAL)

        #all bitmaps for buttons
        leftArrow = wx.Bitmap(relative_textures_path + "leftBlueArrow.png", wx.BITMAP_TYPE_ANY)
        rightArrow = wx.Bitmap(relative_textures_path + "rightBlueArrow.png", wx.BITMAP_TYPE_ANY)
        leftLittleArrow = wx.Bitmap(relative_textures_path + "leftGreenArrow.png", wx.BITMAP_TYPE_ANY)
        rightLittleArrow = wx.Bitmap(relative_textures_path + "rightGreenArrow.png", wx.BITMAP_TYPE_ANY)
        contentsIcon = wx.Bitmap(relative_textures_path + "small_notepad2.png", wx.BITMAP_TYPE_ANY)
        
        #all needed buttons
        leftArrowBtn = wx.BitmapButton(self, bitmap=leftArrow,
            size=(leftArrow.GetWidth(), leftArrow.GetHeight()))
        rightArrowBtn = wx.BitmapButton(self, bitmap=rightArrow,
            size=(rightArrow.GetWidth(), rightArrow.GetHeight()))
        leftLittleArrowBtn = wx.BitmapButton(self, bitmap=leftLittleArrow,
            size=(leftLittleArrow.GetWidth(), leftLittleArrow.GetHeight()))
        rightLittleArrowBtn = wx.BitmapButton(self, bitmap=rightLittleArrow,
            size=(rightLittleArrow.GetWidth(), rightLittleArrow.GetHeight()))
        contentsBtn = wx.BitmapButton(self, bitmap=contentsIcon,
            size=(contentsIcon.GetWidth(), contentsIcon.GetHeight()))
        self.Bind(wx.EVT_BUTTON, self.showMainView, contentsBtn)
        self.Bind(wx.EVT_BUTTON, self.nextSubPage, rightLittleArrowBtn)
        self.Bind(wx.EVT_BUTTON, self.prevSubPage, leftLittleArrowBtn)

        #place for right image
        helperImg = wx.Image(relative_textures_path + "Grass.jpg", wx.BITMAP_TYPE_ANY)
        imgWidth = self.size[0] //2
        imgHeight = self.size[1]
        
        helperBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(helperImg), 
            size=(imgWidth, imgHeight))

        #place everything where needed
        self.rightSizer.Add(helperBitmap)
        self.topBtnSizer.Add(leftArrowBtn, 0, wx.CENTER)
        self.topBtnSizer.AddSpacer(10)
        self.topBtnSizer.Add(contentsBtn, 0, wx.CENTER)
        self.topBtnSizer.AddSpacer(10)
        self.topBtnSizer.Add(rightArrowBtn, 0, wx.CENTER)

        self.bottomBtnSizer.Add(leftLittleArrowBtn)
        self.bottomBtnSizer.AddSpacer(20)
        self.bottomBtnSizer.Add(rightLittleArrowBtn)

        self.leftSizer.AddSpacer(20)
        self.leftSizer.Add(self.topBtnSizer, 0, wx.CENTER)
        self.leftSizer.AddSpacer(15)
        self.leftSizer.Add(self.contentField, 0, wx.CENTER)
        self.leftSizer.AddSpacer(15)
        self.leftSizer.Add(self.bottomBtnSizer, 0, wx.CENTER)
        self.leftSizer.AddSpacer(15)

        self.hyperlinksBox = wx.BoxSizer(wx.HORIZONTAL)
        self.initHyperlinks()

        self.centerSizer.AddSpacer(10)
        self.centerSizer.Add(self.leftSizer)
        self.centerSizer.AddSpacer(10)
        self.centerSizer.Add(self.rightSizer)
        self.centerSizer.SetDimension(0, 0, self.size[0], self.size[1])

        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def moveToPage(self, event):
        #event.StopPropagation()
        print "Page will be changed\n"

    def showMainView(self, event):
        self.parent.Show()
        self.parent.centerSizer.ShowItems(True)
        self.Hide()

    def nextSubPage(self, event):
        self.subPage += 1
        if self.subPage >= self.nrOfSubpages:
            self.subPage = 0
        subPageName = "sub" + str(self.subPage)
        subPageContent = self.tutorialContent[subPageName]
        subPageString = ""
        for x in subPageContent:
            subPageString +=  x
            subPageString += "\n"
        self.contentField.SetValue(subPageString)

    def prevSubPage(self, event):
        self.subPage -= 1;
        if self.subPage < 0:
            self.subPage = self.nrOfSubpages-1
        subPageName = "sub" + str(self.subPage)
        subPageContent = self.tutorialContent[subPageName]
        subPageString = ""
        for x in subPageContent:
            subPageString +=  x
            subPageString += "\n"
        self.contentField.SetValue(subPageString)

    def initHyperlinks(self):
        hyperlinksFont = self.tutorialPageFont
        hyperlinksFont.SetPointSize(18)

        hyperlinksLabel = wx.StaticText(self, label="See also: ")
        hyperlinksLabel.SetFont(hyperlinksFont)
        self.hyperlinksBox.Add(hyperlinksLabel)

        for i in range(self.maxNrOfHyperlinks):  
            #hyperLabel ="link"+str(i)
            hyperlink = wx.HyperlinkCtrl(self, id=i, label="", url="")
            hyperlink.SetFont(hyperlinksFont)
            self.hyperlinkCtrls.append(hyperlink)

            space = wx.StaticText(self, label="\t")

            self.hyperlinksBox.Add(hyperlink)
            self.hyperlinksBox.Add(space)
        self.leftSizer.Add(self.hyperlinksBox)

    def updateHyperlinks(self):
        #self.hyperlinksBox.Hide()
        for i in range(len(self.hyperlinks)):
            child = self.hyperlinkCtrls[i]
            child.SetLabel(self.hyperlinks[i]['label'])
            child.SetId(self.hyperlinks[i]['id'])
        for i in range (len(self.hyperlinks), self.maxNrOfHyperlinks):
            child = self.hyperlinkCtrls[i]
            child.SetLabel("")
            child.SetId(-100)
        #self.hyperlinksBox.Show()
        self.centerSizer.Layout()

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

