import json
import re
import traceback
from uuid import uuid4

import wx
from wx.lib.scrolledpanel import ScrolledPanel

from DependenciesSubPanel import DependenciesSubPanel
from GraphsSpaces import GraphsSpaces
from LogMessages import WELCOME_MSG
from RelativePaths import relative_dependencies_path,relative_textures_path
from utils.ButtonsFactory import ButtonsFactory
from utils.JSONMonter import JSONMonter
from utils.OnShowUtil import OnShowUtil
from utils.SocketMsgReader.CreatorMsgReader import CreatorMsgReader
from viewmodel.CreatorData import CreatorData
from viewmodel.DependenciesFileLoader import DependenciesFileLoader


class CreatorMainPanel(ScrolledPanel):

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
        self.subpanels = []
        self.initCreatorView()

    def initCreatorView(self):
        self.SetupScrolling()
        self.initRootSizer()
        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def newLine(self):
        return wx.StaticLine(self, -1)

    def addToSizerWithSpace(self, sizer, view, space = 10, alignment = wx.CENTER):
        sizer.Add(view, 0, alignment)
        sizer.AddSpacer(space)

    def addToSizerWithSpaceAndLine(self, sizer, view, linePadding = 75, viewSpace = 10):
        self.addToSizerWithSpace(sizer, view, space=viewSpace)
        self.addToSizerWithSpace(sizer, self.newLine(), alignment=wx.EXPAND, space=linePadding)

    def newRootSizer(self, topPadding):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddSpacer(topPadding)
        self.addToSizerWithSpaceAndLine(rootSizer, self.newChosenSetNameSizer())
        self.addToSizerWithSpaceAndLine(rootSizer,self.newDependenciesSubpanelsHorizontalSizer(), linePadding=10, viewSpace=75)
        self.addToSizerWithSpace(rootSizer, self.newBackgroundTextureOneHorizontalSizer())
        self.addToSizerWithSpaceAndLine(rootSizer, self.newBackgroundTextureTwoHorizontalSizer())
        self.addToSizerWithSpace(rootSizer, self.newButtonsSizer(), space = 50)
        self.addToSizerWithSpace(rootSizer, self.newGraphSpaces(), space=175)
        return rootSizer

    def initRootSizer(self, topPadding = 20):
        rootSizer = self.newRootSizer(topPadding)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])
        self.SetSizer(rootSizer)

    def newInfoST(self, desc):
        return wx.StaticText(self, -1, desc)

    def newNameInput(self):
        self.dependenciesSetNameInput = wx.TextCtrl(self, -1, "Default Set")
        return self.dependenciesSetNameInput

    def newChosenSetNameSizer(self):
        self.chosenSetSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(self.chosenSetSizer, self.newInfoST("Name of this dependencies set"))
        self.chosenSetSizer.Add(self.newNameInput())
        return self.chosenSetSizer

    def newSubPanel(self, panelName, displayedEntitiesNames):
       subpanel = DependenciesSubPanel(self, panelName, displayedEntitiesNames, self.frame, self.current_dependencies)
       self.subpanels.append(subpanel)
       return subpanel

    def newResourcesSubpanel(self):
        self.resourcesDependenciesSubPanel = self.newSubPanel("Resources", self.getCurrentResourcesNames())
        return self.resourcesDependenciesSubPanel

    def newBuildingsSubpanel(self):
        self.buildingsDependenciesSubPanel = self.newSubPanel("Buildings", self.getCurrentBuildingsNames())
        return self.buildingsDependenciesSubPanel

    def newDwellersSubpanel(self):
        self.dwellersDependenciesSubPanel = self.newSubPanel("Dwellers", self.getCurrentDwellersNames())
        return self.dwellersDependenciesSubPanel

    def newDependenciesSubPanelsVerticalSizer(self):
        self.dependenciesSubpanelsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.dependenciesSubpanelsVerticalSizer.Add(self.newResourcesSubpanel(), 0, wx.CENTER)
        self.dependenciesSubpanelsVerticalSizer.Add(self.newBuildingsSubpanel(), 0, wx.CENTER)
        self.dependenciesSubpanelsVerticalSizer.Add(self.newDwellersSubpanel(), 0, wx.CENTER)
        return self.dependenciesSubpanelsVerticalSizer

    def newDependenciesSubpanelsHorizontalSizer(self):
        self.dependenciesSubpanelsHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(self.dependenciesSubpanelsHorizontalSizer, self.newDependenciesSubPanelsVerticalSizer())
        self.dependenciesSubpanelsHorizontalSizer.Add(self.newLogAreaSizer())
        return self.dependenciesSubpanelsHorizontalSizer

    def newLogArea(self):
        # height of a logArea textctrl comes from the equation:
        #  h = dependencyPanel_height * dependenciesPanelsAmount + part_desc_label_height * dependenciesPanelsAmount
        self.logArea = wx.TextCtrl(parent = self, id=-1, size=(400, 90 * 3 + 10 * 3), style=wx.TE_MULTILINE | wx.TE_READONLY)
        return self.logArea

    def newLogAreaSizer(self):
        self.logAreaVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.logAreaVerticalSizer.Add(self.newInfoST("Log area, shows important information"))
        self.logAreaVerticalSizer.Add(self.newLogArea())
        return self.logAreaVerticalSizer

    def newImageSelectorButton(self, onImgChangeCallback):
        img_selector_btn = wx.Button(self, -1, label = "Choose another texture", size = (-1, 32))
        self.Bind(wx.EVT_BUTTON, onImgChangeCallback, img_selector_btn)
        return img_selector_btn

    def newBitmap(self, textureName):
        image = wx.Image(name = relative_textures_path + textureName)#"..\\..\\resources\\Textures\\Grass.png"
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))

    def newBackgroundTextureHorizontalSizer(self, imageBitmap, info, onImageChangeCallback):
        texture_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(texture_horizontal_sizer, self.newInfoST(info))
        self.addToSizerWithSpace(texture_horizontal_sizer, imageBitmap)
        texture_horizontal_sizer.Add(self.newImageSelectorButton(onImageChangeCallback))
        return texture_horizontal_sizer

    def newBackgroundBitmapOne(self):
        self.imageBitmapOne = self.newBitmap(self.texture_one_name)
        return self.imageBitmapOne

    def newBackgroundTextureOneHorizontalSizer(self):
        self.image_one_horizontal_sizer = self.newBackgroundTextureHorizontalSizer(
            self.newBackgroundBitmapOne(),
            "Your background texture number one: ",
            self.onSelectImageOne
        )
        return self.image_one_horizontal_sizer

    def newBackgroundBitmapTwo(self):
        self.imageBitmapTwo = self.newBitmap(self.texture_two_name)
        return self.imageBitmapTwo

    def newBackgroundTextureTwoHorizontalSizer(self):
        self.image_two_horizontal_sizer = self.newBackgroundTextureHorizontalSizer(
            self.newBackgroundBitmapTwo(),
            "Your background texture number two: ",
            self.onSelectImageTwo
        )
        return self.image_two_horizontal_sizer

    def newMenuButton(self):
        self.menu_btn = ButtonsFactory().newButton(self, "Menu", self.retToMenu)
        return self.menu_btn

    def newLoadButton(self):
        self.load_btn = ButtonsFactory().newButton(self, "Load dependencies From File", self.loadDependencies)
        return self.load_btn

    def newSaveButton(self):
        self.save_btn = ButtonsFactory().newButton(self, "Save these dependencies to File", self.save)
        return self.save_btn

    def newCreateButton(self):
        self.create_btn = ButtonsFactory().newButton(self, "Create", self.createDependencies)
        return self.create_btn

    def newCleanButton(self):
        self.clean_btn = ButtonsFactory().newButton(self, "Clean and Start Again", self.clean)
        return self.clean_btn

    def newButtonsSizer(self):
        self.buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.buttonsSizer.Add(self.newMenuButton(), 0, wx.EXPAND, 5)
        self.buttonsSizer.Add(self.newLoadButton(), 0, wx.EXPAND, 5)
        self.buttonsSizer.Add(self.newSaveButton(), 0, wx.EXPAND, 5)
        self.buttonsSizer.Add(self.newCreateButton(), 0, wx.EXPAND, 5)
        self.buttonsSizer.Add(self.newCleanButton())
        return self.buttonsSizer

    def newGraphSpaces(self):
        self.graphsSpaces = GraphsSpaces(self)
        return self.graphsSpaces

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
                f.write(json.dumps(self.current_dependencies, indent=4).replace(",",",\n"))

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
        dependenciesPanel.entities_names_listbox.Clear()
        for value in values: dependenciesPanel.entities_names_listbox.Append(value)

    def refreshDependenciesPanels(self):
        self.refreshDependenciesPanel(self.resourcesDependenciesSubPanel, self.getCurrentResourcesNames())
        self.refreshDependenciesPanel(self.buildingsDependenciesSubPanel, self.getCurrentBuildingsNames())
        self.refreshDependenciesPanel(self.dwellersDependenciesSubPanel, self.getCurrentDwellersNames())

    def getCurrentBuildingsNames(self):
        return self.current_dependencies["Buildings"].keys()

    def getCurrentResourcesNames(self):
        return self.current_dependencies["Resources"].keys()

    def getCurrentDwellersNames(self):
        return self.current_dependencies["Dwellers"].keys()

    def refreshChildren(self):
        for child in self.subpanels: child.resetContents()

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
        dependencies = self.fetchDependenciesDictStrippedOfEntitiesNameKeys()
        setName = self.dependenciesSetNameInput.GetValue()
        if not self.dependenciesSetNameTypedCorrectly(setName): return
        msg = "Dependencies sent to further processing to creator controller"
        self.logArea.SetLabelText(msg)
        self.sendDependenciesPy4J(dependencies, setName)

    def fetchDependenciesDictStrippedOfEntitiesNameKeys(self):
        buildings = self.current_dependencies["Buildings"]
        resources = self.current_dependencies["Resources"]
        dwellers = self.current_dependencies["Dwellers"]
        return {"Buildings": buildings.values(), "Resources": resources.values(), "Dwellers": dwellers.values()}

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