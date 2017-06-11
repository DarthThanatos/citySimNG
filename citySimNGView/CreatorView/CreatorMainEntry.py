import wx
from wx.lib.scrolledpanel import ScrolledPanel
from DependenciesPanel import DependenciesPanel
from LogMessages import WELCOME_MSG
import json
from pprint import PrettyPrinter
from RelativePaths import relative_dependencies_path,relative_textures_path
import traceback
import re
from uuid import uuid4
from GraphsSpaces import GraphsSpaces

class CreatorMainEntry(ScrolledPanel):
    def __init__(self, parent, size, frame, current_dependencies, lists_of_names, sender):
        self.sender = sender
        ScrolledPanel.__init__(self, size = size, parent=parent, style=wx.SIMPLE_BORDER)
        self.SetupScrolling()
        ROOT_SPACER_SIZE = 75
        self.parent = parent
        self.ackMsgs = {}
        self.imageOneFile = "Grass.png"
        self.imageTwoFile = "Grass2.png"
        self.wakeUpData = None
        self.currentDependencies = current_dependencies # all dependencies will be stored here
        self.frame = frame

        self.lists_of_names = lists_of_names
        buildingsNames, resourcesNames, dwellersNames = lists_of_names

        rootSizer = wx.BoxSizer(wx.VERTICAL)
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        chosenSetSizer = wx.BoxSizer(wx.HORIZONTAL)
        dependenciesPartsHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        dependenciesPartsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        logAreaVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        image_one_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        image_two_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

        rootSizer.AddSpacer(20)

        dependenciesSetNameLabel = wx.StaticText(self,-1, "Name of this dependencies set")
        self.dependenciesSetNameInput = wx.TextCtrl(self, -1, "Default Set")
        chosenSetSizer.Add(dependenciesSetNameLabel)
        chosenSetSizer.AddSpacer(5)
        chosenSetSizer.Add(self.dependenciesSetNameInput)

        rootSizer.Add(chosenSetSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        top_ln = wx.StaticLine(self, -1)
        rootSizer.Add(top_ln, 0, wx.EXPAND)
        rootSizer.AddSpacer(ROOT_SPACER_SIZE)

        resourcesNames = current_dependencies["Resources"].keys()
        dwellersNames = current_dependencies["Dwellers"].keys()
        buildingsNames = current_dependencies["Buildings"].keys()

        self.resourcesDependenciesPanel = DependenciesPanel(self, dependenciesPartsVerticalSizer, "Resources", resourcesNames, frame, self.currentDependencies)
        self.dwellersDependenciesPanel = DependenciesPanel(self, dependenciesPartsVerticalSizer, "Dwellers",dwellersNames,frame, self.currentDependencies)
        self.buildingsDependenciesPanel = DependenciesPanel(self, dependenciesPartsVerticalSizer, "Buildings",buildingsNames, frame, self.currentDependencies)
        self.children = [self.resourcesDependenciesPanel, self.dwellersDependenciesPanel, self.buildingsDependenciesPanel]

        self.children = [self.resourcesDependenciesPanel, self.dwellersDependenciesPanel, self.buildingsDependenciesPanel]
        dependenciesPartsHorizontalSizer.Add(dependenciesPartsVerticalSizer)

        logLabel = wx.StaticText(self, label="Log area, shows important information")
        logAreaVerticalSizer.Add(logLabel)
        self.logArea = wx.TextCtrl(parent = self, id=-1, size=(400, 90 * 3 + 10 * 3), style=wx.TE_MULTILINE | wx.TE_READONLY)
        # ^ height of a logArea textctrl comes from the equation:
        #  h = dependencyPanel_height * dependenciesPanelsAmount + part_desc_label_height * dependenciesPanelsAmount
        logAreaVerticalSizer.Add(self.logArea)
        dependenciesPartsHorizontalSizer.AddSpacer(10)
        dependenciesPartsHorizontalSizer.Add(logAreaVerticalSizer)

        rootSizer.Add(dependenciesPartsHorizontalSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(ROOT_SPACER_SIZE)

        ln = wx.StaticLine(self, -1)
        rootSizer.Add(ln, 0, wx.EXPAND)
        rootSizer.AddSpacer(10)

        img_one_info_label = wx.StaticText(self, -1, "Your background texture number one: ")
        img_one_selector_btn = wx.Button(self, -1, label = "Choose another texture", size = (-1, 32))
        self.Bind(wx.EVT_BUTTON, self.onImageOneSelected ,img_one_selector_btn)
        image = wx.Image(name = relative_textures_path + "Grass.png")#"..\\..\\resources\\Textures\\Grass.png"
        self.imageBitmapOne = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))
        self.texture_one_name = "Grass.png"
        image_one_horizontal_sizer.Add(img_one_info_label)
        image_one_horizontal_sizer.AddSpacer(10)
        image_one_horizontal_sizer.Add(self.imageBitmapOne)
        image_one_horizontal_sizer.AddSpacer(10)
        image_one_horizontal_sizer.Add(img_one_selector_btn)
        rootSizer.Add(image_one_horizontal_sizer, 0, wx.CENTER)
        rootSizer.AddSpacer(10)

        img_two_info_label = wx.StaticText(self, -1, "Your background texture number two: ")
        img_two_selector_btn = wx.Button(self, -1, label = "Choose another texture", size = (-1, 32))
        self.Bind(wx.EVT_BUTTON, self.onImageTwoSelected ,img_two_selector_btn)
        image = wx.Image(name = relative_textures_path + "Grass2.jpg") #"..\\..\\resources\\Textures\\Grass2.jpg"
        self.texture_two_name = "Grass2.jpg"
        self.imageBitmapTwo = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))
        image_two_horizontal_sizer.Add(img_two_info_label)
        image_two_horizontal_sizer.AddSpacer(10)
        image_two_horizontal_sizer.Add(self.imageBitmapTwo)
        image_two_horizontal_sizer.AddSpacer(10)
        image_two_horizontal_sizer.Add(img_two_selector_btn)
        rootSizer.Add(image_two_horizontal_sizer, 0, wx.CENTER)
        rootSizer.AddSpacer(10)

        ln = wx.StaticLine(self, -1)
        rootSizer.Add(ln, 0, wx.EXPAND)
        rootSizer.AddSpacer(ROOT_SPACER_SIZE)

        menu_btn = wx.Button(self, label="Menu")
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)
        buttonsSizer.Add(menu_btn, 0, wx.EXPAND, 5)

        load_btn = wx.Button(self, label="Load dependencies From File")
        self.Bind(wx.EVT_BUTTON, self.loadDependencies, load_btn)
        buttonsSizer.Add(load_btn, 0, wx.EXPAND, 5)

        save_btn = wx.Button(self, label="Save these dependencies to File")
        self.Bind(wx.EVT_BUTTON, self.save, save_btn)
        buttonsSizer.Add(save_btn, 0, wx.EXPAND, 5)

        create_btn = wx.Button(self, label="Create")
        self.Bind(wx.EVT_BUTTON, self.createDependencies, create_btn)
        buttonsSizer.Add(create_btn, 0, wx.EXPAND, 5)

        clean_btn = wx.Button(self, label = "Clean and Start Again")
        self.Bind(wx.EVT_BUTTON, self.clean, clean_btn)
        buttonsSizer.Add(clean_btn)

        rootSizer.Add(buttonsSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(50)
        self.graphsSpaces = GraphsSpaces(self)
        rootSizer.Add(self.graphsSpaces,0,wx.CENTER)

        rootSizer.AddSpacer(ROOT_SPACER_SIZE + 100)
        rootSizer.SetDimension(0, 0, size[0], size[1])
        self.SetSizer(rootSizer)

        self.Bind(wx.EVT_SHOW, self.onShow, self)

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
        #self.parent.setView("Menu")
        msg = {}
        msg["To"] = "CreatorNode"
        msg["Operation"] = "MoveTo"
        msg["Args"] = {}
        msg["Args"]["TargetView"] = "MainMenu"
        msg["Args"]["TargetControlNode"] = "MainMenuNode"
        self.sender.send(json.dumps(msg))

    def getContents(self):
        contents_copy = dict(self.currentDependencies)
        return contents_copy

    def save(self, event):
        dependencies = self.currentDependencies
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

    def readMsg(self, msg):
        print "Creator view got msg", msg
        jsonMsg = json.loads(msg)
        operation = jsonMsg["Operation"]
        if operation == "ParseConfirm":
            self.ackMsgs[jsonMsg["Args"]["UUID"]] = True #unblock blocked thread
            self.graphsSpaces.resetViewFromJSON(jsonMsg["Args"]["graph"])
            log_msg = "Dependencies created successfully, please go to the Loader menu now to check what was created"
            print log_msg
            self.logArea.SetLabelText(log_msg)
        elif operation == "ParseFail":
            self.ackMsgs[jsonMsg["Args"]["UUID"]] = True #unblock blocked thread
            self.logArea.SetLabelText(jsonMsg["Args"]["errorMsg"])


    def dependencyLoadFail(self):
        errorMsg = "Not a valid file format, need a .dep file with a valid format"
        print errorMsg
        self.logArea.SetValue(errorMsg)

    def clean(self, event):
        self.currentDependencies["Buildings"] = {}
        self.currentDependencies["Resources"] = {}
        self.currentDependencies["Dwellers"] = {}
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

        buildingsNames, resourceNames, dwellersNames = self.currentDependencies["Buildings"].keys(), \
                                                       self.currentDependencies["Resources"].keys(), \
                                                       self.currentDependencies["Dwellers"].keys()
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
        for key in content_dict: self.currentDependencies[key] = content_dict[key]

    def checkDependenciesPanelsCorrectness(self):
        self.resetContents()
        try:
            resources = self.currentDependencies["Resources"]
            buildings = self.currentDependencies["Buildings"]
            dwellers = self.currentDependencies["Dwellers"]
            for resource in resources:
                self.frame.views["Resources"].setUpEditMode(resource) #check if filling gets correctly and there is no exception
            for building in buildings:
                self.frame.views["Buildings"].setUpEditMode(building)
            for dweller in dwellers:
                self.frame.views["Dwellers"].setUpEditMode(dweller)
        except Exception:
            return False
        return True

    def createDependencies(self, event):
        buildings = self.currentDependencies["Buildings"]
        resources = self.currentDependencies["Resources"]
        dwellers = self.currentDependencies["Dwellers"]
        dependencies = {"Buildings": buildings.values(), "Resources":resources.values(), "Dwellers":dwellers.values()}
        pp = PrettyPrinter()
        pp.pprint(dependencies)

        setName = self.dependenciesSetNameInput.GetValue()
        if re.sub(r'\s', "", setName) == "":
            errorMsg = "Please, fill dependencies set name field"
            print errorMsg
            self.logArea.SetValue(errorMsg)
            return

        msg = "Dependencies sent to further processing to creator controller"
        print msg
        self.logArea.SetLabelText(msg)
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
        stream = json.dumps(msg)
        print stream
        self.sender.send(stream)
        while not self.ackMsgs[uuid]: pass
        """
        dwellers_tree = [["dweller.JPG"]]
        resources_tree = [["pszenica.jpg"], ["maka.jpg"], ["chleb.jpg"],["gold.jpg"]]

        firstLvl = ["farma.JPG", "bakery.png"]
        secondLvl = ["farma.JPG", "browar.JPG", "house.png"]
        thirdLvl = ["farma.JPG", "browar.JPG"]
        buildings_tree = [ firstLvl, secondLvl, thirdLvl, firstLvl]

        self.graphsSpaces.resetView([resources_tree,dwellers_tree, buildings_tree])
        """

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