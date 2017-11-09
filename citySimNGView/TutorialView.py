import json
#import traceback
import wx
from py4j.java_collections import JavaList, JavaArray

from CreatorView.GraphsSpaces import GraphsSpaces
from TutorialPageView import TutorialPageView
from utils.RelativePaths import relative_music_path, relative_textures_path, relative_fonts_path


class MainTab(wx.Panel):
    def __init__(self, parent, master):
        wx.Panel.__init__(self, parent)
        self.master = master
        self.centerSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.centerSizer)

#        self.initContentList()

    def addListElem(self, box, font, arrow, i):
        elemField = wx.StaticText(self, label=self.master.content[i])
        elemID = i
        elemField.SetFont(font)
        arrowButton = wx.Button(self, id=elemID, label="  ", 
            size=(arrow.GetWidth()+10, arrow.GetHeight()+5))
        arrowButton.SetBitmap(arrow)
        self.Bind(wx.EVT_BUTTON, self.master.showPageView, arrowButton)
        tmpBox = wx.BoxSizer(wx.HORIZONTAL)
        tmpBox.Add(elemField, 0, wx.CENTER)
        tmpBox.AddSpacer(10)
        tmpBox.Add(arrowButton,0)
        box.Add(tmpBox,0,wx.CENTER)
        box.AddSpacer(20)


    def initContentList(self):
        """ This function creates content list and buttons, sets theirs positions and size and
            binds logic to them."""
        leftBox = wx.BoxSizer(wx.VERTICAL)
        rightBox = wx.BoxSizer(wx.VERTICAL)
        contentBox = wx.BoxSizer(wx.HORIZONTAL)

        listFont = self.master.tutorialFont
        listFont.SetPointSize(18)
        arrow = wx.Bitmap(relative_textures_path+"new\\arrow_green_head_small.png", wx.BITMAP_TYPE_ANY)

        contentSize = len(self.master.content)-1
        contentHalf = contentSize - (contentSize // 2)
        for i in range(contentHalf):
            self.addListElem(leftBox, listFont, arrow, i+1)

        for i in range(contentHalf, contentSize):
            self.addListElem(rightBox, listFont, arrow, i+1)

        contentBox.Add(leftBox,0)
        contentBox.AddSpacer(50)
        contentBox.Add(rightBox,0)
        self.centerSizer.Add(contentBox, 0, wx.CENTER) 
        self.centerSizer.AddSpacer(20)
        self.centerSizer.Layout()

    
class EntitiesTab(wx.Panel): #sparametryzowac po listach bytow - zadac konkretnych indeksow
    def __init__(self, parent, master):
        wx.Panel.__init__(self, parent)
        self.master = master
        self.centerSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.centerSizer)
        t = wx.StaticText(self, -1, "This is EntitiesTab", (20,20))
        self.centerSizer.Add(t, 0, wx.CENTER)


class TutorialView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        #ScrolledPanel.__init__(self, size=size, parent=parent, style=wx.SIMPLE_BORDER)
        wx.Panel.__init__(self, size=size, parent=parent)        
        self.name = name
        self.sender = sender

        self.size = size
        self.musicPath = musicPath

        #self.SetBackgroundColour((255, 255, 255))
        self.pageID = 0
        self.nrOfPages = 0
        self.tutorialInfo = "Welcome to our tutorial! If you'd like to find out what are all the functionalities of this cutting-edge game engine, you're in the right place :)"
        self.welcomeField = wx.StaticText(self, label=self.tutorialInfo)
        self.tutorialFont = wx.Font(20, wx.FONTFAMILY_DECORATIVE, 
            wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.welcomeField.SetFont(self.tutorialFont)
        self.setName = ""
        self.centerSizer = wx.BoxSizer(wx.VERTICAL)

        headerImg = wx.Image(relative_textures_path + "Tutorial.png", wx.BITMAP_TYPE_ANY)
        headerBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(headerImg))
        
        headerSizer = wx.BoxSizer(wx.HORIZONTAL)
        headerSizer.Add(headerBitmap)
        self.centerSizer.AddSpacer(10)
        self.centerSizer.Add(headerSizer, 0, wx.CENTER)
        self.centerSizer.AddSpacer(30)
        self.centerSizer.Add(self.welcomeField, 0, wx.CENTER)
        self.centerSizer.AddSpacer(10)
        self.content = None
        tabs = wx.Notebook(self)
        # Create the tab windows
        self.tab1 = MainTab(tabs,self)
        self.tab2 = EntitiesTab(tabs, self)
        self.tab3 = EntitiesTab(tabs,self)
        self.tab4 = EntitiesTab(tabs,self)
 
        # Add the windows to tabs and name them.
        tabs.AddPage(self.tab1, "MainTab")
        tabs.AddPage(self.tab2, "Resources Tab`")
        tabs.AddPage(self.tab3, "Dwellers Tab")
        tabs.AddPage(self.tab4, "Buildings Tab")
        self.centerSizer.Add(tabs, 0, wx.EXPAND)
        ln = wx.StaticLine(self, -1)
        self.centerSizer.Add(ln, 0, wx.EXPAND)

        menu_btn = wx.Button(self, label="Menu")
        self.centerSizer.AddSpacer(30)
        self.centerSizer.Add(menu_btn, 0, wx.CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

        #page view
        self.pageView = TutorialPageView(self, size, "Tutorial Page")
        self.pageView.Hide()
        self.pageView.centerSizer.ShowItems(False)
        self.graphsSpaces = GraphsSpaces(self)
        self.centerSizer.Add(self.graphsSpaces,0,wx.CENTER)
        self.centerSizer.SetDimension(0, 0, self.size[0], self.size[1])
        self.SetSizer(self.centerSizer)
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


    def requestPage(self, event):
        print "TutorialView: requestPage executed"
        print "PageID: " + str(event.GetId())
        realPageID = event.GetId()
        if realPageID > self.nrOfPages:
            realPageID = 1
        elif realPageID <= 0:
            realPageID = self.nrOfPages
        self.sender.entry_point.getTutorialPresenter().fetchTutorialPage(realPageID)

    def retToMenu(self, event):
        """ This function returns to Menu view """
        self.sender.entry_point.getTutorialPresenter().returnToMenu()

    def displayDependenciesGraph(self, jsonGraph):
        self.graphsSpaces.resetViewFromJSON(jsonGraph["Args"])
        self.centerSizer.Layout()

    def displayTutorialPage(self, jsonPage):
        pageContentString = jsonPage["Args"]["Page"]["page"]
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
            ratio = float(image.GetWidth()) / float(imgWidth)
            imgHeight = float(imgHeight) / ratio
            image.Rescale(imgWidth, int(imgHeight))
        if imgHeight < image.GetHeight():
            ratio = float(image.GetHeight()) / float(imgHeight)
            imgWidth = float(imgWidth) / float(ratio)
            image.Rescale(int(imgWidth), imgHeight)
            
        self.pageView.helperImg = image
        self.pageView.subPage = 0
        self.pageView.nrOfSubpages = len(pageContentString) - 3
        self.pageView.page = pageContentString["nr"]
        self.pageView.updateHyperlinksAndImg()

    def fetchTutorialIndex(self, index):
        # for x in jsonPage.keys():
        #     self.content.append(x)
        self.nrOfPages = len(index)-1
        if self.content is None:
            self.content = index
            print "Print index"
            if self.content is not None:
                for x in self.content:
                    print x
                    print type(x)
            self.tab1.initContentList()
            self.centerSizer.Layout()
        else:
            print "len(self.content):"
            print len(self.content)

    def fetchNodes(self, buildingsList, resourcesList, dwellersList):
        print "Print buildingsList"
        if buildingsList is not None:
            for x in buildingsList:
                print x
        print "Print resourcesList"
        if resourcesList is not None:
            for x in resourcesList:
                print x
        print "Print dwellersList"
        if dwellersList is not None:
            for x in dwellersList:
                print x
                print type(x)


    