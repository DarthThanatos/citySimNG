import json
#import traceback
import wx
#from py4j.java_collections import JavaList, JavaArray

from CreatorView.GraphsSpaces import GraphsSpaces
from TutorialPageView import TutorialPageView
from utils.RelativePaths import relative_music_path, relative_textures_path, relative_fonts_path


class MainTab(wx.Panel):
    def __init__(self, parent, master, tabID):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.master = master
        self.centerSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.centerSizer)
        self.listCtrls =[]
        self.indexList = []
        self.tabID = tabID
        self.isInitialized = False

        self.initContentList()

    def addListElem(self, box, font, arrow, i):
        elemField = wx.StaticText(self, label=" ") #elemField = wx.StaticText(self, label=self.master.content[i])
        elemID = i
        elemField.SetFont(font)
        arrowButton = wx.Button(self, id=elemID, label="  ", 
            size=(arrow.GetWidth()+10, arrow.GetHeight()+5))
        arrowButton.SetBitmap(arrow)
        tmpBox = wx.BoxSizer(wx.HORIZONTAL)
        tmpBox.Add(elemField, 0, wx.CENTER)
        tmpBox.AddSpacer(10)
        tmpBox.Add(arrowButton,0)

        listItem = {'elemField': elemField, 'arrowButton': arrowButton, 'box': tmpBox}
        self.listCtrls.append(listItem)
        box.Add(tmpBox,0,wx.CENTER)
        box.AddSpacer(20)


    def initContentList(self):
        """ This function creates content list and buttons, sets theirs positions and size and
            binds logic to them."""
        self.leftBox = wx.BoxSizer(wx.VERTICAL)
        self.rightBox = wx.BoxSizer(wx.VERTICAL)
        self.contentBox = wx.BoxSizer(wx.HORIZONTAL)

        listFont = self.master.tutorialFont
        listFont.SetPointSize(18)
        arrow = wx.Bitmap(relative_textures_path+"new\\arrow_green_head_small.png", wx.BITMAP_TYPE_ANY)

        #contentSize = len(self.master.content)-1
        contentSize = self.master.maxNrOfItemsOnList
        contentHalf = contentSize - (contentSize // 2)
        for i in range(contentHalf):
            self.addListElem(self.leftBox, listFont, arrow, i)

        for i in range(contentHalf, contentSize):
            self.addListElem(self.rightBox, listFont, arrow, i)

        self.contentBox.Add(self.leftBox,0)
        self.contentBox.AddSpacer(50)
        self.contentBox.Add(self.rightBox,0)
        self.centerSizer.Add(self.contentBox, 0, wx.CENTER) 
        self.centerSizer.AddSpacer(20)
        self.centerSizer.Layout()

    def fillListItem(self, i):
        print "Filling listItem"
        listItem = self.listCtrls[i]
        if self.indexList[i] is not None:
            print "Lable type: " + str(type(self.indexList[i]))
            print "Lable : " + str(self.indexList[i]) + "\n"
            listItem['elemField'].SetLabel(self.indexList[i])
            listItem['arrowButton'].SetId(i + 10*self.tabID)
            self.Bind(wx.EVT_BUTTON, self.master.showPageView, listItem['arrowButton'])
            listItem['box'].Layout()
        else:
            #listItem['box'].ShowItems(False)
            #listItem['box'].Layout()
            listItem['arrowButton'].Hide()
            listItem['box'].Layout()

    def fillContentList(self, indexList):
        print "\nFilling content list"
        self.indexList = indexList
        contentSize = len(indexList)
        contentHalf = contentSize - (contentSize // 2)
        for i in range(contentHalf):
            self.fillListItem(i)

        for i in range(contentHalf, contentSize):
            self.fillListItem(i)
        self.leftBox.Layout()
        self.rightBox.Layout()
        self.contentBox.Layout()
        self.centerSizer.Layout()
        self.Layout()

    
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
        self.maxNrOfItemsOnList = 8

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
        #self.content = None
        tabs = wx.Notebook(self)
        # Create the tab windows
        self.tab1 = MainTab(tabs,self, 1)
        self.tab2 = MainTab(tabs, self, 2)
        self.tab3 = MainTab(tabs,self, 3)
        self.tab4 = MainTab(tabs,self, 4)
 
        # Add the windows to tabs and name them.
        tabs.AddPage(self.tab1, "MainTab")
        tabs.AddPage(self.tab2, "Buildings Tab`")
        tabs.AddPage(self.tab3, "Resources Tab")
        tabs.AddPage(self.tab4, "Dwellers Tab")
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
        print "\nshowPageView"
        self.requestPage(event)

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
        tabID = event.GetId() // 10
        if tabID is 1:
            print "Tutorial index request"
            realPageID = event.GetId() % 10
            if realPageID > self.nrOfPages-1:
                realPageID = 0
            elif realPageID < 0:
                realPageID = self.nrOfPages-1 
            print("realPageID: " +str(realPageID) + "; self.nrOfPages: " + str(self.nrOfPages))

            self.sender.entry_point.getTutorialPresenter().fetchTutorialPage(realPageID)
        elif tabID is 2:
            print "Buildings index request"
        elif tabID is 3:
            print "Resources index request"
        elif tabID is 4:
            print "Dwellers index request"
        

    def retToMenu(self, event):
        """ This function returns to Menu view """
        self.sender.entry_point.getTutorialPresenter().returnToMenu()

    def displayDependenciesGraph(self, jsonGraph):
        self.graphsSpaces.resetViewFromJSON(jsonGraph["Args"])
        self.centerSizer.Layout()

    def displayTutorialPage(self, jsonPage):
        pageContentString = jsonPage["Args"]
        self.pageView.tutorialContent = pageContentString
        firstSubPage = pageContentString["sub0"]
        firstSubPageContent = ""
        for x in firstSubPage:
            firstSubPageContent += x
            firstSubPageContent += "\n"
        self.pageView.contentField.SetValue(firstSubPageContent)

        hyperlinks = pageContentString["link"]
        #tu przejrzec hyperlinks, stworzyc nowy slownik na podstawie danych z tab1\
        hyperlinksWithLabels = []
        for x in hyperlinks:
            if x >=0 and x <= self.nrOfPages-1:
                link = {'label': self.tab1.indexList[x], 'id': x}
                print ("Link: " + str(link))
                hyperlinksWithLabels.append(link)
        self.pageView.hyperlinks = hyperlinksWithLabels
        print "hyperlinksWithLabels:"
        print hyperlinksWithLabels

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
        self.pageView.page = pageContentString["nr"] + 10
        self.pageView.tabID = 1
        self.pageView.updateHyperlinksAndImg()

        self.centerSizer.ShowItems(False)
        self.pageView.Show()
        self.pageView.centerSizer.ShowItems(True)


    def useFetchedIndex(self, index, tab):
        if index is not None:
            for x in index:
                print x
            tab.fillContentList(index)
            tab.isInitialized = True
        self.centerSizer.Layout()

    def fetchTutorialIndex(self, index):
        self.nrOfPages = len(index)-1
        print "self.nrOfPages = " + str(self.nrOfPages)
        if self.tab1.isInitialized is False:
            print "Print index"
            self.useFetchedIndex(index, self.tab1)
            if self.tab1.isInitialized is False:
                print "Sth went wrong with tutorial indexList!!!!"
        else:
            print "len(self.tab1.indexList):"
            print len(self.tab1.indexList)

    def fetchNodes(self, buildingsList, resourcesList, dwellersList):
        print "Print buildingsList"
        if self.tab2.isInitialized is False:
            self.useFetchedIndex(buildingsList, self.tab2)
            if self.tab2.isInitialized is False:
                print "Sth went wrong with buildings!!!"
        print "Print resourcesList"
        if self.tab3.isInitialized is False:
            self.useFetchedIndex(resourcesList, self.tab3)
            if self.tab3.isInitialized is False:
                print "Sth went wrong with resources!!!"
        print "Print dwellersList"
        if self.tab4.isInitialized is False:
            self.useFetchedIndex(dwellersList, self.tab4)
            if self.tab4.isInitialized is False:
                print "Sth went wrong with Dwellers!!!"


    