import wx
from wx.lib.scrolledpanel import ScrolledPanel

import Consts
from CreatorView.SheetBasicViewsUtils import SheetBasicViewsUtils
from NumberFillingChecker import NumberFillingChecker
from utils.OnShowUtil import OnShowUtil
from viewmodel.SheetEntityChecker import BuildingSheetChecker, AddModeSheetEntityChecker, EditModeSheetEntityChecker, \
    ADD_MODE, EDIT_MODE


class BuildingSheet(ScrolledPanel):
    def __init__(self,parent, size, frame, currentDependencies):
        ScrolledPanel.__init__(self, size = size, parent = parent, style = wx.SIMPLE_BORDER)
        self.SetupScrolling()
        self.size = size
        self.frame = frame
        self.currentDependencies = currentDependencies
        self.wakeUpData = None
        self.entityIconRelativePath = "house.png"
        self.sheet_name =  Consts.BUILDINGS
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.sheetChecker = AddModeSheetEntityChecker(self)
        self.initSheetSubViews()
        self.initRootSizer()

    def getEntityType(self):
        return Consts.BUILDING

    def getEntityNameKey(self):
        return Consts.BUILDING_NAME

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddSpacer(10)
        rootSizer.Add(SheetBasicViewsUtils(self).newEntityNameHorizontalSizer(Consts.BUILDING), 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        rootSizer.Add(SheetBasicViewsUtils(self).newLine(), 0, wx.EXPAND)
        rootSizer.AddSpacer(10)
        rootSizer.Add(SheetBasicViewsUtils(self).newMainSheetPartHorizontalSizer(self.newBuildingCharacteristicsVerticalSizer()), 0, wx.CENTER, 0, wx.CENTER)
        rootSizer.Add(SheetBasicViewsUtils(self).newLine(), 0, wx.EXPAND)
        rootSizer.AddSpacer(10)
        rootSizer.Add(SheetBasicViewsUtils(self).newButtonsPanelHorizontalSizer(self.submit), 0, wx.CENTER, 5)
        rootSizer.AddSpacer(75)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])


    def newBuildingCharacteristicsVerticalSizer(self):
        buildingCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        buildingCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newDescriptionAreaVerticalSizer(Consts.BUILDING), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newPredecessorPickerHorizontalSizer(Consts.BUILDING), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(5)
        buildingCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newSuccesorPickerHorizontalSizer(Consts.BUILDING), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newEntityIconHorizontalSizer(), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
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
        buildingCharacteristicsVerticalSizer.Add(self.newResourcesConsumedChecker(), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newLine(), 0, wx.EXPAND)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(self.newCostInResourcesChecker(), 0, wx.CENTER)
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        return buildingCharacteristicsVerticalSizer

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

    def newResourcesProducedChecker(self):
        return self.newNumberFillingChecker(
            "Produced in quantity:",
            "Produced resources",
            Consts.PRODUCES
        )

    def newResourcesConsumedChecker(self):
        return self.newNumberFillingChecker(
            "Consumed in quantity:",
            "Consumed resources",
            Consts.CONSUMES
        )

    def newCostInResourcesChecker(self):
        return self.newNumberFillingChecker(
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
        return self.dwellers_names_selector

    def newDwellerNameLabel(self):
        return wx.StaticText(self, -1, "Name of dweller being here: ")

    def newDwellersAmountLabel(self):
        return wx.StaticText(self, -1, "Amount of dwellers in this building: ")

    def newDwellersAmountSpinner(self):
        self.dwellers_amount =  wx.SpinCtrl(self, value='0', size=(60, -1), min=0, max = 50)
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
        return self.type_of_building_selector

    def initSheetSubViews(self):
        self.NameInput = None
        self.descriptionArea = None
        self.imageBitmap = None
        self.predecessorSelector = None
        self.successorSelector = None
        self.type_of_building_selector = None
        self.dwellers_names_selector = None
        self.log_area = None
        self.dwellers_amount = None
        self.resources_produced_panel = None
        self.resources_consumed_panel = None
        self.cost_in_resources_panel = None
        self.childrenCheckers = []

    def getAllDwellerEntities(self):
        return self.currentDependencies["Dwellers"].keys()

    def resetSheetValues(
         self,
         sheetMode,
         entityNameInput = Consts.BUILDING,
         descriptionAreaValue = "",
         entityIconRelativePath = "house.png",
         predecessorStringSelection = "None",
         successorStringSelection = "None",
         dwellerNameSelection = "None",
         typeOfBuilding = "Industrial",
         dwellersAmount = 0
    ):
        self.sheetChecker = sheetMode
        self.entityIconRelativePath = entityIconRelativePath
        SheetBasicViewsUtils(self).reinitNameInput(entityNameInput, enabled = sheetMode.getMode() == ADD_MODE)
        self.descriptionArea.SetValue(descriptionAreaValue)
        SheetBasicViewsUtils(self).setEntityImageBmp()
        SheetBasicViewsUtils(self).clearSelector(self.predecessorSelector, predecessorStringSelection)
        SheetBasicViewsUtils(self).clearSelector(self.successorSelector, successorStringSelection)
        SheetBasicViewsUtils(self).clearSelector(self.dwellers_names_selector, dwellerNameSelection, self.getAllDwellerEntities())
        self.type_of_building_selector.SetStringSelection(typeOfBuilding)
        self.dwellers_amount.SetValue(dwellersAmount)
        self.log_area.SetValue("")
        for child in self.childrenCheckers: child.fillWithEntries(entityNameInput if sheetMode.getMode() == EDIT_MODE else None)

    def setUpEditMode(self, edit_element_name):
        self.resetSheetValues(
            sheetMode= EditModeSheetEntityChecker(self),
            entityNameInput= edit_element_name,
            descriptionAreaValue=SheetBasicViewsUtils(self).getEntityCharacteristic(edit_element_name, Consts.DESCRIPTION),
            entityIconRelativePath=SheetBasicViewsUtils(self).getEntityCharacteristic(edit_element_name, Consts.TEXTURE_PATH),
            predecessorStringSelection=SheetBasicViewsUtils(self).getEntityCharacteristicFromEntitiesSet(edit_element_name, Consts.PREDECESSOR),
            successorStringSelection=SheetBasicViewsUtils(self).getEntityCharacteristicFromEntitiesSet(edit_element_name, Consts.SUCCESSOR),
            dwellerNameSelection = SheetBasicViewsUtils(self).getEntityCharacteristic(edit_element_name, Consts.DWELLER_NAME),
            typeOfBuilding = SheetBasicViewsUtils(self).getEntityCharacteristic(edit_element_name, Consts.TYPE),
            dwellersAmount = int(SheetBasicViewsUtils(self).getEntityCharacteristic(edit_element_name, Consts.DWELLERS_AMOUNT))
        )

    def setUpAddMode(self):
        self.resetSheetValues(sheetMode=AddModeSheetEntityChecker(self))

    def onShow(self, event):
        OnShowUtil().onCreatorSheetShow(self, event)

    def submit(self, event):
        self.sheetChecker.onCheck(BuildingSheetChecker())
