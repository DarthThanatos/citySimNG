import wx
from wx.lib.scrolledpanel import ScrolledPanel

import Consts
from CreatorView.SheetBasicViewsFactory import SheetBasicViewsFactory
from NumberFillingChecker import NumberFillingChecker
import json
import traceback
import re
from RelativePaths import relative_textures_path

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
        self.initSheetSubViews()
        self.initRootSizer()

        self.Bind(wx.EVT_SHOW, self.onShow, self)

        self.check_and_dump_name = self.checkAndDumpNameAddMode
        self.mount_exit_msg = self.mountSuccessAddMsg

    def initSheetSubViews(self):
        self.NameInput = None
        self.descriptionArea = None
        self.imageBitmap = None
        self.predecessorSelector = None
        self.successorSelector = None
        self.type_of_building_selector = None
        self.log_area = None
        self.dwellers_names_selector = None
        self.dwellers_amount = None
        self.resources_produced_panel = None
        self.resources_consumed_panel = None
        self.cost_in_resources_panel = None
        self.childrenCheckers = []

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddSpacer(10)
        rootSizer.Add(
            SheetBasicViewsFactory(self)
                .newEntityNameHorizontalSizer(Consts.BUILDING), 0, wx.CENTER)
        rootSizer.AddSpacer(10)
        rootSizer.Add(
            SheetBasicViewsFactory(self).newLine(), 0, wx.EXPAND
        )
        rootSizer.AddSpacer(10)
        rootSizer.Add(
            SheetBasicViewsFactory(self)
                .newMainSheetPartHorizontalSizer(
                self.newBuildingCharacteristicsVerticalSizer()
            ), 0, wx.CENTER, 0, wx.CENTER
        )
        rootSizer.Add(
            SheetBasicViewsFactory(self).newLine(), 0, wx.EXPAND
        )
        rootSizer.AddSpacer(10)
        rootSizer.Add(
            SheetBasicViewsFactory(self)
                .newButtonsPanelHorizontalSizer(
                    self.submit, self.moveToMainPanel
            ), 0, wx.CENTER, 5)
        rootSizer.AddSpacer(75)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, self.size[0], self.size[1])


    def newBuildingCharacteristicsVerticalSizer(self):
        buildingCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        buildingCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self)
                .newDescriptionAreaVerticalSizer(Consts.BUILDING), 0, wx.CENTER
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self)
                .newPredecessorPickerHorizontalSizer(Consts.BUILDING), 0, wx.CENTER
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(5)
        buildingCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self)
                .newSuccesorPickerHorizontalSizer(Consts.BUILDING), 0, wx.CENTER
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self)
                .newEntityIconHorizontalSizer(self.selectImage), 0, wx.CENTER
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(
            self.newDwellersHorizontalSizer(), 0, wx.CENTER
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(
            self.newBuildingTypeHorizontalSizer(), 0, wx.CENTER
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self).newLine(), 0, wx.EXPAND
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(
            self.newResourcesProducedChecker(), 0, wx.CENTER
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self).newLine(), 0, wx.EXPAND
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(
            self.newResourcesConsumedChecker(), 0, wx.CENTER
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(
            SheetBasicViewsFactory(self).newLine(), 0, wx.EXPAND
        )
        buildingCharacteristicsVerticalSizer.AddSpacer(10)
        buildingCharacteristicsVerticalSizer.Add(
            self.newCostInResourcesChecker(), 0, wx.CENTER
        )
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
        self.type_of_building_selector = wx.ComboBox(
            self, choices=["Industrial", "Domestic"], style=wx.CB_READONLY, value = "Industrial"
        )
        return self.type_of_building_selector




    def resetContents(self):
        self.predecessorSelector.Clear()
        self.successorSelector.Clear()
        self.dwellers_names_selector.Clear()
        for buildingName in self.currentDependencies["Buildings"].keys() + ["None"]:
            self.predecessorSelector.Append(buildingName)
            self.successorSelector.Append(buildingName)
        for dwellerName in self.currentDependencies["Dwellers"].keys():
            self.dwellers_names_selector.Append(dwellerName)
        self.dwellers_amount.SetValue(0)
        self.predecessorSelector.SetStringSelection("None")
        self.successorSelector.SetStringSelection("None")
        self.log_area.SetValue("")


    def mountSuccessAddMsg(self, building_name):
        return {"Log": "Successfully added " + building_name + " to buildings list\n"}

    def mountSuccessEditMsg(self, building_name):
        return {"Log": "Successfully edited " + building_name + " building\n"}


    def setUpAddMode(self):
        print "Add mode"
        self.check_and_dump_name = self.checkAndDumpNameAddMode
        self.NameInput.SetValue("Building")
        self.NameInput.Enable()
        self.mount_exit_msg = self.mountSuccessAddMsg
        self.descriptionArea.SetValue("")

        self.texture_name = "house.png"
        image = wx.Image(relative_textures_path + self.texture_name) #"..\\..\\resources\\Textures\\"
        image = image.Scale(32,32)
        self.imageBitmap.SetBitmap(wx.BitmapFromImage(image))
        for child in self.childrenCheckers:
            child.reset_init_mode = child.resetContentsInit_AddMode
            child.resetContents(None)

    def setUpEditMode(self, edit_element_name):
        print "Editing", edit_element_name
        self.check_and_dump_name = self.checkAndDumpNameEditMode
        self.NameInput.SetValue(edit_element_name)
        self.NameInput.Disable()
        self.mount_exit_msg = self.mountSuccessEditMsg
        self.descriptionArea.SetValue(self.currentDependencies["Buildings"][edit_element_name][Consts.DESCRIPTION])

        self.texture_name = self.currentDependencies["Buildings"][edit_element_name][Consts.TEXTURE_PATH]
        try:
            image = wx.Image(relative_textures_path + self.texture_name) #"..\\..\\resources\\Textures\\"
            image = image.Scale(32,32)
            self.imageBitmap.SetBitmap(wx.BitmapFromImage(image))
        except Exception:
            traceback.print_exc()

        for child in self.childrenCheckers:
            child.reset_init_mode = child.resetContentsInit_EditMode
            child.resetContents(edit_element_name)
        successorVal = self.currentDependencies["Buildings"][edit_element_name]["Successor"]
        successorVal = successorVal if successorVal in self.currentDependencies["Buildings"].keys() else "None"
        predecessorVal = self.currentDependencies["Buildings"][edit_element_name]["Predecessor"]
        predecessorVal = predecessorVal if predecessorVal in self.currentDependencies["Buildings"].keys() else "None"
        self.predecessorSelector.SetStringSelection(predecessorVal)
        self.successorSelector.SetStringSelection(successorVal)

        dwellerTypeVal = self.currentDependencies["Buildings"][edit_element_name]["Dweller\nName"]
        amount_of_dwellers_val = self.currentDependencies["Buildings"][edit_element_name][Consts.DWELLERS_AMOUNT]
        if not dwellerTypeVal in self.currentDependencies["Dwellers"].keys():
            dwellerTypeVal = ""
            amount_of_dwellers_val = 0
        self.dwellers_amount.SetValue(amount_of_dwellers_val)
        self.dwellers_names_selector.SetStringSelection(dwellerTypeVal)

        print "Dweller living here: ", dwellerTypeVal
        building_type_val = self.currentDependencies["Buildings"][edit_element_name][Consts.TYPE]
        self.type_of_building_selector.SetStringSelection(building_type_val)

    def onShow(self, event):
        if event.GetShow():
            self.resetContents()
            self.setUpAddMode()
            if not self.wakeUpData == None:
                try:
                    edit_element_name = self.wakeUpData["Edit"]
                    self.setUpEditMode(edit_element_name)
                except:
                    traceback.print_exc()
                self.wakeUpData = None

    def checkAndDumpNameEditMode(self, result_struct):
        result_struct["Result"][Consts.BUILDING_NAME] = self.NameInput.GetValue()
        return True

    def checkAndDumpNameAddMode(self,result_struct):
        buildings_names = self.currentDependencies["Buildings"].keys()
        building_name = self.NameInput.GetValue()
        if  re.sub(r'\s', "", building_name) == "":
            error_msg =  "-> Not a valid name\n"
            result_struct["ErrorMsg"] += error_msg
            return False
        if building_name in buildings_names:
            error_msg ="-> Building name already taken\n"
            result_struct["ErrorMsg"] += error_msg
            return False
        result_struct["Result"][Consts.BUILDING_NAME] = building_name
        return True

    def checkAndDumpPredAndSucc(self, result_struct):
        predecessor_name = self.predecessorSelector.GetStringSelection()
        successor_name = self.successorSelector.GetStringSelection()
        building_name = self.NameInput.GetValue()
        if successor_name == predecessor_name and successor_name != "None":
            result_struct["ErrorMsg"] += "-> Predecessor and Successor cannot be the same (both can be None though)\n"
            return False
        if successor_name == building_name :
            result_struct["ErrorMsg"] += "-> A building cannot be its own successor\n"
            return False
        if predecessor_name == building_name :
            result_struct["ErrorMsg"] += "-> A building cannot be its own predeccessor\n"
            return False
        result_struct["Result"][Consts.PREDECESSOR] = predecessor_name
        result_struct["Result"][Consts.SUCCESSOR] = successor_name
        return True

    def checkAndDumpDescriptionArea(self, result_struct):
        description_content = self.descriptionArea.GetValue()
        if re.sub(r'\s', "", description_content) == "":
            result_struct["ErrorMsg"] += "-> Please enter description of this building\n"
            return False
        result_struct["Result"][Consts.DESCRIPTION] = description_content
        return True

    def checkAndDumpTexture(self, result_struct):
        result_struct["Result"][Consts.TEXTURE_PATH] = self.texture_name
        return True

    def checkAndDumpDweller(self, result_struct):
        dweller_name = self.dwellers_names_selector.GetStringSelection()
        if dweller_name == "":
            result_struct["ErrorMsg"] += "-> Please select a dweller that lives here\n"
            return False
        result_struct["Result"][Consts.DWELLER_NAME] = dweller_name
        return True

    def checkAndDumpDwellersAmount(self, result_struct):
        result_struct["Result"][Consts.DWELLERS_AMOUNT] = self.dwellers_amount.GetValue()
        return True

    def checkAndDumpTypeOfBuilding(self, result_struct):
        result_struct["Result"][Consts.TYPE] = self.type_of_building_selector.GetValue()
        return True

    def submit(self, event):
        correct = True
        result_struct = {"ErrorMsg":"Errors detected:\n", "Result":{}} # init error msg displayed if sth went wrong

        correct &= self.check_and_dump_name(result_struct)
        correct &= self.checkAndDumpPredAndSucc(result_struct)
        correct &= self.checkAndDumpDescriptionArea(result_struct)
        correct &= self.checkAndDumpTexture(result_struct)
        correct &= self.checkAndDumpDweller(result_struct)
        correct &= self.checkAndDumpDwellersAmount(result_struct)
        correct &= self.checkAndDumpTypeOfBuilding(result_struct)
        for child in self.childrenCheckers:
            correct &= child.checkAndDumpCheckers(result_struct)
        if not correct:
            self.log_area.SetValue(result_struct["ErrorMsg"])
            return

        building_name = self.NameInput.GetValue()
        result_msg = self.mount_exit_msg(building_name)
        self.currentDependencies["Buildings"][building_name] = result_struct["Result"]
        print json.dumps(result_struct["Result"])
        self.frame.showPanel("main_panel", initDataForSearchedPanel=result_msg)

    def onSuccessorSelected(self, event):
        pass

    def onPredecessorSelected(self, event):
        pass

    def fillDepenendenciesPanelWithContent(self, content_dict):
        self.resetContents()
        try:
            pass
        except Exception:
            return False
        return True

    def checkDependenciesPanelsCorrectness(self):
        pass

    def moveToMainPanel(self,event):
        self.frame.showPanel("main_panel",initDataForSearchedPanel=None)


    def selectImage(self, event):
        dlg = wx.FileDialog(
            self,
            defaultDir= relative_textures_path,#"..\\..\\resources\\Textures\\",
            message="Choose an image",
            wildcard="*.png | *.jpg",
            style=wx.FD_OPEN
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "Filename:", dlg.GetFilename()
            self.texture_name = dlg.GetFilename()
            image = wx.Image(path)
            image = image.Scale(32,32)
            self.imageBitmap.SetBitmap(wx.BitmapFromImage(image))