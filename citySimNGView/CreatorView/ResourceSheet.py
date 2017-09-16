import wx

from wx.lib.scrolledpanel import ScrolledPanel

from CreatorView import Consts
from CreatorView.RestorableView import RestorableStartIncomePicker
from CreatorView.SheetBasicViewsUtils import SheetBasicViewsUtils

from utils.OnShowUtil import OnShowUtil
from viewmodel.SheetEntityChecker import AddModeSheetEntityChecker, EditModeSheetEntityChecker, ResourceSheetChecker


class ResourceSheet(ScrolledPanel):
    def __init__(self,parent, size, frame, currentDependencies):
        ScrolledPanel.__init__(self, size = size, parent = parent, style = wx.SIMPLE_BORDER)
        self.SetupScrolling()
        self.size= size
        self.frame = frame
        self.currentDependencies = currentDependencies
        self.wakeUpData = None
        self.entityIconRelativePath = self.getDefaultIconRelativePath()
        self.sheet_name =  "Resources"
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.restorableViews = []
        self.sheetChecker = AddModeSheetEntityChecker(self)
        SheetBasicViewsUtils(self).initRootSizer(self.newResourceCharacteristicsVerticalSizer(), topPadding=75)


    def addViewToCharacteristicsSizerWithSpace(self, view, space= 0, alignment = wx.CENTER):
        self.resourceCharacteristicsVerticalSizer.Add(view, 0, alignment)
        self.resourceCharacteristicsVerticalSizer.AddSpacer(space)

    def newResourceCharacteristicsVerticalSizer(self):
        self.resourceCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.addViewToCharacteristicsSizerWithSpace(SheetBasicViewsUtils(self).newDescriptionAreaVerticalSizer(Consts.RESOURCE), space = 10)
        self.addViewToCharacteristicsSizerWithSpace(SheetBasicViewsUtils(self).newPredecessorPickerHorizontalSizer(Consts.RESOURCE), space = 5)
        self.addViewToCharacteristicsSizerWithSpace(SheetBasicViewsUtils(self).newSuccesorPickerHorizontalSizer(Consts.RESOURCE), space = 10)
        self.addViewToCharacteristicsSizerWithSpace(SheetBasicViewsUtils(self).newEntityIconHorizontalSizer(), space=10)
        self.addViewToCharacteristicsSizerWithSpace(self.newStartIncomePickerHorizontalSizer(), space = 10)
        return self.resourceCharacteristicsVerticalSizer

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
        self.restorableViews.append(RestorableStartIncomePicker(self, self.start_income_picker))
        return self.start_income_picker

    def getDefaultIconRelativePath(self):
        return "DefaultBuilding.jpg"

    def getEntityType(self):
        return Consts.RESOURCE

    def getEntityNameKey(self):
        return Consts.RESOURCE_NAME

    def setUpEditMode(self, edit_element_name):
        SheetBasicViewsUtils(self).setupMode( EditModeSheetEntityChecker(self), edit_element_name)

    def setUpAddMode(self):
        SheetBasicViewsUtils(self).setupMode( AddModeSheetEntityChecker(self))

    def onShow(self, event):
        OnShowUtil().onCreatorSheetShow(self, event)

    def submit(self, event):
        self.sheetChecker.onCheck(ResourceSheetChecker())
