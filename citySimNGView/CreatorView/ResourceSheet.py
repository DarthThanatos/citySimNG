import wx

from wx.lib.scrolledpanel import ScrolledPanel

from CreatorView import Consts
from RelativePaths import relative_textures_path

from utils.ButtonsFactory import ButtonsFactory
from utils.OnShowUtil import OnShowUtil
from viewmodel.SheetEntityChecker import AddModeSheetEntityChecker, EditModeSheetEntityChecker, ADD_MODE


class ResourceSheet(ScrolledPanel):
    def __init__(self,parent, size, frame, currentDependencies):
        ScrolledPanel.__init__(self, size = size, parent = parent, style = wx.SIMPLE_BORDER)
        self.SetupScrolling()
        self.size= size
        self.frame = frame
        self.currentDependencies = currentDependencies
        self.wakeUpData = None
        self.entityIconRelativePath = "DefaultBuilding.jpg"
        self.sheet_name =  "Resources"
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.sheetChecker = AddModeSheetEntityChecker(self)
        self.initRootSizer()

    def newLine(self, style = wx.HORIZONTAL):
        return wx.StaticLine(self, -1, style = style)

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddSpacer(75)
        rootSizer.Add(self.newEntityNameHorizontalSizer(), 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        rootSizer.Add(self.newLine(), 0, wx.EXPAND)
        rootSizer.AddSpacer(10)
        rootSizer.Add(self.newMainSheetPartHorizontalSizer(), 0, wx.CENTER)
        rootSizer.Add(self.newLine(), 0, wx.EXPAND)
        rootSizer.AddSpacer(10)
        rootSizer.Add(self.newButtonsPanelHorizontalSizer(), 0, wx.CENTER, 5)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])

    def newEntityNameHorizontalSizer(self):
        entityNameHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.NameInput = wx.TextCtrl(self, -1, "Resource")
        entityNameHorizontalSizer.Add(self.newNameFieldLabel())
        entityNameHorizontalSizer.AddSpacer(5)
        entityNameHorizontalSizer.Add(self.NameInput)
        return entityNameHorizontalSizer

    def newNameFieldLabel(self):
         return wx.StaticText(self,-1, "Name of this resource")

    def newMainSheetPartHorizontalSizer(self):
        mainSheetPartHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSheetPartHorizontalSizer.Add(self.newEntityCharacteristicsVerticalSizer(),0, wx.LEFT)
        mainSheetPartHorizontalSizer.AddSpacer(50)
        mainSheetPartHorizontalSizer.Add(self.newLine(wx.VERTICAL), 0, wx.EXPAND)
        mainSheetPartHorizontalSizer.AddSpacer(50)
        mainSheetPartHorizontalSizer.Add(self.newLogAreaVerticalSizer(),0,wx.RIGHT)
        return mainSheetPartHorizontalSizer

    def newButtonsPanelHorizontalSizer(self):
        buttons_panel_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_panel_horizontal_sizer.Add(self.newCreateEntityButton())
        buttons_panel_horizontal_sizer.Add(self.newCancelButton())
        return buttons_panel_horizontal_sizer

    def newCreateEntityButton(self):
        return ButtonsFactory().newButton(self, "Submit", self.submit)

    def newCancelButton(self):
        return ButtonsFactory().newButton(self, "Cancel", self.moveToMainPanel)

    def newEntityCharacteristicsVerticalSizer(self):
        entityCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        entityCharacteristicsVerticalSizer.Add(self.newDescriptionFieldLabel(), 0, wx.CENTER)
        entityCharacteristicsVerticalSizer.Add(self.newDescriptionArea(), 0, wx.CENTER)
        entityCharacteristicsVerticalSizer.AddSpacer(10)
        entityCharacteristicsVerticalSizer.Add(self.newPredecessorPickerHorizontalSizer(), 0, wx.CENTER)
        entityCharacteristicsVerticalSizer.AddSpacer(5)
        entityCharacteristicsVerticalSizer.Add(self.newSuccesorPickerHorizontalSizer(), 0, wx.CENTER)
        entityCharacteristicsVerticalSizer.AddSpacer(10)
        entityCharacteristicsVerticalSizer.Add(self.newEntityIconHorizontalSizer(), 0, wx.CENTER)
        entityCharacteristicsVerticalSizer.AddSpacer(10)
        entityCharacteristicsVerticalSizer.Add(self.newStartIncomePickerHorizontalSizer(), 0, wx.CENTER)
        entityCharacteristicsVerticalSizer.AddSpacer(10)
        return entityCharacteristicsVerticalSizer

    def newDescriptionFieldLabel(self):
        return wx.StaticText(self, -1, "Description of Resource for Tutorial module")

    def newDescriptionArea(self):
        self.descriptionArea = wx.TextCtrl(self, -1,size=(400, 200), style=wx.TE_MULTILINE)
        return self.descriptionArea

    def newPredecessorPickerHorizontalSizer(self):
        predecessor_picker_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        predecessor_picker_horizontal_sizer.Add(self.newPredeccesorLabel())
        predecessor_picker_horizontal_sizer.AddSpacer(10)
        predecessor_picker_horizontal_sizer.Add(self.newPredecessorSelector())
        return predecessor_picker_horizontal_sizer

    def newSelector(self):
        return wx.ComboBox(self, choices=["None"], size = (125,-1), style=wx.CB_READONLY)

    def newPredecessorSelector(self):
        self.predecessorSelector = self.newSelector()
        return self.predecessorSelector

    def newSuccesorPickerHorizontalSizer(self):
        successor_picker_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        successor_picker_horizontal_sizer.Add(self.newSuccesorLabel())
        successor_picker_horizontal_sizer.AddSpacer(10)
        successor_picker_horizontal_sizer.Add(self.newSuccessorSelector())
        return successor_picker_horizontal_sizer

    def newSuccessorSelector(self):
        self.successorSelector = self.newSelector()
        return self.successorSelector

    def newEntityIconHorizontalSizer(self):
        entityIconHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        entityIconHorizontalSizer.Add(self.newImageInfoLabel())
        entityIconHorizontalSizer.AddSpacer(10)
        entityIconHorizontalSizer.Add(self.newEntityBmp())
        entityIconHorizontalSizer.AddSpacer(10)
        entityIconHorizontalSizer.Add(self.newImageSelectorButton())
        return entityIconHorizontalSizer

    def newEntityBmp(self):
        self.imageBitmap = self.newScaledImgBitmap(relative_textures_path + "DefaultBuilding.jpg")
        return self.imageBitmap

    def newScaledImg(self, non_relative_path):
        image = wx.Image(name = non_relative_path) #"..\\..\\resources\\Textures\\DefaultBuilding.jpg"
        return image.Scale(32,32)

    def newScaledImgBitmap(self, non_relative_path):
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(self.newScaledImg(non_relative_path)), size = (32,32))

    def newImageInfoLabel(self):
        return wx.StaticText(self, -1, "Your texture: ")

    def newImageSelectorButton(self):
        return ButtonsFactory().newButton(self, "Choose another texture", self.selectImage, size = (-1, 32))

    def newStartIncomePickerHorizontalSizer(self):
        startIncomePickerHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        startIncomePickerHorizontalSizer.Add(self.newStartIncomeLabel())
        startIncomePickerHorizontalSizer.AddSpacer(10)
        startIncomePickerHorizontalSizer.Add(self.newStartIncomePicker())
        return startIncomePickerHorizontalSizer

    def newStartIncomeLabel(self):
        return wx.StaticText(self, -1, "StartIncome: ")

    def newStartIncomePicker(self):
        self.start_income_picker =  wx.SpinCtrl(self, value='0', size=(60, -1), min=0, max = 5000)
        return self.start_income_picker

    def newPredeccesorLabel(self):
        return wx.StaticText(self, -1, "Predecessor resource:", size = (150, -1))

    def newSuccesorLabel(self):
        return wx.StaticText(self, -1, "Successor resource:", size = (125,-1))

    def newLogAreaVerticalSizer(self):
        log_area_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        log_area_vertical_sizer.Add(self.newLogAreaLabel(),0,wx.CENTER)
        log_area_vertical_sizer.Add(self.newLogArea(), 0, wx.CENTER)
        log_area_vertical_sizer.AddSpacer(50)
        return log_area_vertical_sizer

    def newLogAreaLabel(self):
        return wx.StaticText(self,-1,"Below lies logging area, showing error msgs")

    def newLogArea(self):
        self.log_area = wx.TextCtrl(self, -1, size = (500,350), style=wx.TE_MULTILINE | wx.TE_READONLY)
        return self.log_area

    def reinitNameInput(self, input, enabled):
        self.NameInput.SetValue(input)
        self.NameInput.Enable(enabled)


    def getSheetEntitiesNames(self):
        return self.currentDependencies[self.sheet_name].keys()

    def getEntityCharacteristicFromEntitiesSet(self, edit_element_name, characteristic):
        characteristic = self.getEntityCharacteristic(edit_element_name, characteristic)
        return characteristic if characteristic in self.getSheetEntitiesNames() else "None"

    def clearSelector(self, selector, stringSelection = "None"):
        selector.Clear()
        for entityName in self.currentDependencies[self.sheet_name].keys() + ["None"]:
            selector.Append(entityName)
        selector.SetStringSelection(stringSelection)

    def resetSheetValues(
         self,
         sheetMode,
         entityNameInput ="Resource",
         descriptionAreaValue = "",
         startIncomePickerValue = 0,
         entityIconRelativePath = "DefaultBuilding.jpg",
         predecessorStringSelection = "None",
         successorStringSelection = "None"
    ):
        self.sheetChecker = sheetMode
        self.reinitNameInput(entityNameInput, enabled = sheetMode.getMode() == ADD_MODE)
        self.descriptionArea.SetValue(descriptionAreaValue)
        self.start_income_picker.SetValue(startIncomePickerValue)
        self.entityIconRelativePath = entityIconRelativePath
        self.imageBitmap.SetBitmap(wx.BitmapFromImage(self.newScaledImg(relative_textures_path + self.entityIconRelativePath)))
        self.clearSelector(self.predecessorSelector, predecessorStringSelection)
        self.clearSelector(self.successorSelector, successorStringSelection)
        self.log_area.SetValue("")

    def setUpAddMode(self):
        self.resetSheetValues(sheetMode= AddModeSheetEntityChecker(self))

    def setUpEditMode(self, edit_element_name):
        self.resetSheetValues(
            sheetMode= EditModeSheetEntityChecker(self),
            entityNameInput= edit_element_name,
            descriptionAreaValue=self.getEntityCharacteristic(edit_element_name, Consts.DESCRIPTION),
            startIncomePickerValue=int(self.getEntityCharacteristic(edit_element_name, Consts.START_INCOME)),
            entityIconRelativePath=self.getEntityCharacteristic(edit_element_name, Consts.TEXTURE_PATH),
            predecessorStringSelection=self.getEntityCharacteristicFromEntitiesSet(edit_element_name, Consts.PREDECESSOR),
            successorStringSelection=self.getEntityCharacteristicFromEntitiesSet(edit_element_name, Consts.SUCCESSOR)
        )

    def getEntityCharacteristic(self, edit_element_name, characteristic):
        return self.currentDependencies[self.sheet_name][edit_element_name][characteristic]

    def onShow(self, event):
        OnShowUtil().onCreatorSheetShow(self, event)

    def submit(self, event):
        self.sheetChecker.onCheck()

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
