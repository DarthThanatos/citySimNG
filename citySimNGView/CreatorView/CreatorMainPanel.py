import json
import re
import traceback
from uuid import uuid4

import os.path
import wx
from wx.lib.scrolledpanel import ScrolledPanel

from CreatorView import Consts
from DependenciesSubPanel import DependenciesSubPanel
from GraphsSpaces import GraphsSpaces
from RelativePaths import relative_dependencies_path, relative_textures_path
from utils import LogMessages
from utils.ButtonsFactory import ButtonsFactory
from utils.JSONMonter import JSONMonter
from utils.LogMessages import WELCOME_MSG
from utils.OnShowUtil import OnShowUtil
from utils.SocketMsgReader.CreatorMsgReader import CreatorMsgReader
from viewmodel.CreatorData import CreatorData
from viewmodel.DependenciesFileLoader import DependenciesFileLoader
from viewmodel.SheetEntityChecker import EditModeSheetEntityChecker


class CreatorMainPanel(ScrolledPanel):

    def __init__(self, parent, size, frame, current_dependencies, sender):
        self.sender = sender
        ScrolledPanel.__init__(self, size = size, parent=parent, style=wx.SIMPLE_BORDER)
        self.parent = parent
        self.size = size
        self.ackMsgs = {}
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
        self.resourcesDependenciesSubPanel = self.newSubPanel(Consts.RESOURCES, self.getCurrentResourcesNames())
        return self.resourcesDependenciesSubPanel

    def newBuildingsSubpanel(self):
        self.buildingsDependenciesSubPanel = self.newSubPanel(Consts.BUILDINGS, self.getCurrentBuildingsNames())
        return self.buildingsDependenciesSubPanel

    def newDwellersSubpanel(self):
        self.dwellersDependenciesSubPanel = self.newSubPanel(Consts.DWELLERS, self.getCurrentDwellersNames())
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
        return ButtonsFactory().newButton(self, "Choose another texture", onImgChangeCallback, size=(-1, 32), hint = LogMessages.BACKGROUND_TEXTURE_SELECTION_BTN_HINT)

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
        self.imageBitmapOne = self.newBitmap(self.current_dependencies[Consts.TEXTURE_ONE])
        return self.imageBitmapOne

    def newBackgroundTextureOneHorizontalSizer(self):
        self.image_one_horizontal_sizer = self.newBackgroundTextureHorizontalSizer(
            self.newBackgroundBitmapOne(),
            "Your background texture number one: ",
            self.onSelectImageOne
        )
        return self.image_one_horizontal_sizer

    def newBackgroundBitmapTwo(self):
        self.imageBitmapTwo = self.newBitmap(self.current_dependencies[Consts.TEXTURE_TWO])
        return self.imageBitmapTwo

    def newBackgroundTextureTwoHorizontalSizer(self):
        self.image_two_horizontal_sizer = self.newBackgroundTextureHorizontalSizer(
            self.newBackgroundBitmapTwo(),
            "Your background texture number two: ",
            self.onSelectImageTwo
        )
        return self.image_two_horizontal_sizer

    def newMenuButton(self):
        self.menu_btn = ButtonsFactory().newButton(self, "Menu", self.retToMenu, hint = LogMessages.MENU_BTN_HINT)
        return self.menu_btn

    def newLoadButton(self):
        self.load_btn = ButtonsFactory().newButton(self, "Load dependencies From File", self.loadDependencies, hint = LogMessages.LOAD_DEPS_BTN_HINT)
        return self.load_btn

    def newSaveButton(self):
        self.save_btn = ButtonsFactory().newButton(self, "Save these dependencies to File", self.save, hint = LogMessages.SAVE_DEPS_BTN_HINT)
        return self.save_btn

    def newCreateButton(self):
        self.create_btn = ButtonsFactory().newButton(self, "Create", self.createDependencies, hint = LogMessages.CREATE_DEPS_BTN_HINT)
        return self.create_btn

    def newCleanButton(self):
        self.clean_btn = ButtonsFactory().newButton(self, "Clean and Start Again", self.clean, hint = LogMessages.CLEAN_DEPS_BTN_HINT)
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
        self.current_dependencies[Consts.TEXTURE_ONE] = dlg.GetFilename()

    def onSelectImageTwo(self, event):
        dlg = self.createImageSelectionDialog()
        self.onImageSelected(dlg, self.imageBitmapTwo)
        self.current_dependencies[Consts.TEXTURE_TWO] = dlg.GetFilename()

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
        self.current_dependencies[Consts.BUILDINGS] = {}
        self.current_dependencies[Consts.RESOURCES] = {}
        self.current_dependencies[Consts.DWELLERS] = {}

    def clean(self, event):
        self.cleanCurrentDependencies()
        self.resetContents()
        self.graphsSpaces.resetViewFromJSON({Consts.DWELLERS:[], Consts.BUILDINGS:[], Consts.RESOURCES:[]})
        self.logArea.SetValue("Restored default settings")

    def createScaledBitmap(self, bmp, img_path):
        image = wx.Image(img_path)
        image = image.Scale(32,32)
        bmp.SetBitmap(wx.BitmapFromImage(image))


    def getCurrentBuildingsNames(self):
        return self.current_dependencies[Consts.BUILDINGS].keys()

    def getCurrentResourcesNames(self):
        return self.current_dependencies[Consts.RESOURCES].keys()

    def getCurrentDwellersNames(self):
        return self.current_dependencies[Consts.DWELLERS].keys()

    def refreshSubPanels(self):
        for subpanel in self.subpanels: subpanel.resetContents()

    def updateTextureOne(self):
        self.createScaledBitmap(self.imageBitmapOne, relative_textures_path + self.current_dependencies[Consts.TEXTURE_ONE])

    def updateTextureTwo(self):
        self.createScaledBitmap(self.imageBitmapTwo, relative_textures_path + self.current_dependencies[Consts.TEXTURE_TWO])

    def refreshBackgroundTextures(self):
        self.updateTextureOne()
        self.updateTextureTwo()

    def resetContents(self):
        self.dependenciesSetNameInput.SetValue(self.current_dependencies[Consts.SET_NAME])
        self.refreshBackgroundTextures()
        self.refreshSubPanels()

    def resetView(self):
        self.resetContents()
        self.logArea.SetValue(WELCOME_MSG)

    def fillCurrentDependenciesWithValidContent(self, content_dict):
        validKeys = self.parent.newCurrentDependenciesKeys()
        for key in content_dict:
            if key not in validKeys: raise Exception
            self.current_dependencies[key] = content_dict[key]

    def checkCorrectnessOf(self, dependencyPanelName):
        # checks if filling ends correctly and there is no exception
        correct = True
        try:
            for dependency in self.current_dependencies[dependencyPanelName]:
                self.frame.setupPanelEditMode(panelName = dependencyPanelName, editedElementName = dependency)
                panel = self.frame.views[dependencyPanelName]
                correct &= panel.getEntityChecker().entityCorrect(EditModeSheetEntityChecker(panel))
        except Exception:
            traceback.print_exc()
            return False
        return correct

    def textureExists(self, path):
        return os.path.isfile(relative_textures_path + path)

    def currentDependenciesCorrect(self, updateNameFromInput):
        input_correct = self.dependenciesSetNameTypedCorrectly(updateNameFromInput=updateNameFromInput)
        input_correct &= self.textureExists(self.current_dependencies[Consts.TEXTURE_ONE])
        input_correct &= self.textureExists(self.current_dependencies[Consts.TEXTURE_TWO])
        input_correct &= self.checkCorrectnessOf(Consts.RESOURCES)
        input_correct &= self.checkCorrectnessOf(Consts.BUILDINGS)
        input_correct &= self.checkCorrectnessOf(Consts.DWELLERS)
        return input_correct

    def dependenciesSetNameTypedCorrectly(self, updateNameFromInput):
        if updateNameFromInput:
            self.current_dependencies[Consts.SET_NAME] = self.dependenciesSetNameInput.GetValue()
        setName = self.current_dependencies[Consts.SET_NAME]
        if re.sub(r'\s', "", setName) == "":
            errorMsg = "Dependencies set name field not correct"
            self.logArea.SetValue(errorMsg)
            return False
        return True

    def createDependencies(self, event):
        if not self.currentDependenciesCorrect(updateNameFromInput=True): return
        dependencies = self.fetchDependenciesDictStrippedOfEntitiesNameKeys()
        self.logArea.SetLabelText(LogMessages.DEPENDENCIES_SENT_MSG)
        self.sendDependenciesPy4J(dependencies)

    def fetchDependenciesDictStrippedOfEntitiesNameKeys(self):
        buildings = self.current_dependencies[Consts.BUILDINGS]
        resources = self.current_dependencies[Consts.RESOURCES]
        dwellers = self.current_dependencies[Consts.DWELLERS]
        return {
            Consts.SET_NAME: self.current_dependencies[Consts.SET_NAME],
            Consts.TEXTURE_ONE: self.current_dependencies[Consts.TEXTURE_ONE],
            Consts.TEXTURE_TWO: self.current_dependencies[Consts.TEXTURE_TWO],
            Consts.BUILDINGS: buildings.values(),
            Consts.RESOURCES: resources.values(),
            Consts.DWELLERS: dwellers.values()
        }

    def sendDependenciesPy4J(self, dependencies):
        creatorData = CreatorData(self.sender).receiveFromDict(dependencies)
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