import wx

from CreatorView import Consts
from CreatorView.RestorableView import RestorableStartIncomePicker
from CreatorView.SheetView import SheetView

from utils.OnShowUtil import OnShowUtil
from viewmodel.SheetEntityChecker import ResourceSheetChecker


class ResourceSheet(SheetView):
    def __init__(self, parent, size, frame, currentDependencies):
        super(ResourceSheet, self).__init__(parent, size, frame, currentDependencies)
        self.initRootSizer(self.newResourceCharacteristicsVerticalSizer(), topPadding=75)

    def getDefaultIconRelativePath(self):
        return "DefaultBuilding.jpg"

    def getEntityType(self):
        return Consts.RESOURCE

    def getEntityNameKey(self):
        return Consts.RESOURCE_NAME

    def onShow(self, event):
        OnShowUtil().onCreatorSheetShow(self, event)

    def submit(self, event):
        self.sheetChecker.onCheck(ResourceSheetChecker())

    def getEntityChecker(self):
        return ResourceSheetChecker()

    def getValidKeySet(self):
        return [Consts.PREDECESSOR, Consts.SUCCESSOR, Consts.DESCRIPTION, Consts.TEXTURE_PATH, Consts.START_INCOME, Consts.RESOURCE_NAME]

    def getSheetName(self):
        return Consts.RESOURCES

    def newResourceCharacteristicsVerticalSizer(self):
        resourceCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        resourceCharacteristicsVerticalSizer.Add(self.newBasicCharacteristicsVerticalSizer(), 0, wx.CENTER)
        self.addToSizerWithSpace(resourceCharacteristicsVerticalSizer,self.newStartIncomePickerHorizontalSizer())
        return resourceCharacteristicsVerticalSizer

    def newStartIncomePickerHorizontalSizer(self):
        startIncomePickerHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(startIncomePickerHorizontalSizer,self.newStartIncomeLabel())
        startIncomePickerHorizontalSizer.Add(self.newStartIncomePicker())
        return startIncomePickerHorizontalSizer

    def newStartIncomeLabel(self):
        return wx.StaticText(self, -1, "StartIncome: ")

    def newStartIncomePicker(self):
        self.start_income_picker =  wx.SpinCtrl(self, value='0', size=(60, -1), min=-1, max = 5000)
        self.start_income_picker.SetForegroundColour((0,0,0))
        self.restorableViews.append(RestorableStartIncomePicker(self, self.start_income_picker))
        return self.start_income_picker
