import wx
from wx.lib.scrolledpanel import ScrolledPanel

from CreatorView.DependenciesFileLoader import DependenciesFileLoader
from DependenciesPanel import DependenciesPanel
from LogMessages import WELCOME_MSG
import json
from RelativePaths import relative_dependencies_path,relative_textures_path
import traceback
import re
from uuid import uuid4
from GraphsSpaces import GraphsSpaces
from utils.JSONMonter import JSONMonter
from utils.OnShowUtil import OnShowUtil
from utils.SocketMsgReader.CreatorMsgReader import CreatorMsgReader
from viewmodel.CreatorData import CreatorData


class CreatorMainEntry(ScrolledPanel):

    def __init__(self, parent, size, frame, current_dependencies, sender):
        self.sender = sender
        ScrolledPanel.__init__(self, size = size, parent=parent, style=wx.SIMPLE_BORDER)
        self.parent = parent
        self.size = size
        self.ackMsgs = {}
        self.texture_one_name = "Grass.png"
        self.texture_two_name = "Grass2.jpg"
        self.wakeUpData = None
        self.current_dependencies = current_dependencies # all dependencies will be stored here
        self.frame = frame
        self.initCreatorView()

    def initCreatorView(self):
        self.SetupScrolling()
        self.initChosenSetNameSizer()
        self.initChildrenDependenciesPanelsSizer()
        self.initLogAreaSizer()
        self.initDependenciesPanelsPartHorizontalSizer()
        self.initBackgroundTextureOneHorizontalSizer()
        self.initBackgroundTextureTwoHorizontalSizer()
        self.initButtonsPanel()
        self.initGraphSpaces()
        self.initRootSizer()
        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def initChosenSetNameSizer(self):
        self.chosenSetSizer = wx.BoxSizer(wx.HORIZONTAL)
        dependenciesSetNameLabel = wx.StaticText(self,-1, "Name of this dependencies set")
        self.dependenciesSetNameInput = wx.TextCtrl(self, -1, "Default Set")
        self.chosenSetSizer.Add(dependenciesSetNameLabel)
        self.chosenSetSizer.AddSpacer(5)
        self.chosenSetSizer.Add(self.dependenciesSetNameInput)

    def getSubPanel(self, panelName, displayedEntitiesNames):
           return \
               DependenciesPanel(
                   self,
                   self.dependenciesPartsVerticalSizer,
                   panelName,
                   displayedEntitiesNames,
                   self.frame,
                   self.current_dependencies
               )


    def initChildrenDependenciesPanelsSizer(self):
        self.dependenciesPartsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.resourcesDependenciesPanel = self.getSubPanel("Resources", self.getCurrentResourcesNames())
        self.buildingsDependenciesPanel = self.getSubPanel("Buildings", self.getCurrentBuildingsNames())
        self.dwellersDependenciesPanel = self.getSubPanel("Dwellers", self.getCurrentDwellersNames())
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

    def getImageSelectorButton(self,onImgChangeCallback):
        img_selector_btn = wx.Button(self, -1, label = "Choose another texture", size = (-1, 32))
        self.Bind(wx.EVT_BUTTON, onImgChangeCallback, img_selector_btn)
        return img_selector_btn

    def getBitmap(self,  textureName):
        image = wx.Image(name = relative_textures_path + textureName)#"..\\..\\resources\\Textures\\Grass.png"
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))

    def getBackgroundInfoST(self, desc):
        return wx.StaticText(self, -1, desc)

    def initBackgroundTextureHorizontalSizer(self, imageBitmap, info, onImageChangeCallback):
        image_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        image_horizontal_sizer.Add(self.getBackgroundInfoST(info))
        image_horizontal_sizer.AddSpacer(10)
        image_horizontal_sizer.Add(imageBitmap)
        image_horizontal_sizer.AddSpacer(10)
        image_horizontal_sizer.Add(self.getImageSelectorButton(onImageChangeCallback))
        return image_horizontal_sizer

    def newBitmapOne(self):
        self.imageBitmapOne = self.getBitmap(self.texture_one_name)
        return self.imageBitmapOne

    def initBackgroundTextureOneHorizontalSizer(self):
        self.image_one_horizontal_sizer = self.initBackgroundTextureHorizontalSizer(
            self.newBitmapOne(),
            "Your background texture number one: ",
            self.onSelectImageOne
        )

    def newBitmapTwo(self):
        self.imageBitmapTwo = self.getBitmap(self.texture_two_name)
        return self.imageBitmapTwo

    def initBackgroundTextureTwoHorizontalSizer(self):
        self.image_two_horizontal_sizer = self.initBackgroundTextureHorizontalSizer(
            self.newBitmapTwo(),
            "Your background texture number two: ",
            self.onSelectImageTwo
        )

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

    def initButtonsPanel(self):
        self.createButtons()
        self.bindButtons()
        self.initButtonsSizer()

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddSpacer(20)
        rootSizer.Add(self.chosenSetSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        rootSizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)
        rootSizer.AddSpacer(75)
        rootSizer.Add(self.dependenciesPartsHorizontalSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(75)
        rootSizer.Add(wx.StaticLine(self, -1), 0, wx.EXPAND)
        rootSizer.AddSpacer(10)
        rootSizer.Add(self.image_one_horizontal_sizer, 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        rootSizer.Add(self.image_two_horizontal_sizer, 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        rootSizer.Add( wx.StaticLine(self, -1), 0, wx.EXPAND)
        rootSizer.AddSpacer(75)
        rootSizer.Add(self.buttonsSizer, 0, wx.CENTER)
        rootSizer.AddSpacer(50)
        rootSizer.Add(self.graphsSpaces,0,wx.CENTER)
        rootSizer.AddSpacer(175)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])
        self.SetSizer(rootSizer)

    def onShow(self, event):
        OnShowUtil().onCreatorPanelShow(self, event)

    def createImageSelectionDialog(self):
        return wx.FileDialog(
            self,
            defaultDir=relative_textures_path, #"..\\..\\resources\\Textures\\",
            message="Choose an image",
            wildcard="*.png|*.jpg",
            style=wx.FD_OPEN
        )

    def  onImageSelected(self, dlg, imageBitmap):
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            image = wx.Image(path)
            image = image.Scale(32,32)
            imageBitmap.SetBitmap(wx.BitmapFromImage(image))

    def onSelectImageOne(self, event):
        dlg = self.createImageSelectionDialog()
        self.onImageSelected(dlg, self.imageBitmapOne)
        self.texture_one_name = dlg.GetFilename()

    def onSelectImageTwo(self, event):
        dlg = self.createImageSelectionDialog()
        self.onImageSelected(dlg, self.imageBitmapTwo)
        self.texture_two_name = dlg.GetFilename()

    def retToMenu(self, event):
        self.sender.entry_point.getCreatorPresenter().returnToMenu()

    def fetchDependenciesCopy(self):
        return dict(self.current_dependencies)

    def createSaveDialog(self):
        return wx.FileDialog(
            self,
            defaultDir = relative_dependencies_path,
            message = "Choose a file to save",
            wildcard = "*.dep",
            style = wx.FD_SAVE
        )

    def onSaveDependencies(self, dlg):
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            with open(path, "wb+") as f:
                f.write(json.dumps(self.current_dependencies).replace(",",",\n"))

    def save(self, event):
        dlg = self.createSaveDialog()
        self.onSaveDependencies(dlg)

    def dependencyLoadFail(self):
        errorMsg = "Not a valid file format, need a .dep file with a valid format"
        self.logArea.SetValue(errorMsg)

    def cleanCurrentDependencies(self):
        self.current_dependencies["Buildings"] = {}
        self.current_dependencies["Resources"] = {}
        self.current_dependencies["Dwellers"] = {}

    def clean(self, event):
        self.cleanCurrentDependencies()
        self.resetContents()
        self.graphsSpaces.resetViewFromJSON({"Dwellers":[], "Buildings":[], "Resources":[]})
        self.logArea.SetValue("Restored default settings")

    def createScaledBitmap(self, bmp, img_path):
        image = wx.Image(img_path)
        image = image.Scale(32,32)
        bmp.SetBitmap(wx.BitmapFromImage(image))

    def refreshDependenciesPanel(self, dependenciesPanel, values):
        dependenciesPanel.list_box.Clear()
        for value in values: dependenciesPanel.list_box.Append(value)

    def refreshDependenciesPanels(self):
        self.refreshDependenciesPanel(self.resourcesDependenciesPanel, self.getCurrentResourcesNames())
        self.refreshDependenciesPanel(self.buildingsDependenciesPanel, self.getCurrentBuildingsNames())
        self.refreshDependenciesPanel(self.dwellersDependenciesPanel, self.getCurrentDwellersNames())

    def getCurrentBuildingsNames(self):
        return self.current_dependencies["Buildings"].keys()

    def getCurrentResourcesNames(self):
        return self.current_dependencies["Resources"].keys()

    def getCurrentDwellersNames(self):
        return self.current_dependencies["Dwellers"].keys()

    def refreshChildren(self):
        for child in self.children: child.resetContents()

    def updateTextureOne(self, imageName):
        self.createScaledBitmap(self.imageBitmapOne, relative_textures_path +imageName)
        self.texture_one_name = imageName

    def updateTextureTwo(self, imageName):
        self.createScaledBitmap(self.imageBitmapTwo, relative_textures_path+imageName)
        self.texture_two_name = imageName

    def refreshBackgroundTextures(self):
        self.updateTextureOne("Grass.png")
        self.updateTextureTwo("Grass2.jpg")

    def resetContents(self):
        self.dependenciesSetNameInput.SetValue("Default Set")
        self.refreshBackgroundTextures()
        self.refreshChildren()
        self.refreshDependenciesPanels()

    def resetView(self):
        self.resetContents()
        self.logArea.SetValue(WELCOME_MSG)

    def fillCurrentDependenciesWithContent(self, content_dict):
        for key in content_dict: self.current_dependencies[key] = content_dict[key]

    def checkCorrectnessOf(self, dependencyName):
        # checks if filling ends correctly and there is no exception
        try:
            for dependency in self.current_dependencies[dependencyName]:
                self.frame.setupPanelEditMode(panelName = dependencyName, editedElementName = dependency)
        except Exception:
            traceback.print_exc()
            return False
        return True

    def fileContentsCorrect(self):
        self.resetContents()
        input_correct = self.checkCorrectnessOf("Resources")
        input_correct &= self.checkCorrectnessOf("Buildings")
        input_correct &= self.checkCorrectnessOf("Dwellers")
        return input_correct

    def dependenciesSetNameTypedCorrectly(self, setName):
        if re.sub(r'\s', "", setName) == "":
            errorMsg = "Please, fill dependencies set name field"
            self.logArea.SetValue(errorMsg)
            return False
        return True

    def createDependencies(self, event):
        dependencies = self.fetchDependenciesDictStrappedOfEntitiesNameKeys()
        setName = self.dependenciesSetNameInput.GetValue()
        if not self.dependenciesSetNameTypedCorrectly(setName): return
        msg = "Dependencies sent to further processing to creator controller"
        self.logArea.SetLabelText(msg)
        self.sendDependenciesPy4J(dependencies, setName)

    def sendDependenciesPy4J(self, dependencies, setName):
        creatorData = CreatorData(self.sender).receiveFromDict(dependencies)
        creatorData.setDependenciesSetName(setName)
        creatorData.setTextureOne(self.texture_one_name)
        creatorData.setTextureTwo(self.texture_two_name)
        self.sender.entry_point.getCreatorPresenter().createDependencies(creatorData)

    def displayDependenciesGraph(self, jsonGraph):
        self.graphsSpaces.resetViewFromJSON(jsonGraph)

    def displayMsg(self, msg):
        self.logArea.SetLabelText(msg)

    def loadDependencies(self, event):
        dlg = self.createLoadDialog()
        self.onLoadFileSelected(dlg)

    def fetchDependenciesDictStrappedOfEntitiesNameKeys(self):
        buildings = self.current_dependencies["Buildings"]
        resources = self.current_dependencies["Resources"]
        dwellers = self.current_dependencies["Dwellers"]
        return {"Buildings": buildings.values(), "Resources": resources.values(), "Dwellers": dwellers.values()}

    def createLoadDialog(self):
        return wx.FileDialog(
            self,
            defaultDir = relative_dependencies_path,
            message = "Choose a file",
            wildcard="*.dep",
            style = wx.FD_OPEN | wx.FD_MULTIPLE
        )

    def onLoadFileSelected(self, dlg):
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            DependenciesFileLoader(self).onLoadFileSelected(path)

    def sendDependenciesViaSockets(self, dependencies, setName):
        uuid = uuid4().__str__()
        self.ackMsgs[uuid] = False
        msg = JSONMonter().mountCreatorParseMsg(self, dependencies, setName, uuid)
        stream = json.dumps(msg, indent=4)
        self.sender.send(stream)
        while not self.ackMsgs[uuid]: pass

    def retToMenuViaSockets(self):
        msg = JSONMonter().mountMoveToMsg("CreatorNode", "MainMenu")
        self.sender.send(json.dumps(msg))

    def readMsg(self, msg):
        CreatorMsgReader(self).reactOnMsg(msg)