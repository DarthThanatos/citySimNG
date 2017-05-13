import wx
import wx.grid as gridlib
import wx.combo
from pprint import PrettyPrinter
import json
import os
from RelativePaths import relative_music_path,relative_dependencies_path
from uuid import uuid4
import traceback
import re

class CreatorView(wx.Panel):
    def __init__(self, parent, size, name,  musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        wx.Panel.__init__(self,  size=size,  parent=parent)
        self.name = name
        self.parent = parent
        self.musicPath = musicPath
        self.sender = sender
        self.ackMsgs = {} #for confirming blocking send operations

        rootSizer = wx.BoxSizer(wx.VERTICAL)
        topSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        chosenSetSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.centerSizer = wx.BoxSizer(wx.HORIZONTAL) 

        choiceList = ["Resources", "Buildings", "Dwellers"]
        self.modes = wx.ComboBox(self, choices=choiceList, value="Buildings", style=wx.CB_READONLY)
        self.modes.Bind(wx.EVT_COMBOBOX, self.OnCombo)
        topSizer.Add(self.modes)

        self.dependenciesHeaders = {}
        # ^ list of type [[resourcesColumnsNames[0]...],[buildingsColumnsnames[0]...], [dwellersColumnsNames[0]...]]
        # needed at the time of creating dependencies via Create button

        resourcesColumnsNames = ["Resource\nName", "Predecessor", "Successor", "Description", "Texture path", "Start income", "Ico path"]
        self.dependenciesHeaders["Resources"] = resourcesColumnsNames

        resourcesInfo = "Resource name identifies this object; must be unique throughout this dependency set.\n" \
                        "Predecessor is the name of a resource that this object requires\n" \
                        "Successor is the name of a resource next in the hierarchy\n" \
                        "Description goes to the tutorial module\nStart income tells how much of a resource you get at start; set to zero if you do not want this resource to be produced at start" \
                        "Ico is the path to a file that contains image representing this object"


        dwellersColumnsNames = ["Dweller\nName", "Predecessor", "Successor", "Description", "Consumes",
                                "Consume Rate", "Ico path"]
        self.dependenciesHeaders["Dwellers"] = dwellersColumnsNames

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
                                 "Description", "Produces", "Consumes", "Consume Rate", "Produce Rate", "Cost\nin\nresources","Texture path",
                                 "Ico path", "Type"]
        self.dependenciesHeaders["Buildings"]  = buildingsColumnsNames

        buildingsInfo =\
            "Building name identifies this object; must be unique throughout this dependency set.\n" \
            "Dweller is a name existing in Dwellers list\n" \
            "Predecessor is the name of a dweller that this object requires\n" \
            "Successor is the name of a dweller next in the hierarchy\n" \
            "Description goes to the tutorial module\nCost in resources is a comma-separated list of pairs resource_name:units, that indicates how many units of resources player is due to have\n" \
            "Ico is the path to a file that contains image representing this object\n" +\
            ">>Produces<< is a semi-colon separated sequence of items existing at the resources list that" \
            " this building produces;\n Same rule applies for >>Consumes<< list\n>>Consume<< and >>Produce<<" \
            " rates ar metrics indicating pace at which building consumes a resource or produces it, respectively\n" \
            "Type can be either domastic or industrial\n texture path is a path to a file containing an image to be" \
            " loaded at play-time and displayed on the map\n"
        
        self.infos = {"Resources": resourcesInfo, "Buildings": buildingsInfo, "Dwellers": dwellersInfo}

        buildingsGrid = gridlib.Grid(self)
        buildingsGrid.CreateGrid(1, len(buildingsColumnsNames))
        for i, name in enumerate(buildingsColumnsNames):
            buildingsGrid.SetColLabelValue(i, name)
        buildingsGrid.Show()

        resourcesGrid = gridlib.Grid(self)
        resourcesGrid.CreateGrid(1, len(resourcesColumnsNames))
        for i, name in enumerate(resourcesColumnsNames):
            resourcesGrid.SetColLabelValue(i, name)
        resourcesGrid.Hide()

        dwellersGrid = gridlib.Grid(self)
        dwellersGrid.CreateGrid(1, len(dwellersColumnsNames))
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

        self.ctrlText = wx.TextCtrl(self, -1, "Default Set")
        chosenSetSizer.Add(self.ctrlText)

        load_btn = wx.Button(self, label="Load Created dependencies")
        self.Bind(wx.EVT_BUTTON, self.loadDependencies, load_btn)
        buttonsSizer.Add(load_btn, 0, wx.EXPAND, 5)

        menu_btn = wx.Button(self,  label="Menu")
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)
        buttonsSizer.Add(menu_btn, 0, wx.ALL | wx.EXPAND, 5)

        save_btn = wx.Button(self, label = "Save")
        self.Bind(wx.EVT_BUTTON, self.save, save_btn)
        buttonsSizer.Add(save_btn, 0, wx.EXPAND, 5)

        create_btn = wx.Button(self, label="Create")
        self.Bind(wx.EVT_BUTTON, self.createDependencies, create_btn)
        buttonsSizer.Add(create_btn, 0, wx.EXPAND, 5)

        add_row_btn = wx.Button(self, label="Add row")
        self.Bind(wx.EVT_BUTTON, self.addRow, add_row_btn)
        buttonsSizer.Add(add_row_btn, 0, wx.EXPAND, 5)

        delete_row_btn = wx.Button(self, label= "Delete Row")
        self.Bind(wx.EVT_BUTTON, self.deleteRow, delete_row_btn)
        buttonsSizer.Add(delete_row_btn, 0, wx.EXPAND, 5)

        self.errorMsgField = wx.StaticText(self, label=self.infos[self.currentGrid])
        self.defaultErrorFieldMsg = "Be careful when deleting rows;" +\
                                    "\nclick on one of the cells in a row you want to delete;"+\
                                    "\nthen press delete button;"+\
                                    "\nBefore creating dependencies, all cells must be filled;"+\
                                    "\nOtherwise we cannot procced"
        self.errorMsgField.SetLabelText(self.defaultErrorFieldMsg)
        buttonsSizer.Add(self.errorMsgField, 0, wx.EXPAND, 5)

        rootSizer.Add(topSizer, 0, wx.CENTER)
        rootSizer.Add(self.centerSizer, 0, wx.EXPAND, 5)
        rootSizer.Add(buttonsSizer, 0, wx.CENTER)
        rootSizer.Add(chosenSetSizer, 0, wx.CENTER)
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
            self.resetView() # true means that one empty row is always present in each grid after reset
            try:        
                import pygame
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(
                    #os.path.dirname(os.path.abspath(__file__)) + "\\" +
                    self.musicPath)
                pygame.mixer.music.play()
            except Exception:
                print "Problem with music"
        else:
            try:
                pygame.quit()
            except Exception:
                print "creator: problem with pygame quit"

    def retToMenu(self, event):
        #self.parent.setView("Menu")
        msg = {}
        msg["To"] = "CreatorNode"
        msg["Operation"] = "MoveTo"
        msg["Args"] = {}
        msg["Args"]["TargetView"] = "MainMenu"
        msg["Args"]["TargetControlNode"] = "MainMenuNode"
        self.sender.send(json.dumps(msg))

    def getGridsContent(self):
        gridNamesList = ["Resources", "Buildings", "Dwellers"]
        dependencies = {} #initialize empty lists for each grid; lists will be of dict type

        for gridName in gridNamesList:
            grid = self.tables[gridName]
            gridRowsNum, gridColsNum = grid.GetNumberRows(), grid.GetNumberCols()
            dependencies[gridName] = [
                {
                    self.dependenciesHeaders[gridName][j] : grid.GetCellValue(i,j) for j in range(gridColsNum)
                } for i in range(gridRowsNum)
            ]
        # ^ here we have a dictionary representing an entire dependency set;
        # each key holds textual representation of each grid's content;
        # that representation is a list of rows in a grid;
        # each row content is described via a dictonary mapping the column name to its value in a particular row
        return dependencies

    def createDependencies(self, event):
        gridNamesList = ["Resources", "Buildings", "Dwellers"]
        dependencies = self.getGridsContent()

        pp = PrettyPrinter()
        pp.pprint(dependencies)

        #check if each cell has content (is not empty)
        for gridName in gridNamesList:
            tableTextRepresentation = dependencies[gridName]
            for row_index, row in enumerate(tableTextRepresentation):
                for columnName, value in row.items():
                    if value == "":
                        errorMsg =  "Dependencies not created: empty cell\nat: " + gridName + "\nrow: " + str(row_index) +  "\ncolumn name: " + columnName
                        print errorMsg
                        self.errorMsgField.SetLabelText(errorMsg)
                        return
        setName = self.ctrlText.GetValue()
        if re.sub(r'\s', "", setName) == "":
            errorMsg = "Please, fill dependencies set name field"
            print errorMsg
            self.errorMsgField.SetLabelText(errorMsg)
            return

        msg = "Dependencies sent to further processing to creator controller"
        print msg
        self.errorMsgField.SetLabelText(msg)
        uuid = uuid4().__str__()
        self.ackMsgs[uuid] = False

        msg = {}
        msg["To"] = "CreatorNode"
        msg["Operation"] = "Parse"
        msg["Args"] = {}
        msg["Args"]["Dependencies"] = dependencies
        msg["Args"]["DependenciesSetName"] = setName
        msg["Args"]["UUID"] = uuid
        stream = json.dumps(msg)
        print stream
        self.sender.send(stream)
        while not self.ackMsgs[uuid]: pass

        msg = "Dependencies created successfully, please go to the Loader menu now to check what was created"
        print msg
        self.errorMsgField.SetLabelText(msg)



    def save(self, event):
        dependencies = self.getGridsContent()
        dlg = wx.FileDialog(
            self,
            defaultDir = relative_dependencies_path,
            message = "Choose a file to save",
            wildcard = "*.dep",
            style = wx.FD_SAVE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            with open(path, "wb+") as f:
                f.write(json.dumps(dependencies).replace(",",",\n"))

    def addRow(self, event):
        self.tables[self.currentGrid].AppendRows()
        self.centerSizer.Layout()
        pos = self.tables[self.currentGrid].GetGridCursorRow()
        msg = "row added to " + self.currentGrid + " current pos:" + str(pos)
        print msg
        self.errorMsgField.SetLabelText(msg)

    def deleteRow(self, event):
        pos = self.tables[self.currentGrid].GetGridCursorRow()
        self.tables[self.currentGrid].DeleteRows(pos)
        msg = "Row removed from " + self.currentGrid +  " at: " + str(pos)
        print msg
        self.errorMsgField.SetLabelText(msg)


    def readMsg(self, msg):
        print "Creator view got msg", msg
        jsonMsg = json.loads(msg)
        operation = jsonMsg["Operation"]
        if operation == "ParseConfirm":
            self.ackMsgs[jsonMsg["Args"]["UUID"]] = True #unblock blocked thread


    def dependencyLoadFail(self):
        errorMsg = "Not a valid file format, need a .dep file"
        print errorMsg
        self.errorMsgField.SetLabelText(errorMsg)

    def resetGrids(self, addStartRow = False):
        gridNamesList = ["Resources", "Buildings", "Dwellers"]
        for gridName in gridNamesList:
            grid = self.tables[gridName]
            rowsNum = grid.GetNumberRows()
            for i in range(rowsNum):
                grid.DeleteRows()
            if addStartRow: grid.AppendRows()
        self.centerSizer.Layout()

    def resetView(self):
        self.resetGrids(True)
        self.errorMsgField.SetLabelText(self.defaultErrorFieldMsg)
        self.tables[self.currentGrid].Hide()
        self.tables["Buildings"].Show()
        self.currentGrid = "Buildings"
        self.ctrlMsgField.SetLabel(self.infos[self.currentGrid])
        self.modes.SetStringSelection("Buildings")
        self.centerSizer.Layout()
        self.ctrlText.SetLabelText("Default Set")

    def fillGridsWithContent(self, content_dict):
        self.resetGrids()
        try:
            gridNamesList = ["Resources", "Buildings", "Dwellers"]
            for gridName in gridNamesList:
                tableTextRepresentation = content_dict[gridName]
                for row_index, row in enumerate(tableTextRepresentation):
                    self.tables[gridName].AppendRows(1)
                    for columnName, value in row.items():
                        j = self.dependenciesHeaders[gridName].index(columnName)
                        self.tables[gridName].SetCellValue(row_index,j, value)
        except Exception:
            return False
        self.centerSizer.Layout()
        return True

    def loadDependencies(self, event):
        dlg = wx.FileDialog(
            self,
            defaultDir = relative_dependencies_path,
            message = "Choose a file",
            wildcard="*.dep",
            style = wx.FD_OPEN | wx.FD_MULTIPLE
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "You chose the following file:", path
            if path.endswith(".dep"):
                with open (path, "r+") as dependency_file:
                    dependency_content = dependency_file.read().replace("u'","'").replace("'","\"")
                    print dependency_content
                    try:
                        dependency_dict = json.loads(dependency_content)
                        grids_copy = self.getGridsContent() #if sth goes wrong, we can restore previous state
                        if not self.fillGridsWithContent(dependency_dict):
                            errorMsg = "Error while loading file"
                            print errorMsg
                            self.errorMsgField.SetLabelText(errorMsg)
                            self.fillGridsWithContent(grids_copy) #here we restore previous state of grids
                        else:
                            msg = "Dependencies loaded successfully!"
                            print msg
                            self.errorMsgField.SetLabelText(msg)
                    except Exception:
                        self.dependencyLoadFail()
                        traceback.print_exc()
            else:
                self.dependencyLoadFail()