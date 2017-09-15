import wx

from wx.lib.scrolledpanel import ScrolledPanel

from CreatorView import Consts
from CreatorView.SheetBasicViewsFactory import SheetBasicViewsFactory
from RelativePaths import relative_textures_path

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
        self.initSheetSubViews()
        self.initRootSizer()

    def initSheetSubViews(self):
        self.NameInput = None
        self.descriptionArea = None
        self.imageBitmap = None
        self.predecessorSelector = None
        self.successorSelector = None
        self.log_area = None

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddSpacer(75)
        rootSizer.Add(
            SheetBasicViewsFactory(self)
                .newEntityNameHorizontalSizer(Consts.RESOURCE), 0, wx.CENTER
        )
        rootSizer.AddSpacer(10)
        rootSizer.Add(
            SheetBasicViewsFactory(self).newLine(), 0, wx.EXPAND
        )
        rootSizer.AddSpacer(10)
        rootSizer.Add(
            SheetBasicViewsFactory(self)
                .newMainSheetPartHorizontalSizer(
                self.newResourceCharacteristicsVerticalSizer()
            ), 0, wx.CENTER
        )
        rootSizer.Add(SheetBasicViewsFactory(self).newLine(), 0, wx.EXPAND)
        rootSizer.AddSpacer(10)
        rootSizer.Add(
            SheetBasicViewsFactory(self)
                .newButtonsPanelHorizontalSizer(
                self.submit, self.moveToMainPanel
            ), 0, wx.CENTER, 5
        )
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])

    def newResourceCharacteristicsVerticalSizer(self):
        resourceCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        resourceCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self)
                .newDescriptionAreaVerticalSizer(Consts.RESOURCE), 0, wx.CENTER
        )
        resourceCharacteristicsVerticalSizer.AddSpacer(10)
        resourceCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self)
                .newPredecessorPickerHorizontalSizer(Consts.RESOURCE), 0, wx.CENTER
        )
        resourceCharacteristicsVerticalSizer.AddSpacer(5)
        resourceCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self)
                .newSuccesorPickerHorizontalSizer(Consts.RESOURCE), 0, wx.CENTER
        )
        resourceCharacteristicsVerticalSizer.AddSpacer(10)
        resourceCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self)
                .newEntityIconHorizontalSizer(self.selectImage), 0, wx.CENTER
        )
        resourceCharacteristicsVerticalSizer.AddSpacer(10)
        resourceCharacteristicsVerticalSizer.Add(
            self.newStartIncomePickerHorizontalSizer(), 0, wx.CENTER
        )
        resourceCharacteristicsVerticalSizer.AddSpacer(10)
        return resourceCharacteristicsVerticalSizer

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
        self.imageBitmap.SetBitmap(
            wx.BitmapFromImage(
                SheetBasicViewsFactory(self)
                    .newScaledImg(relative_textures_path + self.entityIconRelativePath)
            )
        )
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
            self.imageBitmap.SetBitmap(wx.BitmapFromImage(SheetBasicViewsFactory(self).newScaledImg(path)))

    def moveToMainPanel(self,event):
        self.frame.showPanel("main_panel",initDataForSearchedPanel=None)
