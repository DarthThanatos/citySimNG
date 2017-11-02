import json
import re
import traceback
from uuid import uuid4

import os.path
import wx
from wx.lib.scrolledpanel import ScrolledPanel

from CreatorView import Consts, CreatorConfig
from DependenciesSubPanel import DependenciesSubPanel
from GraphsSpaces import GraphsSpaces
from RelativePaths import relative_dependencies_path, relative_textures_path
from utils import LogMessages
from utils.ButtonsFactory import ButtonsFactory
from utils.JSONMonter import JSONMonter
from utils.LogMessages import WELCOME_MSG
from utils.OnShowUtil import OnShowUtil
from utils.RelativePaths import relative_music_path
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
        self.SetBackgroundColour((0,0,0))
        self.SetForegroundColour((255,255,255))
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
        rootSizer.Add(self.newMapBackgroundHorizontalSizer(), 0, wx.CENTER)
        self.addToSizerWithSpaceAndLine(rootSizer, self.newMusicNameHorizontalSizer())
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
        self.dependenciesSetNameInput.Bind(wx.EVT_TEXT, self.onDepSetNameChanged)
        return self.dependenciesSetNameInput

    def onDepSetNameChanged(self,ev):
        self.current_dependencies[Consts.SET_NAME] = self.dependenciesSetNameInput.GetValue()

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
        dependenciesSubpanelsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        dependenciesSubpanelsVerticalSizer.Add(self.newResourcesSubpanel(), 0, wx.CENTER)
        dependenciesSubpanelsVerticalSizer.Add(self.newBuildingsSubpanel(), 0, wx.CENTER)
        dependenciesSubpanelsVerticalSizer.Add(self.newDwellersSubpanel(), 0, wx.CENTER)
        return dependenciesSubpanelsVerticalSizer

    def newDependenciesSubpanelsHorizontalSizer(self):
        dependenciesSubpanelsHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(dependenciesSubpanelsHorizontalSizer, self.newDependenciesSubPanelsVerticalSizer())
        dependenciesSubpanelsHorizontalSizer.Add(self.newLogAreaSizer())
        return dependenciesSubpanelsHorizontalSizer

    def newLogArea(self):
        # height of a logArea textctrl comes from the equation:
        #  h = dependencyPanel_height * dependenciesPanelsAmount + part_desc_label_height * dependenciesPanelsAmount
        self.logArea = wx.TextCtrl(parent = self, id=-1, size=(400, 90 * 3 + 10 * 3), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.logArea.SetLabelText(WELCOME_MSG)
        return self.logArea

    def newLogAreaSizer(self):
        self.logAreaVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.logAreaVerticalSizer.Add(self.newInfoST("Log area, shows important information"))
        self.logAreaVerticalSizer.Add(self.newLogArea())
        return self.logAreaVerticalSizer

    def newMapBackgroundHorizontalSizer(self):
        mapBackgroundHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(mapBackgroundHorizontalSizer, self.newBgTexturesVerticalSizer())
        mapBackgroundHorizontalSizer.Add(self.newMusicAndPanelTextureVerticalSizer())
        return mapBackgroundHorizontalSizer

    def newMusicNameHorizontalSizer(self):
        musicNameHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        musicNameHorizontalSizer.Add(wx.StaticText(self, label = "Selected .mp3 file: "))
        musicNameHorizontalSizer.AddSpacer(10)
        musicNameHorizontalSizer.Add(self.newMusicNameST())
        return musicNameHorizontalSizer

    def newMusicNameST(self):
        self.musicNameST = wx.StaticText(self, label = self.current_dependencies[Consts.MP3])
        return self.musicNameST

    def newMusicAndPanelTextureVerticalSizer(self):
        musicAndPanelVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.addToSizerWithSpace(musicAndPanelVerticalSizer,self.newMapPanelTextureHorizontalSizer())
        musicAndPanelVerticalSizer.Add(self.newMusicSelectorHorizontalSizer())
        return musicAndPanelVerticalSizer

    def newMusicSelectorHorizontalSizer(self):
        return self.newSelectorHorizontalSizer(
            self.newBitmap("nutka.jpg"),
            "The path of music in the Map:     ",
            self.onMusicSelected,
            "Choose another .mp3 file"
        )

    def newMapPanelTextureHorizontalSizer(self):
        return self.newSelectorHorizontalSizer(
            self.newMapPanelTexture(),
            "The texture of panels in the Map: ",
            self.onMapPanelTextureSelected
        )
    def newMapPanelTexture(self):
        self.mapPanelTexture = self.newBitmap(self.current_dependencies[Consts.PANEL_TEXTURE])
        return self.mapPanelTexture

    def onMusicSelected(self, ev):
        dlg = self.createFileSelectionDialog(
            dir=relative_music_path, msg="Choose an MP3 file", wildcard="*.mp3"
        )
        if dlg.ShowModal() == wx.ID_OK:
            self.current_dependencies[Consts.MP3] = dlg.GetFilename()
            self.musicNameST.SetLabelText(dlg.GetFilename())

    def onMapPanelTextureSelected(self, ev):
        dlg = self.createFileSelectionDialog()
        self.onImageSelected(dlg, self.mapPanelTexture)
        self.current_dependencies[Consts.PANEL_TEXTURE] = dlg.GetFilename()

    def newBgTexturesVerticalSizer(self):
        texturesVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.addToSizerWithSpace(texturesVerticalSizer, self.newBackgroundTextureOneHorizontalSizer())
        self.addToSizerWithSpace(texturesVerticalSizer, self.newBackgroundTextureTwoHorizontalSizer())
        return texturesVerticalSizer


    def newImageSelectorButton(self, onImgChangeCallback, btn_text):
        return ButtonsFactory().newButton(self, btn_text, onImgChangeCallback, size=(-1, 32), hint = LogMessages.BACKGROUND_TEXTURE_SELECTION_BTN_HINT)

    def newBitmap(self, textureName):
        image = wx.Image(name = relative_textures_path + textureName)#"..\\..\\resources\\Textures\\Grass.png"
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))

    def newSelectorHorizontalSizer(self, imageBitmap, info, onFileSelectedCallback, btn_text ="Choose another texture"):
        texture_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(texture_horizontal_sizer, self.newInfoST(info))
        self.addToSizerWithSpace(texture_horizontal_sizer, imageBitmap)
        texture_horizontal_sizer.Add(self.newImageSelectorButton(onFileSelectedCallback, btn_text))
        return texture_horizontal_sizer

    def newBackgroundBitmapOne(self):
        self.imageBitmapOne = self.newBitmap(self.current_dependencies[Consts.TEXTURE_ONE])
        return self.imageBitmapOne

    def newBackgroundTextureOneHorizontalSizer(self):
        return self.newSelectorHorizontalSizer(
            self.newBackgroundBitmapOne(),
            "Your background texture number one: ",
            self.onSelectImageOne
        )

    def newBackgroundBitmapTwo(self):
        self.imageBitmapTwo = self.newBitmap(self.current_dependencies[Consts.TEXTURE_TWO])
        return self.imageBitmapTwo

    def newBackgroundTextureTwoHorizontalSizer(self):
        return self.newSelectorHorizontalSizer(
            self.newBackgroundBitmapTwo(),
            "Your background texture number two: ",
            self.onSelectImageTwo
        )

    def newMenuButton(self):
        return ButtonsFactory().newButton(self, "Menu", self.retToMenu, hint = LogMessages.MENU_BTN_HINT)

    def newLoadButton(self):
        return ButtonsFactory().newButton(self, "Load dependencies From File", self.loadDependencies, hint = LogMessages.LOAD_DEPS_BTN_HINT)

    def newSaveButton(self):
        return ButtonsFactory().newButton(self, "Save these dependencies to File", self.save, hint = LogMessages.SAVE_DEPS_BTN_HINT)

    def newCreateButton(self):
        return ButtonsFactory().newButton(self, "Create", self.createDependencies, hint = LogMessages.CREATE_DEPS_BTN_HINT)

    def newCleanButton(self):
        return ButtonsFactory().newButton(self, "Clean and Start Again", self.clean, hint = LogMessages.CLEAN_DEPS_BTN_HINT)

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

    def createFileSelectionDialog(self, dir = relative_textures_path, msg ="Choose an image", wildcard ="*.png|*.jpg"):
        return wx.FileDialog(
            self,
            defaultDir=dir, #"..\\..\\resources\\Textures\\",
            message=msg,
            wildcard = wildcard,
            style=wx.FD_OPEN
        )

    def  onImageSelected(self, dlg, imageBitmap):
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            image = wx.Image(path)
            image = image.Scale(32,32)
            imageBitmap.SetBitmap(wx.BitmapFromImage(image))

    def onSelectImageOne(self, event):
        dlg = self.createFileSelectionDialog()
        self.onImageSelected(dlg, self.imageBitmapOne)
        self.current_dependencies[Consts.TEXTURE_ONE] = dlg.GetFilename()

    def onSelectImageTwo(self, event):
        dlg = self.createFileSelectionDialog()
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
                self.logArea.SetValue("Dependencies successfully saved")

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


    def createScaledBitmap(self, bmp, img_path):
        image = wx.Image(img_path)
        image = image.Scale(32,32)
        bmp.SetBitmap(wx.BitmapFromImage(image))

    def refreshSubPanels(self):
        for subpanel in self.subpanels: subpanel.resetContents()

    def updateTextureOne(self, file = None):
        file = self.current_dependencies[Consts.TEXTURE_ONE] if file is None else file
        self.createScaledBitmap(self.imageBitmapOne, relative_textures_path + file)

    def updateTextureTwo(self, file = None):
        file = self.current_dependencies[Consts.TEXTURE_TWO] if file is None else file
        self.createScaledBitmap(self.imageBitmapTwo, relative_textures_path + file)

    def updateMapPanelTexture(self, file=None):
        file = self.current_dependencies[Consts.PANEL_TEXTURE] if file is None else file
        self.createScaledBitmap(self.mapPanelTexture, relative_textures_path + file)

    def restoreDefaultCurrentDepsValues(self):
        self.cleanCurrentDependencies()
        self.current_dependencies[Consts.MP3] = CreatorConfig.MP3_DEFAULT_NAME
        self.current_dependencies[Consts.SET_NAME] = CreatorConfig.DEPENDENCIES_DEFAULT_SET_NAME
        self.current_dependencies[Consts.TEXTURE_ONE] = CreatorConfig.TEXTURE_ONE_DEFAULT_NAME
        self.current_dependencies[Consts.TEXTURE_TWO] = CreatorConfig.TEXTURE_TWO_DEFAULT_NAME
        self.current_dependencies[Consts.PANEL_TEXTURE] = CreatorConfig.PANEL_TEXURE_DEFAULT_NAME
        self.graphsSpaces.resetViewFromJSON(
            {
                Consts.DWELLERS:[],
                Consts.BUILDINGS:[],
                Consts.RESOURCES:[]
            }
        )

    def clean(self, event):
        self.restoreDefaultCurrentDepsValues()
        self.resetContents("Restored default settings")

    def resetContents(self, logMsg = None):
        self.dependenciesSetNameInput.SetValue(self.current_dependencies[Consts.SET_NAME])
        self.updateTextureOne()
        self.updateTextureTwo()
        self.updateMapPanelTexture()
        self.refreshSubPanels()
        if logMsg is not None: self.logArea.SetValue(logMsg)

    def getCurrentBuildingsNames(self):
        return self.current_dependencies[Consts.BUILDINGS].keys()

    def getCurrentResourcesNames(self):
        return self.current_dependencies[Consts.RESOURCES].keys()

    def getCurrentDwellersNames(self):
        return self.current_dependencies[Consts.DWELLERS].keys()


    def fillCurrentDependenciesWithValidContent(self, content_dict):
        validKeys = self.parent.newCurrentDependenciesKeys()
        contentKeys = content_dict.keys()
        for key in validKeys:
            if key not in contentKeys: raise Exception
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

    def fileExists(self, path, dir = relative_textures_path):
        return os.path.isfile(dir + path)

    def currentDependenciesCorrect(self, updateNameFromInput):
        input_correct = self.depsNotEmpty()
        input_correct &= self.dependenciesSetNameTypedCorrectly(updateNameFromInput=updateNameFromInput)
        input_correct &= self.fileExists(self.current_dependencies[Consts.TEXTURE_ONE])
        input_correct &= self.fileExists(self.current_dependencies[Consts.TEXTURE_TWO])
        input_correct &= self.fileExists(self.current_dependencies[Consts.MP3], relative_music_path)
        input_correct &= self.fileExists(self.current_dependencies[Consts.PANEL_TEXTURE])
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

    def depsNotEmpty(self):
        res = True
        if self.current_dependencies[Consts.DWELLERS].__len__() == 0:
            self.logArea.SetLabelText("->Dwellers list empty, please fill it\n")
            res = False
        if self.current_dependencies[Consts.BUILDINGS].__len__() == 0:
            self.logArea.AppendText("->Buildings list empty, please fill it\n")
            res = False
        if  self.current_dependencies[Consts.RESOURCES].__len__() == 0:
            self.logArea.AppendText("-> Resources list empty, please fill it\n")
            res = False
        return res


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
            Consts.MP3: self.current_dependencies[Consts.MP3],
            Consts.PANEL_TEXTURE: self.current_dependencies[Consts.PANEL_TEXTURE],
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