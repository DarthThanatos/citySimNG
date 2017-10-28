import json
#import traceback

import wx

from CreatorView.GraphsSpaces import GraphsSpaces
from TutorialPageView import TutorialPageView
from utils.RelativePaths import relative_music_path, relative_textures_path, relative_fonts_path


class TutorialView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        #ScrolledPanel.__init__(self, size=size, parent=parent, style=wx.SIMPLE_BORDER)
        wx.Panel.__init__(self, size=size, parent=parent)
        #TODO 
        
        self.name = name
        self.sender = sender

        self.size = size
        self.musicPath = musicPath

        #self.showGraph()
        #self.SetBackgroundColour((255, 255, 255))
        self.pageID = 0
        self.nrOfPages = 3
        self.tutorialInfo = "Welcome to our tutorial! If you'd like to find out what are all the functionalities of this cutting-edge game engine, you're in the right place :)"
        self.welcomeField = wx.StaticText(self, label=self.tutorialInfo)
        self.tutorialFont = wx.Font(20, wx.FONTFAMILY_DECORATIVE, 
            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.welcomeField.SetFont(self.tutorialFont)
        self.setName = ""
        self.centerSizer = wx.BoxSizer(wx.VERTICAL)

        #self.ctrlMsgField = wx.StaticText(self, label=self.tutorial_info[self.pageID])
        headerImg = wx.Image(relative_textures_path + "Tutorial.png", wx.BITMAP_TYPE_ANY)
        headerBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImg))
        
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerSizer.Add(headerBitmap)
        self.centerSizer.AddSpacer(10)
        self.centerSizer.Add(headerSizer, 0, wx.CENTER)
        self.centerSizer.AddSpacer(30)
        self.centerSizer.Add(self.welcomeField, 0, wx.CENTER)
        self.centerSizer.AddSpacer(10)
        self.content = [
            {
                'name': 'Gielda',
                'id': 1
            },
            {
                'name': 'Gielda - transakcje',
                'id': 2
            },
            {
                'name': 'Gielda - loteria',
                'id': 3
            },
        ]
        #ponizej graf zaleznosci - skierowany

        #page view
        self.pageView = TutorialPageView(self, size, "Tutorial Page")
        self.pageView.Hide()
        self.pageView.centerSizer.ShowItems(False)
        self.initContentList()
        self.graphsSpaces = GraphsSpaces(self)
        self.centerSizer.Add(self.graphsSpaces,0,wx.CENTER)
        self.centerSizer.SetDimension(0, 0, self.size[0], self.size[1])
        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def showPageView(self, event):
        self.requestPage(event)
        self.centerSizer.ShowItems(False)
        self.pageView.Show()
        self.pageView.centerSizer.ShowItems(True)


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
        # else:
        #     try:
        #         # print "Menu, quitting"
        #         pygame.quit()
        #     except Exception:
        #         # print "menu: problem with pygame quit"
        #         pass

    def initContentList(self):
        """ This function creates content list and buttons, sets theirs positions and size and
            binds logic to them."""
        leftBox = wx.BoxSizer(wx.VERTICAL)
        rightBox = wx.BoxSizer(wx.VERTICAL)
        contentBox = wx.BoxSizer(wx.HORIZONTAL)

        contentSize = len(self.content)
        contentHalf = contentSize // 2 + 1
        listFont = self.tutorialFont
        listFont.SetPointSize(18)

        arrow = wx.Bitmap(relative_textures_path+"rightGreenArrow.png", wx.BITMAP_TYPE_ANY)
        for i in range(contentHalf):
            elemField = wx.StaticText(self, label=self.content[i]['name'])
            elemID = self.content[i]['id']
            elemField.SetFont(listFont)
            arrowButton = wx.Button(self, id=elemID, label="  ", 
                size=(arrow.GetWidth()+10, arrow.GetHeight()+5))
            arrowButton.SetBitmap(arrow)
            self.Bind(wx.EVT_BUTTON, self.showPageView, arrowButton)
            tmpBox = wx.BoxSizer(wx.HORIZONTAL)
            tmpBox.Add(elemField, 0, wx.CENTER)
            tmpBox.AddSpacer(10)
            tmpBox.Add(arrowButton,0, wx.CENTER)
            leftBox.Add(tmpBox)
            leftBox.AddSpacer(20)

        
        for i in range(contentHalf, contentSize):
            elemField = wx.StaticText(self, label=self.content[i]['name'])
            elemID = self.content[i]['id']
            elemField.SetFont(listFont)
            arrowButton = wx.Button(self, id=elemID, label="  ", 
                size=(arrow.GetWidth()+10, arrow.GetHeight()+5))
            arrowButton.SetBitmap(arrow)
            self.Bind(wx.EVT_BUTTON, self.showPageView, arrowButton)
            tmpBox = wx.BoxSizer(wx.HORIZONTAL)
            tmpBox.Add(elemField, 0, wx.CENTER)
            tmpBox.AddSpacer(10)
            tmpBox.Add(arrowButton,0, wx.CENTER)
            rightBox.Add(tmpBox)
            rightBox.AddSpacer(20)
        contentBox.Add(leftBox)
        contentBox.AddSpacer(50)
        contentBox.Add(rightBox)
        self.centerSizer.Add(contentBox, 0, wx.CENTER) 
        self.centerSizer.AddSpacer(20)
        ln = wx.StaticLine(self, -1)
        self.centerSizer.Add(ln, 0, wx.EXPAND)

        menu_btn = wx.Button(self, label="Menu")
        self.centerSizer.AddSpacer(30)
        self.centerSizer.Add(menu_btn, 0, wx.CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

    def requestPage(self, event):
        print "TutorialView: requestPage executed"
        print "PageID: " + str(event.GetId())
        #sprawdzamy, czy Id jest prawidlowy, w razie czego poprawiamy
        realPageID = event.GetId()
        if realPageID > self.nrOfPages:
            realPageID = 1
        elif realPageID <= 0:
            realPageID = self.nrOfPages
        self.sender.entry_point.getTutorialPresenter().fetchTutorialPage(realPageID)
    

    def retToMenu(self, event):
        """ This function returns to Menu view """
        self.sender.entry_point.getTutorialPresenter().returnToMenu()

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

    def displayDependenciesGraph(self, jsonGraph):
        self.graphsSpaces.resetViewFromJSON(jsonGraph["Args"])
        self.centerSizer.Layout()

    def displayTutorialPage(self, jsonPage):
         pageContent = []
         args = jsonPage["Args"]["Page"]["page"]
         for x in args:
            subpageContent =[]
            subpageContent.append(x)    
            pageContent.append(subpageContent)
            pageContentString = pageContent[0][0]
            self.pageView.tutorialContent = pageContentString
            firstSubPage = pageContentString["sub0"]
            firstSubPageContent = ""
            for x in firstSubPage:
                firstSubPageContent += x
                firstSubPageContent += "\n"
            self.pageView.contentField.SetValue(firstSubPageContent)

            hyperlinks = pageContentString["link"]
            self.pageView.hyperlinks = hyperlinks

            image = wx.Image(pageContentString["img"], wx.BITMAP_TYPE_ANY)
            imgWidth = self.size[0] //2
            imgHeight = self.size[1]
            if imgWidth < image.GetWidth():
                #print "scale according to width"
                ratio = float(image.GetWidth()) / float(imgWidth)
                imgHeight = float(imgHeight) / ratio
                image.Rescale(imgWidth, int(imgHeight))
            if imgHeight < image.GetHeight():
                #print "scale according to height"
                ratio = float(image.GetHeight()) / float(imgHeight)
                imgWidth = float(imgWidth) / float(ratio)
                image.Rescale(int(imgWidth), imgHeight)
                
            self.pageView.helperImg = image
            self.pageView.subPage = 0
            self.pageView.nrOfSubpages = 2 #zmienic na len!!!
            self.pageView.page = pageContentString["nr"]
            self.pageView.updateHyperlinksAndImg()

    