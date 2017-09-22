from wx import wx
from wx.lib.scrolledpanel import ScrolledPanel

from CreatorView import Consts
from CreatorView.NumberFillingChecker import NumberFillingChecker
from CreatorView.RestorableView import RestorableNameInput, RestorableDescriptionArea, RestorableImageBmp, RestorableLogArea, RestorableStdSelector
from utils.ButtonsFactory import ButtonsFactory
from utils.OnShowUtil import OnShowUtil
from utils.RelativePaths import relative_textures_path
from viewmodel.SheetEntityChecker import AddModeSheetEntityChecker, EDIT_MODE, EditModeSheetEntityChecker


class SheetView(ScrolledPanel):

    def __init__(self,parent, size, frame, currentDependencies):
        ScrolledPanel.__init__(self, size = size, parent = parent, style = wx.SIMPLE_BORDER)
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.SetupScrolling()
        self.size = size
        self.frame = frame
        self.currentDependencies = currentDependencies
        self.wakeUpData = None
        self.restorableViews = []
        self.childrenCheckers = []
        self.entityIconRelativePath = self.getDefaultIconRelativePath()
        self.sheetChecker = AddModeSheetEntityChecker(self)
        self.sheet_name = self.getSheetName()

    def onShow(self, event):
        OnShowUtil().onCreatorSheetShow(self, event)

    def getSheetName(self):
        raise Exception("getSheetName not implemented")

    def getDefaultIconRelativePath(self):
        raise Exception("getDefaultIconRealtivePath not implemented")

    def getEntityType(self):
        raise Exception("getEntityType not implemented")

    def getEntityNameKey(self):
        raise Exception("getEntityNameKey not implemented")

    def submit(self, event):
        raise Exception("submit not implemented")

    def getEntityChecker(self):
        raise Exception("getEntityChecker not implemented")

    def addToSizerWithSpace(self, sizer, view, space = 10, alignment = wx.CENTER):
        sizer.Add(view, 0, alignment)
        sizer.AddSpacer(space)

    def newBasicCharacteristicsVerticalSizer(self):
        basicCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.addToSizerWithSpace(basicCharacteristicsVerticalSizer, self.newDescriptionAreaVerticalSizer())
        self.addToSizerWithSpace(basicCharacteristicsVerticalSizer, self.newPredecessorPickerHorizontalSizer(), space = 5)
        self.addToSizerWithSpace(basicCharacteristicsVerticalSizer, self.newSuccesorPickerHorizontalSizer())
        self.addToSizerWithSpace(basicCharacteristicsVerticalSizer, self.newEntityIconHorizontalSizer())
        return basicCharacteristicsVerticalSizer

    def newRootSizer(self, characteristicVerticalSizer, topPadding):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddSpacer(topPadding)
        self.addToSizerWithSpace(rootSizer, self.newEntityNameHorizontalSizer(self.getEntityType()))
        self.addToSizerWithSpace(rootSizer, self.newLine(), space= 10, alignment=wx.EXPAND)
        self.addToSizerWithSpace(rootSizer, self.newMainSheetPartHorizontalSizer(characteristicVerticalSizer))
        self.addToSizerWithSpace(rootSizer, self.newLine(), space=10, alignment=wx.EXPAND)
        self.addToSizerWithSpace(rootSizer, self.newButtonsPanelHorizontalSizer(self.submit), space = 75)
        return rootSizer

    def initRootSizer(self, characteristicVerticalSizer, topPadding = 10):
        rootSizer = self.newRootSizer(characteristicVerticalSizer, topPadding)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])

    def newEntityNameHorizontalSizer(self, defaultName= None):
        entityNameHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(entityNameHorizontalSizer,self.newNameFieldLabel(self.getEntityType()))
        entityNameHorizontalSizer.Add(self.newNameInput(defaultName if defaultName is not None else self.getEntityType()))
        return entityNameHorizontalSizer

    def newNameFieldLabel(self, entity_type):
         return wx.StaticText(self,-1, "Name of this " + entity_type)

    def newNameInput(self, defaultName):
        self.NameInput = wx.TextCtrl(self, -1, defaultName)
        self.restorableViews.append(RestorableNameInput(self, self.NameInput))
        return self.NameInput

    def newLine(self, style = wx.HORIZONTAL):
        return wx.StaticLine(self, -1, style = style)

    def newMainSheetPartHorizontalSizer(self, entityCharacteristicsVerticalSizer):
        mainSheetPartHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(mainSheetPartHorizontalSizer, entityCharacteristicsVerticalSizer, space=50, alignment=wx.LEFT)
        self.addToSizerWithSpace(mainSheetPartHorizontalSizer,self.newLine(wx.VERTICAL), space = 50, alignment=wx.EXPAND)
        mainSheetPartHorizontalSizer.Add(self.newLogAreaVerticalSizer(),0,wx.RIGHT)
        return mainSheetPartHorizontalSizer

    def newLogAreaVerticalSizer(self):
        log_area_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        log_area_vertical_sizer.Add(self.newLogAreaLabel(),0,wx.CENTER)
        self.addToSizerWithSpace(log_area_vertical_sizer, self.newLogArea(), space=50)
        return log_area_vertical_sizer

    def newLogAreaLabel(self):
        return wx.StaticText(self,-1,"Below lies logging area, showing error msgs")

    def newLogArea(self):
        self.log_area = wx.TextCtrl(self, -1, size = (500,350), style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.restorableViews.append(RestorableLogArea(self, self.log_area))
        return self.log_area

    def newButtonsPanelHorizontalSizer(self, onSubmit):
        buttons_panel_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_panel_horizontal_sizer.Add(self.newCreateEntityButton(onSubmit))
        buttons_panel_horizontal_sizer.Add(self.newCancelButton(self.moveToMainPanel))
        return buttons_panel_horizontal_sizer

    def newCreateEntityButton(self, onSubmit):
        return ButtonsFactory().newButton(self, "Submit", onSubmit)

    def newCancelButton(self, onCancel):
        return ButtonsFactory().newButton(self, "Cancel", onCancel)

    def newDescriptionAreaVerticalSizer(self):
        descriptionAreaVerticalSizer =  wx.BoxSizer(wx.VERTICAL)
        descriptionAreaVerticalSizer.Add(self.newDescriptionFieldLabel(self.getEntityType()), 0, wx.CENTER)
        descriptionAreaVerticalSizer.Add(self.newDescriptionArea(), 0, wx.CENTER)
        return descriptionAreaVerticalSizer

    def newDescriptionFieldLabel(self, entity_type):
        return wx.StaticText(self, -1, "Description of " + entity_type + "for Tutorial module")

    def newDescriptionArea(self):
        self.descriptionArea = wx.TextCtrl(self, -1,size=(400, 200), style=wx.TE_MULTILINE)
        self.restorableViews.append(RestorableDescriptionArea(self, self.descriptionArea))
        return self.descriptionArea

    def newPredecessorPickerHorizontalSizer(self,):
        predecessor_picker_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(predecessor_picker_horizontal_sizer, self.newPredeccesorLabel(self.getEntityType()))
        predecessor_picker_horizontal_sizer.Add(self.newPredecessorSelector())
        return predecessor_picker_horizontal_sizer

    def newSelector(self):
        return wx.ComboBox(self, choices=["None"], size = (125,-1), style=wx.CB_READONLY)

    def newPredecessorSelector(self):
        self.predecessorSelector = self.newSelector()
        self.restorableViews.append(
            RestorableStdSelector(self, self.predecessorSelector, Consts.PREDECESSOR)
        )
        return self.predecessorSelector

    def newSuccesorPickerHorizontalSizer(self):
        successor_picker_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(successor_picker_horizontal_sizer, self.newSuccesorLabel(self.getEntityType()))
        successor_picker_horizontal_sizer.Add(self.newSuccessorSelector())
        return successor_picker_horizontal_sizer

    def newSuccessorSelector(self):
        self.successorSelector = self.newSelector()
        self.restorableViews.append(
            RestorableStdSelector(self, self.successorSelector, Consts.SUCCESSOR)
        )
        return self.successorSelector

    def newPredeccesorLabel(self, entity_type):
        return wx.StaticText(self, -1, "Predecessor " + entity_type +":", size = (150, -1))

    def newSuccesorLabel(self,entity_type):
        return wx.StaticText(self, -1, "Successor " + entity_type + ":", size = (125,-1))

    def newEntityIconHorizontalSizer(self):
        entityIconHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(entityIconHorizontalSizer, self.newImageInfoLabel())
        self.addToSizerWithSpace(entityIconHorizontalSizer,self.newEntityBmp())
        entityIconHorizontalSizer.Add(self.newImageSelectorButton())
        return entityIconHorizontalSizer

    def newImageInfoLabel(self):
        return wx.StaticText(self, -1, "Your texture: ")

    def newEntityBmp(self):
        self.imageBitmap = self.newScaledImgBitmap(relative_textures_path + "DefaultBuilding.jpg")
        self.restorableViews.append(RestorableImageBmp(self, self.imageBitmap))
        return self.imageBitmap

    def newScaledImg(self, non_relative_path):
        image = wx.Image(name = non_relative_path) #"..\\..\\resources\\Textures\\DefaultBuilding.jpg"
        return image.Scale(32,32)

    def newScaledImgBitmap(self, non_relative_path):
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(self.newScaledImg(non_relative_path)), size = (32,32))

    def newImageSelectorButton(self):
        return ButtonsFactory().newButton(self, "Choose another texture", self.selectImage, size = (-1, 32))

    def selectImage(self, event):
        dlg = self.newImgDialog()
        self.onImageSelected(dlg)

    def newImgDialog(self):
        return wx.FileDialog(
            self,
            defaultDir= relative_textures_path, #"..\\..\\resources\\Textures\\",
            message="Choose an image",
            wildcard="*.png|*.jpg",
            style=wx.FD_OPEN
        )

    def onImageSelected(self, dlg):
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.entityIconRelativePath = dlg.GetFilename()
            self.imageBitmap.SetBitmap(wx.BitmapFromImage(self.newScaledImg(path)))

    def moveToMainPanel(self,event):
        self.frame.showPanel("main_panel",initDataForSearchedPanel=None)

    def restoreRestorables(self, edit_element_name):
        for restorableView in self.restorableViews:
            restorableView.restoreView(edit_element_name)

    def restoreChildrenCheckers(self, sheetMode, edit_element_name):
        for child in self.childrenCheckers:
            child.fillWithEntries(edit_element_name if sheetMode.getMode() == EDIT_MODE else None)

    def setupSheetMode(self, sheetMode, edit_element_name = None):
        self.sheetChecker = sheetMode
        self.restoreRestorables(edit_element_name)
        self.restoreChildrenCheckers(sheetMode, edit_element_name)

    def setUpEditMode(self, edit_element_name):
        self.setupSheetMode(EditModeSheetEntityChecker(self), edit_element_name)

    def setUpAddMode(self):
        self.setupSheetMode(AddModeSheetEntityChecker(self))

    def newNumberFillingChecker(self, value_desc_label_txt, intro_label_txt, json_key):
        numberFillingChecker =  NumberFillingChecker(
            self,
            key_label_txt="Resource:",
            value_desc_label_txt=value_desc_label_txt,
            intro_label_txt=intro_label_txt,
            json_key=json_key
        )
        self.childrenCheckers.append(numberFillingChecker)
        return numberFillingChecker

    def newResourcesConsumedChecker(self):
        return self.newNumberFillingChecker(
            "Consumed in quantity:",
            "Consumed resources",
            Consts.CONSUMES
        )