import wx
import wx.grid as gridlib
import wx.combo


class CreatorView(wx.Panel):
    def __init__(self, parent, size, name,  musicPath="TwoMandolins.mp3"):
        wx.Panel.__init__(self,  size=size,  parent=parent)
        self.name = name
        self.parent = parent
        self.musicPath = musicPath

        rootSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.centerSizer = wx.BoxSizer(wx.HORIZONTAL) 

        choiceList = ["Resources", "Buildings", "Dwellers"]
        modes = wx.ComboBox(self, choices=choiceList, value="Buildings", style=wx.CB_READONLY)
        modes.Bind(wx.EVT_COMBOBOX, self.OnCombo) 
        topSizer.Add(modes)

        resourcesColumnsNames = ["Resource\nName", "Predecessor", "Successor", "Description", "Ico path"]
        resourcesInfo = "Resource name identifies this object; must be unique throughout this dependency set.\n" \
                        "Predecessor is the name of a resource that this object requires\n" \
                        "Successor is the name of a resource next in the hierarchy\n" \
                        "Description goes to the tutorial module\n" \
                        "Ico is the path to a file that contains image representing this object"
        dwellersColumnsNames = ["Dweller\nName", "Predecessor", "Successor", "Description", "Consumes",
                                "Consume Rate", "Ico path"]
        dwellersInfo =\
            "Dweller name identifies this object; must be unique throughout this dependency set.\n" \
            "Predecessor is the name of a dweller that this object requires to exist\n" \
            "Successor is the name of a dweller next in the hierarchy\n" \
            "Description goes to the tutorial module\n" \
            "Ico is the path to a file that contains image representing this object\n" +\
            ">>Consumes<< is a list of resource identifiers that this dweller consumes, whose items are separated" \
            " via semi-colons;\n >>ConsumeRate<< is a rate at which resources listed in >>Consumes<< are removed" \
            " from the stock pile; those are semi-colon separated float values, each representing a resource at the" \
            " same position in >>Consumes<< list"
        buildingsColumnsNames = ["Building\nName", "Dweller\nName", "Dwellers\namount", "Predecessor", "Successor",
                                 "Description", "Produces", "Consumes", "Consume Rate", "Produce Rate", "Texture path",
                                 "Ico path", "Type"]
        buildingsInfo =\
            "Building name identifies this object; must be unique throughout this dependency set.\n" \
            "Dweller is a name existing in Dwellers list\n" \
            "Predecessor is the name of a dweller that this object requires\n" \
            "Successor is the name of a dweller next in the hierarchy\n" \
            "Description goes to the tutorial module\n" \
            "Ico is the path to a file that contains image representing this object\n" +\
            ">>Produces<< is a semi-colon separated sequence of items existing at the resources list that" \
            " this building produces;\n Same rule applies for >>Consumes<< list\n>>Consume<< and >>Produce<<" \
            " rates ar metrics indicating pace at which building consumes a resource or produces it, respectively\n" \
            "Type can be either domastic or industrial\n texture path is a path to a file containing an image to be" \
            " loaded at play-time and displayed on the map\n"
        
        self.infos = {"Resources": resourcesInfo, "Buildings": buildingsInfo, "Dwellers": dwellersInfo}

        buildingsGrid = gridlib.Grid(self)
        buildingsGrid.CreateGrid(25, len(buildingsColumnsNames))
        for i, name in enumerate(buildingsColumnsNames):
            buildingsGrid.SetColLabelValue(i, name)
        buildingsGrid.Show()

        resourcesGrid = gridlib.Grid(self)
        resourcesGrid.CreateGrid(25, len(resourcesColumnsNames))
        for i, name in enumerate(resourcesColumnsNames):
            resourcesGrid.SetColLabelValue(i, name)
        resourcesGrid.Hide()

        dwellersGrid = gridlib.Grid(self)
        dwellersGrid.CreateGrid(25, len(dwellersColumnsNames))
        for i, name in enumerate(dwellersColumnsNames):
            dwellersGrid.SetColLabelValue(i, name)
        dwellersGrid.Hide()

        self.tables = {"Resources": resourcesGrid, "Dwellers": dwellersGrid, "Buildings": buildingsGrid}

        self.centerSizer.Add(buildingsGrid)
        self.centerSizer.Add(resourcesGrid)
        self.centerSizer.Add(dwellersGrid)
        self.currentGrid = "Buildings"
        self.ctrlMsgField = wx.StaticText(self, label=self.infos[self.currentGrid])
        self.centerSizer.Add(self.ctrlMsgField, 0, wx.EXPAND, 5)

        menu_btn = wx.Button(self,  label="Menu")
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)
        buttonsSizer.Add(menu_btn, 0, wx.ALL | wx.EXPAND, 5)

        create_btn = wx.Button(self, label="Create")
        self.Bind(wx.EVT_BUTTON, self.createDependencies, create_btn)
        buttonsSizer.Add(create_btn, 0, wx.EXPAND, 5)
        
        rootSizer.Add(topSizer, 0, wx.CENTER)
        rootSizer.Add(self.centerSizer, 0, wx.EXPAND, 5)
        rootSizer.Add(buttonsSizer, 0, wx.CENTER)

        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, size[0], size[1])
        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def OnCombo(self, event):
        print "combobox:", event.GetString()
        self.tables[self.currentGrid].Hide()
        self.tables[event.GetString()].Show()
        self.currentGrid = event.GetString()
        self.ctrlMsgField.SetLabel(self.infos[self.currentGrid])
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
