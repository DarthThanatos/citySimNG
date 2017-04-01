import wx
import wx.grid as gridlib
import wx.combo

class CreatorView(wx.Panel):
    def __init__(self, parent, size, name,  musicPath = "TwoMandolins.mp3"):
        wx.Panel.__init__(self,  size = size,  parent=parent)
        self.name = name
        self.parent = parent
        self.musicPath = musicPath

        rootSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.centerSizer = wx.BoxSizer(wx.HORIZONTAL) 

        choiceList = ["Resources", "Buildings", "Dwellers"]
        modes = wx.ComboBox(self,choices = choiceList, value = "--select--", style = wx.CB_READONLY)
        modes.Bind(wx.EVT_COMBOBOX, self.OnCombo) 
        topSizer.Add(modes)

        resourcesColumnsNames = ["Resource\nName", "Buildings\nassigned", "Dwellers\nassigned", "Predecessor", "Successor", "Description", "Ico path", "Type"]
        dwellersColumnsNames = ["Dweller\nName", "Dwellers\n amount", "Resources", "Predecessor", "Successor", "Description", "Consumes", "Ico path"]
        buildingsColumnsNames = ["Building\nName", "Dweller\nName", "Dwellers\n amount", "Resources", "Predecessor", "Successor", "Description", "Produces", "Consumes", "Texture path", "Ico path", "Type"]
        
        buildingsGrid = gridlib.Grid(self)
        buildingsGrid.CreateGrid(25, len(buildingsColumnsNames))
        for i,name in enumerate(buildingsColumnsNames):
            buildingsGrid.SetColLabelValue(i, name)
        buildingsGrid.Show()

        resourcesGrid = gridlib.Grid(self)
        resourcesGrid.CreateGrid(25, len(resourcesColumnsNames))
        for i,name in enumerate(resourcesColumnsNames):
            resourcesGrid.SetColLabelValue(i, name)
        resourcesGrid.Hide()

        dwellersGrid = gridlib.Grid(self)
        dwellersGrid.CreateGrid(25, len(dwellersColumnsNames))
        for i,name in enumerate(dwellersColumnsNames):
            dwellersGrid.SetColLabelValue(i, name)
        dwellersGrid.Hide()

        self.tables = {"Resources":resourcesGrid, "Dwellers":dwellersGrid, "Buildings":buildingsGrid}

        ctrlMsgField = wx.StaticText(self, label = "This is the place for control messages")
        self.centerSizer.Add(buildingsGrid)
        self.centerSizer.Add(resourcesGrid)
        self.centerSizer.Add(dwellersGrid)
        self.currentGrid = "Buildings"
        self.centerSizer.Add(ctrlMsgField, 0 , wx.EXPAND, 5)


        menu_btn = wx.Button(self,  label="Menu")
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)
        buttonsSizer.Add(menu_btn, 0 , wx.ALL | wx.EXPAND, 5)

        create_btn = wx.Button(self, label = "Create")
        self.Bind(wx.EVT_BUTTON, self.createDependencies, create_btn)
        buttonsSizer.Add(create_btn, 0, wx.EXPAND, 5)
        
        rootSizer.Add(topSizer, 0, wx.CENTER)
        rootSizer.Add(self.centerSizer, 0, wx.EXPAND, 5)
        rootSizer.Add(buttonsSizer,0, wx.CENTER)

        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0,0,size[0],size[1])
        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def OnCombo(self, event):
        print "combobox:", event.GetString()
        self.tables[self.currentGrid].Hide()
        self.tables[event.GetString()].Show()
        self.currentGrid = event.GetString()
        self.centerSizer.Layout()

    def onShow(self, event):
        global pygame
        if event.GetShow(): 
            try:        
                import pygame
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(self.musicPath)
                pygame.mixer.music.play()
            except Exception:
                print "Problem with music"
        else:
            try:
                pygame.quit()
            except Exception:
                print "menu: problem with pygame quit"

    def retToMenu(self, event):
        self.parent.setView("Menu")

    def createDependencies(self, event):
        print "Dependencies created"
