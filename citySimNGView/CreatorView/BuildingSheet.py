import wx

import Consts
from CreatorView.RestorableView import  RestorableDwellersAmount, RestorableTypeOfBuilding, \
    RestorableDwellersNamesSelector
from CreatorView.SheetView import SheetView
from viewmodel.SheetEntityChecker import BuildingSheetChecker


class BuildingSheet(SheetView):
    def __init__(self, parent, size, frame, currentDependencies):
        super(BuildingSheet, self).__init__(parent, size, frame, currentDependencies)
        self.initRootSizer(self.newBuildingCharacteristicsVerticalSizer(), topPadding=10)

    def getDefaultIconRelativePath(self):
        return "house.png"

    def getEntityType(self):
        return Consts.BUILDING

    def getEntityNameKey(self):
        return Consts.BUILDING_NAME

    def getSheetName(self):
        return Consts.BUILDINGS

    def getEntityChecker(self):
        return BuildingSheetChecker()

    def submit(self, event):
        self.sheetChecker.onCheck(BuildingSheetChecker())

    def addToViewWithSpaceAndLine(self, sizer, view):
        self.addToSizerWithSpace(sizer, view)
        self.addToSizerWithSpace(sizer, self.newLine(), alignment=wx.EXPAND)

    def addSubViewsWithSpacesAndLinesToBuildingsCharacteristicsSizer(self, buildings_characteristics_sizer):
        self.addToViewWithSpaceAndLine(buildings_characteristics_sizer, self.newBuildingTypeHorizontalSizer())
        self.addToViewWithSpaceAndLine(buildings_characteristics_sizer, self.newResourcesProducedChecker())
        self.addToViewWithSpaceAndLine(buildings_characteristics_sizer, self.newResourcesConsumedChecker())

    def newBuildingCharacteristicsVerticalSizer(self):
        buildingCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        buildingCharacteristicsVerticalSizer.Add(self.newBasicCharacteristicsVerticalSizer(), 0, wx.CENTER)
        self.addToSizerWithSpace(buildingCharacteristicsVerticalSizer, self.newDwellersHorizontalSizer())
        self.addSubViewsWithSpacesAndLinesToBuildingsCharacteristicsSizer(buildingCharacteristicsVerticalSizer)
        self.addToSizerWithSpace(buildingCharacteristicsVerticalSizer, self.newCostInResourcesChecker())
        return buildingCharacteristicsVerticalSizer


    def newResourcesProducedChecker(self):
        return self.newNumberFillingChecker(
            "Produced in quantity:",
            "Produced resources",
            Consts.PRODUCES)

    def newCostInResourcesChecker(self):
        return self.newNumberFillingChecker(
            "Costs:",
            "Cost of placing a building in resources",
            Consts.COST_IN_RESOURCES)

    def newDwellersHorizontalSizer(self):
        dwellers_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(dwellers_horizontal_sizer, self.newDwellerNameLabel())
        self.addToSizerWithSpace(dwellers_horizontal_sizer, self.newDwellersNamesSelector())
        self.addToSizerWithSpace(dwellers_horizontal_sizer, self.newDwellersAmountLabel())
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
        self.addToSizerWithSpace(type_horizontal_sizer, self.newBuildingTypeInfoLabel())
        type_horizontal_sizer.Add(self.newBuildingTypeSelector())
        return type_horizontal_sizer

    def newBuildingTypeInfoLabel(self):
        return wx.StaticText(self, -1, "Type of building: ")

    def newBuildingTypeSelector(self):
        self.type_of_building_selector =wx.ComboBox(self, choices=["Industrial", "Domestic"], style=wx.CB_READONLY, value = "Industrial")
        self.restorableViews.append(RestorableTypeOfBuilding(self, self.type_of_building_selector))
        return self.type_of_building_selector