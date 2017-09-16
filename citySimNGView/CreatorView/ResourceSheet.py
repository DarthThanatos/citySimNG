import wx

from wx.lib.scrolledpanel import ScrolledPanel

from CreatorView import Consts
from CreatorView.SheetBasicViewsUtils import SheetBasicViewsUtils

from utils.OnShowUtil import OnShowUtil
from viewmodel.SheetEntityChecker import AddModeSheetEntityChecker, EditModeSheetEntityChecker, ADD_MODE, \
    ResourceSheetChecker


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
        self.initSheetSubViews()
        self.sheetChecker = AddModeSheetEntityChecker(self)
        self.initRootSizer()

    def getEntityType(self):
        return Consts.RESOURCE

    def getEntityNameKey(self):
        return Consts.RESOURCE_NAME

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddSpacer(75)
        rootSizer.Add(SheetBasicViewsUtils(self).newEntityNameHorizontalSizer(Consts.RESOURCE), 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        rootSizer.Add(SheetBasicViewsUtils(self).newLine(), 0, wx.EXPAND)
        rootSizer.AddSpacer(10)
        rootSizer.Add(SheetBasicViewsUtils(self).newMainSheetPartHorizontalSizer(self.newResourceCharacteristicsVerticalSizer()), 0, wx.CENTER)
        rootSizer.Add(SheetBasicViewsUtils(self).newLine(), 0, wx.EXPAND)
        rootSizer.AddSpacer(10)
        rootSizer.Add(SheetBasicViewsUtils(self).newButtonsPanelHorizontalSizer(self.submit), 0, wx.CENTER, 5)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])

    def newResourceCharacteristicsVerticalSizer(self):
        resourceCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        resourceCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newDescriptionAreaVerticalSizer(Consts.RESOURCE), 0, wx.CENTER)
        resourceCharacteristicsVerticalSizer.AddSpacer(10)
        resourceCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newPredecessorPickerHorizontalSizer(Consts.RESOURCE), 0, wx.CENTER)
        resourceCharacteristicsVerticalSizer.AddSpacer(5)
        resourceCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newSuccesorPickerHorizontalSizer(Consts.RESOURCE), 0, wx.CENTER)
        resourceCharacteristicsVerticalSizer.AddSpacer(10)
        resourceCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newEntityIconHorizontalSizer(), 0, wx.CENTER)
        resourceCharacteristicsVerticalSizer.AddSpacer(10)
        resourceCharacteristicsVerticalSizer.Add(self.newStartIncomePickerHorizontalSizer(), 0, wx.CENTER)
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


    def initSheetSubViews(self):
        self.NameInput = None
        self.descriptionArea = None
        self.imageBitmap = None
        self.predecessorSelector = None
        self.successorSelector = None
        self.log_area = None
        self.start_income_picker = None

    def resetSheetValues(
         self,
         sheetMode,
         entityNameInput = Consts.RESOURCE,
         descriptionAreaValue = "",
         startIncomePickerValue = 0,
         entityIconRelativePath = "DefaultBuilding.jpg",
         predecessorStringSelection = "None",
         successorStringSelection = "None"
    ):
        self.sheetChecker = sheetMode
        SheetBasicViewsUtils(self).reinitNameInput(entityNameInput, enabled = sheetMode.getMode() == ADD_MODE)
        self.descriptionArea.SetValue(descriptionAreaValue)
        self.start_income_picker.SetValue(startIncomePickerValue)
        self.entityIconRelativePath = entityIconRelativePath
        SheetBasicViewsUtils(self).setEntityImageBmp()
        SheetBasicViewsUtils(self).clearSelector(self.predecessorSelector, predecessorStringSelection)
        SheetBasicViewsUtils(self).clearSelector(self.successorSelector, successorStringSelection)
        self.log_area.SetValue("")

    def setUpEditMode(self, edit_element_name):
        self.resetSheetValues(
            sheetMode= EditModeSheetEntityChecker(self),
            entityNameInput= edit_element_name,
            descriptionAreaValue=SheetBasicViewsUtils(self).getEntityCharacteristic(edit_element_name, Consts.DESCRIPTION),
            startIncomePickerValue=int(SheetBasicViewsUtils(self).getEntityCharacteristic(edit_element_name, Consts.START_INCOME)),
            entityIconRelativePath=SheetBasicViewsUtils(self).getEntityCharacteristic(edit_element_name, Consts.TEXTURE_PATH),
            predecessorStringSelection= SheetBasicViewsUtils(self).getEntityCharacteristicFromEntitiesSet(edit_element_name, Consts.PREDECESSOR),
            successorStringSelection=SheetBasicViewsUtils(self).getEntityCharacteristicFromEntitiesSet(edit_element_name, Consts.SUCCESSOR)
        )

    def setUpAddMode(self):
        self.resetSheetValues(sheetMode=AddModeSheetEntityChecker(self))

    def onShow(self, event):
        OnShowUtil().onCreatorSheetShow(self, event)

    def submit(self, event):
        self.sheetChecker.onCheck(ResourceSheetChecker())


