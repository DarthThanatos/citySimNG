import wx
from wx.lib.scrolledpanel import ScrolledPanel
from DependenciesPanel import DependenciesPanel
from LogMessages import WELCOME_MSG
import json
from RelativePaths import relative_dependencies_path,relative_textures_path
import traceback
import re
from uuid import uuid4
from GraphsSpaces import GraphsSpaces
from utils.SocketMsgReader.CreatorMsgReader import CreatorMsgReader
from viewmodel.CreatorData import CreatorData
from Consts import CREATOR_MAIN_PANEL_ROOT_SPACER_SIZE


class CreatorMainEntry(ScrolledPanel):

    def initChosenSetNameSizer(self):
        self.chosenSetSizer = wx.BoxSizer(wx.HORIZONTAL)
        dependenciesSetNameLabel = wx.StaticText(self,-1, "Name of this dependencies set")
        self.dependenciesSetNameInput = wx.TextCtrl(self, -1, "Default Set")
        self.chosenSetSizer.Add(dependenciesSetNameLabel)
        self.chosenSetSizer.AddSpacer(5)
        self.chosenSetSizer.Add(self.dependenciesSetNameInput)

    def initChildrenDependenciesPanelsSizer(self):
        self.dependenciesPartsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        resourcesNames = self.current_dependencies["Resources"].keys()
        dwellersNames = self.current_dependencies["Dwellers"].keys()
        buildingsNames = self.current_dependencies["Buildings"].keys()
        self.resourcesDependenciesPanel = \
            DependenciesPanel(self, self.dependenciesPartsVerticalSizer, "Resources", resourcesNames, self.frame, self.current_dependencies)
        self.dwellersDependenciesPanel = \
            DependenciesPanel(self, self.dependenciesPartsVerticalSizer, "Dwellers", dwellersNames, self.frame, self.current_dependencies)
        self.buildingsDependenciesPanel = \
            DependenciesPanel(self, self.dependenciesPartsVerticalSizer, "Buildings", buildingsNames, self.frame, self.current_dependencies)
        self.children = [self.resourcesDependenciesPanel, self.dwellersDependenciesPanel, self.buildingsDependenciesPanel]

    def initDependenciesPanelsPartHorizontalSizer(self):
        self.dependenciesPartsHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.dependenciesPartsHorizontalSizer.Add(self.dependenciesPartsVerticalSizer)
        self.dependenciesPartsHorizontalSizer.AddSpacer(10)
        self.dependenciesPartsHorizontalSizer.Add(self.logAreaVerticalSizer)

    def initLogAreaSizer(self):
        self.logAreaVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        logLabel = wx.StaticText(self, label="Log area, shows important information")
        self.logAreaVerticalSizer.Add(logLabel)
        self.logArea = wx.TextCtrl(parent = self, id=-1, size=(400, 90 * 3 + 10 * 3), style=wx.TE_MULTILINE | wx.TE_READONLY)
        # ^ height of a logArea textctrl comes from the equation:
        #  h = dependencyPanel_height * dependenciesPanelsAmount + part_desc_label_height * dependenciesPanelsAmount
        self.logAreaVerticalSizer.Add(self.logArea)

    def initTextureOneHorizontalSizer(self):
        self.image_one_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        img_one_info_label = wx.StaticText(self, -1, "Your background texture number one: ")
        img_one_selector_btn = wx.Button(self, -1, label = "Choose another texture", size = (-1, 32))
        self.Bind(wx.EVT_BUTTON, self.onImageOneSelected ,img_one_selector_btn)
        image = wx.Image(name = relative_textures_path + "Grass.png")#"..\\..\\resources\\Textures\\Grass.png"
        self.imageBitmapOne = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))
        self.texture_one_name = "Grass.png"
        self.image_one_horizontal_sizer.Add(img_one_info_label)
        self.image_one_horizontal_sizer.AddSpacer(10)
        self.image_one_horizontal_sizer.Add(self.imageBitmapOne)
        self.image_one_horizontal_sizer.AddSpacer(10)
        self.image_one_horizontal_sizer.Add(img_one_selector_btn)

    def initTextureTwoHorizontalSizer(self):
        self.image_two_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        img_two_info_label = wx.StaticText(self, -1, "Your background texture number two: ")
        img_two_selector_btn = wx.Button(self, -1, label = "Choose another texture", size = (-1, 32))
        self.Bind(wx.EVT_BUTTON, self.onImageTwoSelected ,img_two_selector_btn)
        image = wx.Image(name = relative_textures_path + "Grass2.jpg") #"..\\..\\resources\\Textures\\Grass2.jpg"
        self.texture_two_name = "Grass2.jpg"
        self.imageBitmapTwo = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))
        self.image_two_horizontal_sizer.Add(img_two_info_label)
        self.image_two_horizontal_sizer.AddSpacer(10)
        self.image_two_horizontal_sizer.Add(self.imageBitmapTwo)
        self.image_two_horizontal_sizer.AddSpacer(10)
        self.image_two_horizontal_sizer.Add(img_two_selector_btn)

    def createButtons(self):
        self.menu_btn = wx.Button(self, label="Menu")
        self.load_btn = wx.Button(self, label="Load dependencies From File")
        self.save_btn = wx.Button(self, label="Save these dependencies to File")
        self.create_btn = wx.Button(self, label="Create")
        self.clean_btn = wx.Button(self, label = "Clean and Start Again")

    def bindButtons(self):
        self.Bind(wx.EVT_BUTTON, self.retToMenu, self.menu_btn)
        self.Bind(wx.EVT_BUTTON, self.loadDependencies, self.load_btn)
        self.Bind(wx.EVT_BUTTON, self.save, self.save_btn)
        self.Bind(wx.EVT_BUTTON, self.createDependencies, self.create_btn)
        self.Bind(wx.EVT_BUTTON, self.clean, self.clean_btn)

    def initButtonsSizer(self):
        self.buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonsSizer.Add(self.menu_btn, 0, wx.EXPAND, 5)
        self.buttonsSizer.Add(self.load_btn, 0, wx.EXPAND, 5)
        self.buttonsSizer.Add(self.save_btn, 0, wx.EXPAND, 5)
        self.buttonsSizer.Add(self.create_btn, 0, wx.EXPAND, 5)
        self.buttonsSizer.Add(self.clean_btn)

    def initGraphSpaces(self):
        self.graphsSpaces = GraphsSpaces(self)

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddSpacer(20)
        rootSizer.Add(self.chosenSetSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        rootSizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)
        rootSizer.AddSpacer(CREATOR_MAIN_PANEL_ROOT_SPACER_SIZE)
        rootSizer.Add(self.dependenciesPartsHorizontalSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(CREATOR_MAIN_PANEL_ROOT_SPACER_SIZE)
        rootSizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)
        rootSizer.AddSpacer(10)
        rootSizer.Add(self.image_one_horizontal_sizer, 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        rootSizer.Add(self.image_two_horizontal_sizer, 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        rootSizer.Add( wx.StaticLine(self, -1), 0, wx.EXPAND)
        rootSizer.AddSpacer(CREATOR_MAIN_PANEL_ROOT_SPACER_SIZE)
        rootSizer.Add(self.buttonsSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(50)
        rootSizer.Add(self.graphsSpaces,0,wx.CENTER)
        rootSizer.AddSpacer(CREATOR_MAIN_PANEL_ROOT_SPACER_SIZE + 100)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])
        self.SetSizer(rootSizer)

    def initButtonsPanel(self):
        self.createButtons()
        self.bindButtons()
        self.initButtonsSizer()

    def initCreatorView(self):
        self.SetupScrolling()
        self.initChosenSetNameSizer()
        self.initChildrenDependenciesPanelsSizer()
        self.initLogAreaSizer()
        self.initDependenciesPanelsPartHorizontalSizer()
        self.initTextureOneHorizontalSizer()
        self.initTextureTwoHorizontalSizer()
        self.initButtonsPanel()
        self.initGraphSpaces()
        self.initRootSizer()
        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def __init__(self, parent, size, frame, current_dependencies, sender):
        self.sender = sender
        ScrolledPanel.__init__(self, size = size, parent=parent, style=wx.SIMPLE_BORDER)
        self.parent = parent
        self.size = size
        self.ackMsgs = {}
        self.imageOneFile = "Grass.png"
        self.imageTwoFile = "Grass2.png"
        self.wakeUpData = None
        self.current_dependencies = current_dependencies # all dependencies will be stored here
        self.frame = frame
        self.initCreatorView()

    def onShow(self, event):
        if event.GetShow():
            self.resetContents()
            if not self.wakeUpData == None:
                try:
                    self.logArea.SetValue(self.wakeUpData["Log"])
                except:
                    pass #no need to panic
                self.wakeUpData = None

    def onImageOneSelected(self, event):
        dlg = wx.FileDialog(
            self,
            defaultDir=relative_textures_path, #"..\\..\\resources\\Textures\\",
            mesage="Choose an image",
            wildcard="*.png|*.jpg",
            style=wx.FD_OPEN
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "Filename:", dlg.GetFilename()
            self.texture_one_name = dlg.GetFilename()
            image = wx.Image(path)
            image = image.Scale(32,32)
            self.imageBitmapOne.SetBitmap(wx.BitmapFromImage(image))

    def onImageTwoSelected(self, event):
        dlg = wx.FileDialog(
            self,
            defaultDir=relative_textures_path, #"..\\..\\resources\\Textures\\",
            message="Choose an image",
            wildcard="*.png|*.jpg",
            style=wx.FD_OPEN
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "Filename:", dlg.GetFilename()
            self.texture_two_name = dlg.GetFilename()
            image = wx.Image(path)
            image = image.Scale(32,32)
            self.imageBitmapTwo.SetBitmap(wx.BitmapFromImage(image))

    def retToMenu(self, event):
        # self.retToMenuViaSockets()
        self.returnToMenuPy4J()

    def returnToMenuPy4J(self):
        self.sender.entry_point.getCreatorPresenter().returnToMenu()

    def getContents(self):
        contents_copy = dict(self.current_dependencies)
        return contents_copy

    def save(self, event):
        dependencies = self.current_dependencies
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

    def dependencyLoadFail(self):
        errorMsg = "Not a valid file format, need a .dep file with a valid format"
        print errorMsg
        self.logArea.SetValue(errorMsg)

    def clean(self, event):
        self.current_dependencies["Buildings"] = {}
        self.current_dependencies["Resources"] = {}
        self.current_dependencies["Dwellers"] = {}
        self.resetContents()
        self.logArea.SetValue("Restored default settings")
        self.graphsSpaces.resetViewFromJSON({"Dwellers":[], "Buildings":[], "Resources":[]})

    def resetContents(self):
        self.logArea.SetValue(WELCOME_MSG)
        self.dependenciesSetNameInput.SetValue("Default Set")
        image_one = wx.Image(relative_textures_path + "Grass.png")
        image_one = image_one.Scale(32,32)
        self.imageBitmapOne.SetBitmap(wx.BitmapFromImage(image_one))
        self.texture_one_name = "Grass.png"

        image_two = wx.Image(relative_textures_path+"Grass2.png")
        image_two = image_two.Scale(32,32)
        self.imageBitmapTwo.SetBitmap(wx.BitmapFromImage(image_two))
        self.texture_two_name = "Grass2.jpg"

        buildingsNames, resourceNames, dwellersNames = self.current_dependencies["Buildings"].keys(), \
                                                       self.current_dependencies["Resources"].keys(), \
                                                       self.current_dependencies["Dwellers"].keys()
        self.resourcesDependenciesPanel.list_box.Clear()
        self.buildingsDependenciesPanel.list_box.Clear()
        self.dwellersDependenciesPanel.list_box.Clear()
        for resourceName in resourceNames : self.resourcesDependenciesPanel.list_box.Append(resourceName)
        for buildingName in buildingsNames : self.buildingsDependenciesPanel.list_box.Append(buildingName)
        for dwellerName in dwellersNames : self.dwellersDependenciesPanel.list_box.Append(dwellerName)
        for child in self.children: child.resetContents()

    def resetView(self):
        self.resetContents()
        for child in self.children:
            child.resetContents()


    def fillDepenendenciesPanelsWithContent(self, content_dict):
        for key in content_dict: self.current_dependencies[key] = content_dict[key]

    def checkDependenciesPanelsCorrectness(self):
        self.resetContents()
        try:
            resources = self.current_dependencies["Resources"]
            buildings = self.current_dependencies["Buildings"]
            dwellers = self.current_dependencies["Dwellers"]
            for resource in resources:
                self.frame.views["Resources"].setUpEditMode(resource) #check if filling gets correctly and there is no exception
            for building in buildings:
                self.frame.views["Buildings"].setUpEditMode(building)
            for dweller in dwellers:
                self.frame.views["Dwellers"].setUpEditMode(dweller)
        except Exception:
            return False
        return True

    def fetchDependenciesDict(self):
        buildings = self.current_dependencies["Buildings"]
        resources = self.current_dependencies["Resources"]
        dwellers = self.current_dependencies["Dwellers"]
        return {"Buildings": buildings.values(), "Resources":resources.values(), "Dwellers":dwellers.values()}

    def dependenciesSetNameTypedCorrectly(self, setName):
        if re.sub(r'\s', "", setName) == "":
            errorMsg = "Please, fill dependencies set name field"
            print errorMsg
            self.logArea.SetValue(errorMsg)
            return False
        return True

    def createDependencies(self, event):
        dependencies = self.fetchDependenciesDict()
        setName = self.dependenciesSetNameInput.GetValue()
        if not self.dependenciesSetNameTypedCorrectly(setName): return

        msg = "Dependencies sent to further processing to creator controller"
        print msg + "\n" + json.dumps(dependencies, indent=4)
        self.logArea.SetLabelText(msg)

        # self.sendDependenciesViaSockets(dependencies, setName)
        self.sendDependenciesPy4J(dependencies, setName)

    def sendDependenciesPy4J(self, dependencies, setName):
        creatorData = CreatorData(self.sender).receiveFromDict(dependencies)
        creatorData.setDependenciesSetName(setName)
        creatorData.setTextureOne(self.texture_one_name)
        creatorData.setTextureOne(self.texture_two_name)
        self.sender.entry_point.getCreatorPresenter().createDependencies(creatorData)

    def displayDependenciesGraph(self, jsonGraph):
        self.graphsSpaces.resetViewFromJSON(jsonGraph)

    def displayMsg(self, msg):
        self.logArea.SetLabelText(msg)

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
                        grids_copy = self.getContents() #if sth goes wrong, we can restore previous state
                        self.fillDepenendenciesPanelsWithContent(dependency_dict)
                        if not self.checkDependenciesPanelsCorrectness():
                            self.fillDepenendenciesPanelsWithContent(grids_copy) #here we restore previous state of subpanels
                            self.resetView()
                            errorMsg = "Error while loading file, previous dependency set still on board"
                            print errorMsg
                            self.logArea.SetValue(errorMsg)
                        else: #we're good, just reload view and praise lord
                            self.resetView()
                            msg = "Dependencies loaded successfully!"
                            print msg
                            self.logArea.SetLabelText(msg)
                    except Exception:
                        self.dependencyLoadFail()
                        traceback.print_exc()
            else:
                self.dependencyLoadFail()



    def sendDependenciesViaSockets(self, dependencies, setName):
        uuid = uuid4().__str__()
        self.ackMsgs[uuid] = False
        msg = {}
        msg["To"] = "CreatorNode"
        msg["Operation"] = "Parse"
        msg["Args"] = {}
        msg["Args"]["Dependencies"] = dependencies
        msg["Args"]["DependenciesSetName"] = setName
        msg["Args"]["UUID"] = uuid
        msg["Args"]["Texture One"] = self.texture_one_name
        msg["Args"]["Texture Two"] = self.texture_two_name
        stream = json.dumps(msg, indent=4)
        print stream
        self.sender.send(stream)
        while not self.ackMsgs[uuid]: pass


    def retToMenuViaSockets(self):
        msg = {}
        msg["To"] = "CreatorNode"
        msg["Operation"] = "MoveTo"
        msg["Args"] = {}
        msg["Args"]["TargetView"] = "MainMenu"
        msg["Args"]["TargetControlNode"] = "MainMenuNode"
        self.sender.send(json.dumps(msg))

    def readMsg(self, msg):
        CreatorMsgReader(self).reactOnMsg(msg)