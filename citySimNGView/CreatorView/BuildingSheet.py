import wx
from wx.lib.scrolledpanel import ScrolledPanel

import Consts
from CreatorView.RestorableView import RestorableSelector, RestorableDwellersAmount, RestorableTypeOfBuilding, \
    RestorableDwellersNamesSelector
from CreatorView.SheetBasicViewsUtils import SheetBasicViewsUtils
from NumberFillingChecker import NumberFillingChecker
from utils.OnShowUtil import OnShowUtil
from utils.SheetEntitiesUtils import SheetEntitiesUtils
from viewmodel.SheetEntityChecker import BuildingSheetChecker, AddModeSheetEntityChecker, EditModeSheetEntityChecker, EDIT_MODE


class BuildingSheet(ScrolledPanel):
    def __init__(self,parent, size, frame, currentDependencies):
        ScrolledPanel.__init__(self, size = size, parent = parent, style = wx.SIMPLE_BORDER)
        self.SetupScrolling()
        self.size = size
        self.frame = frame
        self.currentDependencies = currentDependencies
        self.wakeUpData = None
        self.entityIconRelativePath = self.getDefaultIconRelativePath()
        self.sheet_name =  Consts.BUILDINGS
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.sheetChecker = AddModeSheetEntityChecker(self)
        self.childrenCheckers = []
        self.restorableViews = []
        SheetBasicViewsUtils(self).initRootSizer(self.newBuildingCharacteristicsVerticalSizer(), topPadding=10)

    def newBuildingCharacteristicsVerticalSizer(self):
        buildingCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        buildingCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newBasicCharacteristicsVerticalSizer(), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.Add(self.newDwellersHorizontalSizer(), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(self.newBuildingTypeHorizontalSizer(), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newLine(), 0, wx.EXPAND)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(self.newResourcesProducedChecker(), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newLine(), 0, wx.EXPAND)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newResourcesConsumedChecker(), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newLine(), 0, wx.EXPAND)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(self.newCostInResourcesChecker(), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        return buildingCharacteristicsVerticalSizer


    def newResourcesProducedChecker(self):
        return SheetBasicViewsUtils(self).newNumberFillingChecker(
            "Produced in quantity:",
            "Produced resources",
            Consts.PRODUCES
        )

    def newCostInResourcesChecker(self):
        return SheetBasicViewsUtils(self).newNumberFillingChecker(
            "Costs:",
            "Cost of placing a building in resources",
            Consts.COST_IN_RESOURCES
        )

    def newDwellersHorizontalSizer(self):
        dwellers_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        dwellers_horizontal_sizer.Add(self.newDwellerNameLabel())
        dwellers_horizontal_sizer.AddSpacer(10)
        dwellers_horizontal_sizer.Add(self.newDwellersNamesSelector())
        dwellers_horizontal_sizer.AddSpacer(10)
        dwellers_horizontal_sizer.Add(self.newDwellersAmountLabel())
        dwellers_horizontal_sizer.AddSpacer(10)
        dwellers_horizontal_sizer.Add(self.newDwellersAmountSpinner())
        return dwellers_horizontal_sizer

    def newDwellersNamesSelector(self):
        self.dwellers_names_selector = wx.ComboBox(self, choices=["None"], style=wx.CB_READONLY)
        self.restorableViews.append(
            RestorableDwellersNamesSelector(
                sheet_view=self,
                selector=self.dwellers_names_selector,
                restoreKey = Consts.DWELLER_NAME
            )
        )
        return self.dwellers_names_selector

    def newDwellerNameLabel(self):
        return wx.StaticText(self, -1, "Name of dweller being here: ")

    def newDwellersAmountLabel(self):
        return wx.StaticText(self, -1, "Amount of dwellers in this building: ")

    def newDwellersAmountSpinner(self):
        self.dwellers_amount =  wx.SpinCtrl(self, value='0', size=(60, -1), min=0, max = 50)
        self.restorableViews.append(RestorableDwellersAmount(self, self.dwellers_amount))
        return self.dwellers_amount

    def newBuildingTypeHorizontalSizer(self):
        type_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        type_horizontal_sizer.Add(self.newBuildingTypeInfoLabel())
        type_horizontal_sizer.AddSpacer(10)
        type_horizontal_sizer.Add(self.newBuildingTypeSelector())
        return type_horizontal_sizer

    def newBuildingTypeInfoLabel(self):
        return wx.StaticText(self, -1, "Type of building: ")

    def newBuildingTypeSelector(self):
        self.type_of_building_selector =wx.ComboBox(self, choices=["Industrial", "Domestic"], style=wx.CB_READONLY, value = "Industrial")
        self.restorableViews.append(RestorableTypeOfBuilding(self, self.type_of_building_selector))
        return self.type_of_building_selector

    def getDefaultIconRelativePath(self):
        return "house.png"

    def getEntityType(self):
        return Consts.BUILDING

    def getEntityNameKey(self):
        return Consts.BUILDING_NAME

    def setupSheetMode(self, sheetMode, edit_element_name = None):
        SheetBasicViewsUtils(self).setupMode(sheetMode,edit_element_name)
        for child in self.childrenCheckers: child.fillWithEntries(edit_element_name if sheetMode.getMode() == EDIT_MODE else None)

    def setUpEditMode(self, edit_element_name):
        self.setupSheetMode(EditModeSheetEntityChecker(self), edit_element_name)

    def setUpAddMode(self):
        self.setupSheetMode(AddModeSheetEntityChecker(self))

    def onShow(self, event):
        OnShowUtil().onCreatorSheetShow(self, event)

    def submit(self, event):
        self.sheetChecker.onCheck(BuildingSheetChecker())
