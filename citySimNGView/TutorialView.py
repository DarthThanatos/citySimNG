import json
#import traceback
import wx

from wx.lib.scrolledpanel import ScrolledPanel
from CreatorView.GraphsSpaces import GraphsSpaces
from TutorialPageView import TutorialPageView
from MainTab import MainTab
from utils.RelativePaths import relative_music_path, relative_textures_path, relative_fonts_path

class TutorialView(ScrolledPanel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        ScrolledPanel.__init__(self, size=size, parent=parent, style=wx.SIMPLE_BORDER)
        #wx.Panel.__init__(self, size=size, parent=parent)        
        self.name = name
        self.sender = sender

        self.size = size
        self.musicPath = musicPath

        self.pageID = 0
        self.nrOfPages = 0
        self.maxNrOfItemsOnList = 21

        self.SetupScrolling()
        self.initTutorialHeader()
        self.initTutorialTabs()
        self.initTutorialFooter()
        self.initTutorialPageView()
        self.centerSizer.Add(self.graphsSpaces,0,wx.CENTER)
        self.SetSizer(self.centerSizer)
        self.centerSizer.SetDimension(0, 0, self.size[0], self.size[1])
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.centerSizer.Layout()


    def initTutorialHeader(self):
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

    def initTutorialTabs(self):
        tabs = wx.Notebook(parent=self, name="tutorialNotebook")
        # Create the tab windows
        self.tab1 = MainTab(tabs,self, 1)
        self.tab2 = MainTab(tabs,self, 2)
        self.tab3 = MainTab(tabs,self, 3)
        self.tab4 = MainTab(tabs,self, 4)
 
        # Add the windows to tabs and name them.
        tabs.AddPage(self.tab1, "MainTab")
        tabs.AddPage(self.tab2, "Buildings Tab`")
        tabs.AddPage(self.tab3, "Resources Tab")
        tabs.AddPage(self.tab4, "Dwellers Tab")
        self.centerSizer.Add(tabs, 0, wx.EXPAND)

    def initTutorialFooter(self):
        ln = wx.StaticLine(self, -1)
        self.centerSizer.Add(ln, 0, wx.EXPAND)

        menu_btn = wx.Button(self, label="Menu")
        self.centerSizer.AddSpacer(30)
        self.centerSizer.Add(menu_btn, 0, wx.CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)

        self.graphsSpaces = GraphsSpaces(self)

    def initTutorialPageView(self):
        self.pageView = TutorialPageView(self, self.size, "Tutorial Page")
        self.pageView.Hide()
        self.pageView.centerSizer.ShowItems(False)

    def showPageView(self, event):
        print "\nshowPageView"
        print "TutorialView: requestPage executed"
        print "PageID: " + str(event.GetId())
        self.sender.entry_point.getTutorialPresenter().fetchPage(event.GetId())

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

        self.pageView.hyperlinks = self.initHyperlinks(hyperlinks)
        # print "hyperlinksWithLabels:"
        # print hyperlinksWithLabels

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
        self.pageView.tabID = pageContentString["nr"]//100
        self.pageView.updateHyperlinksAndImg()

        self.centerSizer.ShowItems(False)
        self.pageView.Show()
        self.pageView.centerSizer.ShowItems(True)

    def initHyperlinks(self, hyperlinks):
        hyperlinksWithLabels = []
        for x in hyperlinks:
            hyperlinkTab = x//100
            hyperlinkID = x%100
            if hyperlinkTab == 1:
                if hyperlinkID >=0 and hyperlinkID <= len(self.tab1.indexList)-1:
                    link = {'label': self.tab1.indexList[hyperlinkID], 'id': x}
                    #print ("Link: " + str(link))
                    hyperlinksWithLabels.append(link)
            elif hyperlinkTab == 2:
                if hyperlinkID >=0 and hyperlinkID <= len(self.tab2.indexList)-1:
                    link = {'label': self.tab2.indexList[hyperlinkID], 'id': x}
                    #print ("Link: " + str(link))
                    hyperlinksWithLabels.append(link)
            elif hyperlinkTab == 3:
                if hyperlinkID >=0 and hyperlinkID <= len(self.tab3.indexList)-1:
                    link = {'label': self.tab3.indexList[hyperlinkID], 'id': x}
                    #print ("Link: " + str(link))
                    hyperlinksWithLabels.append(link)
            elif hyperlinkTab == 4:
                if hyperlinkID >=0 and hyperlinkID <= len(self.tab4.indexList)-1:
                    link = {'label': self.tab4.indexList[hyperlinkID], 'id':x }
                    #print ("Link: " + str(link))
                    hyperlinksWithLabels.append(link)
        return hyperlinksWithLabels


    def useFetchedIndex(self, index, tab):
        #if index is not None:
            #for x in index:
            #    print x
        tab.fillContentList(index)
        tab.isInitialized = True
        self.centerSizer.Layout()

    def fetchTutorialIndex(self, index):
        self.nrOfPages = len(index)-1
        print "self.nrOfPages = " + str(self.nrOfPages)
        #if self.tab1.isInitialized is False:
           # print "Print index"
        self.useFetchedIndex(index[:-1], self.tab1)
        if self.tab1.isInitialized is False:
           print "Sth went wrong with tutorial indexList!!!!"
        # else:
        #     print "len(self.tab1.indexList):"
        #     print len(self.tab1.indexList)

    def fetchNodes(self, buildingsList, resourcesList, dwellersList):
        #print "Print buildingsList"
        #if self.tab2.isInitialized is False:
        self.useFetchedIndex(buildingsList, self.tab2)
        if self.tab2.isInitialized is False:
            print "Sth went wrong with buildings!!!"
       # print "Print resourcesList"
       # if self.tab3.isInitialized is False:
        self.useFetchedIndex(resourcesList, self.tab3)
        if self.tab3.isInitialized is False:
            print "Sth went wrong with resources!!!"
       # print "Print dwellersList"
       # if self.tab4.isInitialized is False:
        self.useFetchedIndex(dwellersList, self.tab4)
        if self.tab4.isInitialized is False:
            print "Sth went wrong with Dwellers!!!"


    