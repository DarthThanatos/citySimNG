import wx
from wx.lib.scrolledpanel import ScrolledPanel

import Consts
from NumberFillingChecker import NumberFillingChecker
import json
import traceback
import re
from RelativePaths import relative_textures_path

class BuildingsPanel(ScrolledPanel):
    def __init__(self,parent, size, frame, currentDependencies, lists_of_names):
        ScrolledPanel.__init__(self, size = size, parent = parent, style = wx.SIMPLE_BORDER)
        self.SetupScrolling()
        self.wakeUpData = None

        self.lists_of_names = lists_of_names
        self.frame = frame
        self.currentDependencies = currentDependencies

        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        building_name_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        predecessor_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        successor_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        image_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        dwellers_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        type_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        between_lines_part_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        between_lines_part_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        log_area_vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        self.NameLabel = wx.StaticText(self,-1, "Name of this building")
        self.NameInput = wx.TextCtrl(self, -1, "Building")
        building_name_horizontal_sizer.Add(self.NameLabel)
        building_name_horizontal_sizer.AddSpacer(5)
        building_name_horizontal_sizer.Add(self.NameInput)
        vertical_sizer.AddSpacer(10)

        vertical_sizer.Add(building_name_horizontal_sizer, 0, wx.CENTER)
        vertical_sizer.AddSpacer(10)

        header_ln = wx.StaticLine(self, -1)
        vertical_sizer.Add(header_ln, 0, wx.EXPAND)
        vertical_sizer.AddSpacer(10)
        #===============================================================================================================
        descriptionFieldLabel = wx.StaticText(self, -1, "Description of this building for Tutorial module")
        between_lines_part_vertical_sizer.Add(descriptionFieldLabel, 0, wx.CENTER)
        self.descriptionArea = wx.TextCtrl(self, -1,size=(400, 200), style=wx.TE_MULTILINE)
        between_lines_part_vertical_sizer.Add(self.descriptionArea, 0, wx.CENTER)
        between_lines_part_vertical_sizer.AddSpacer(10)

        predecessor_label = wx.StaticText(self, -1, "Predecessor building:", size = (125, -1))
        predecessorChoiceList = ["None"] + self.lists_of_names[0]
        self.predecessorSelector = wx.ComboBox(self, choices=predecessorChoiceList, style=wx.CB_READONLY)
        self.predecessorSelector.Bind(wx.EVT_COMBOBOX, self.onPredecessorSelected)
        predecessor_horizontal_sizer.Add(predecessor_label)
        predecessor_horizontal_sizer.AddSpacer(10)
        predecessor_horizontal_sizer.Add(self.predecessorSelector)
        between_lines_part_vertical_sizer.Add(predecessor_horizontal_sizer, 0, wx.CENTER)
        between_lines_part_vertical_sizer.AddSpacer(5)

        successor_label = wx.StaticText(self, -1, "Successor building:", size = (125,-1))
        successorChoiceList = ["None"] + self.lists_of_names[0]
        self.successorSelector = wx.ComboBox(self, choices=successorChoiceList, style=wx.CB_READONLY)
        self.successorSelector.Bind(wx.EVT_COMBOBOX, self.onSuccessorSelected)
        successor_horizontal_sizer.Add(successor_label)
        successor_horizontal_sizer.AddSpacer(10)
        successor_horizontal_sizer.Add(self.successorSelector)
        between_lines_part_vertical_sizer.Add(successor_horizontal_sizer, 0, wx.CENTER)
        between_lines_part_vertical_sizer.AddSpacer(10)

        img_info_label = wx.StaticText(self, -1, "Your texture: ")
        img_selector_btn = wx.Button(self, -1, label = "Choose another texture", size = (-1, 32))
        self.Bind(wx.EVT_BUTTON, self.onImageSelected ,img_selector_btn)
        image = wx.Image(name = relative_textures_path + "house.png") #"..\\..\\resources\\Textures\\house.png"
        self.texture_name = "house.png"
        self.imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))
        image_horizontal_sizer.Add(img_info_label)
        image_horizontal_sizer.AddSpacer(10)
        image_horizontal_sizer.Add(self.imageBitmap)
        image_horizontal_sizer.AddSpacer(10)
        image_horizontal_sizer.Add(img_selector_btn)
        between_lines_part_vertical_sizer.Add(image_horizontal_sizer, 0, wx.CENTER)
        between_lines_part_vertical_sizer.AddSpacer(10)

        dweller_name_label = wx.StaticText(self, -1, "Name of dweller being here: ")
        dwellersNamesChoiceList = self.lists_of_names[2]
        dwellersNamesChoiceList = self.currentDependencies["Buildings"].keys()
        self.dwellers_names_selector = wx.ComboBox(self, choices=dwellersNamesChoiceList, style=wx.CB_READONLY)

        dwellers_amount_label = wx.StaticText(self, -1, "Amount of dwellers in this building: ")
        self.dwellers_amount =  wx.SpinCtrl(self, value='0', size=(60, -1), min=0, max = 50)
        dwellers_horizontal_sizer.Add(dweller_name_label)
        dwellers_horizontal_sizer.AddSpacer(10)
        dwellers_horizontal_sizer.Add(self.dwellers_names_selector)
        dwellers_horizontal_sizer.AddSpacer(10)
        dwellers_horizontal_sizer.Add(dwellers_amount_label)
        dwellers_horizontal_sizer.AddSpacer(10)
        dwellers_horizontal_sizer.Add(self.dwellers_amount)

        between_lines_part_vertical_sizer.Add(dwellers_horizontal_sizer, 0, wx.CENTER)
        between_lines_part_vertical_sizer.AddSpacer(10)

        type_label = wx.StaticText(self, -1, "Type of building: ")
        typeChoiceList = ["Industrial", "Domestic"]
        self.type_of_building_selector = wx.ComboBox(self, choices=typeChoiceList, style=wx.CB_READONLY, value = "Industrial")
        type_horizontal_sizer.Add(type_label)
        type_horizontal_sizer.AddSpacer(10)
        type_horizontal_sizer.Add(self.type_of_building_selector)
        between_lines_part_vertical_sizer.Add(type_horizontal_sizer, 0, wx.CENTER)
        between_lines_part_vertical_sizer.AddSpacer(10)

        ln = wx.StaticLine(self, -1)
        between_lines_part_vertical_sizer.Add(ln, 0, wx.EXPAND)
        between_lines_part_vertical_sizer.AddSpacer(10)

        self.resources_produced_panel = NumberFillingChecker(self,
                                                             size,
                                                             self.currentDependencies,
                                                             "Resource:",
                                                             "Produced in quantity:",
                                                             "Produced resources",
                                                             between_lines_part_vertical_sizer,
                                                             json_key="Produces",
                                                             part_name="Buildings")

        bottom_line = wx.StaticLine(self, -1)
        between_lines_part_vertical_sizer.Add(bottom_line, 0, wx.EXPAND)
        between_lines_part_vertical_sizer.AddSpacer(10)

        self.resources_consumed_panel = NumberFillingChecker(self,
                                                             size,
                                                             self.currentDependencies,
                                                             "Resource:",
                                                             "Consumed in quantity:",
                                                             "Consumed resources",
                                                             between_lines_part_vertical_sizer,
                                                             json_key="Consumes",
                                                             part_name="Buildings")

        bottom_line = wx.StaticLine(self, -1)
        between_lines_part_vertical_sizer.Add(bottom_line, 0, wx.EXPAND)
        between_lines_part_vertical_sizer.AddSpacer(10)

        self.cost_in_resources_panel = NumberFillingChecker(self,
                                                             size,
                                                             self.currentDependencies,
                                                             "Resource:",
                                                             "Costs:",
                                                             "Cost of placing a building in resources",
                                                             between_lines_part_vertical_sizer,
                                                             json_key="Cost\nin\nresources",
                                                            part_name="Buildings")
        self.children = [self.resources_consumed_panel, self.resources_produced_panel, self.cost_in_resources_panel]

        between_lines_part_horizontal_sizer.Add(between_lines_part_vertical_sizer, 0, wx.LEFT)
        log_area_label = wx.StaticText(self, -1, "Below lies logging area, showing error msgs")
        self.log_area = wx.TextCtrl(self, -1, size=(500, 450), style=wx.TE_MULTILINE | wx.TE_READONLY)
        log_area_vertical_sizer.AddSpacer(100)
        log_area_vertical_sizer.Add(log_area_label, 0, wx.CENTER)
        log_area_vertical_sizer.Add(self.log_area, 0, wx.CENTER)
        log_area_vertical_sizer.AddSpacer(50)
        between_lines_part_horizontal_sizer.AddSpacer(75)

        separating_ln = wx.StaticLine(self, -1, style=wx.VERTICAL)
        between_lines_part_horizontal_sizer.Add(separating_ln, 0, wx.EXPAND)
        between_lines_part_horizontal_sizer.AddSpacer(50)

        between_lines_part_horizontal_sizer.Add(log_area_vertical_sizer, 0, wx.RIGHT)
        vertical_sizer.Add(between_lines_part_horizontal_sizer, 0, wx.CENTER)
        #===============================================================================================================
        bottom_line = wx.StaticLine(self, -1)
        vertical_sizer.Add(bottom_line, 0, wx.EXPAND)
        vertical_sizer.AddSpacer(10)

        main_panel_btn = wx.Button(self, label="Cancel")
        self.Bind(wx.EVT_BUTTON, self.moveToMainPanel, main_panel_btn)

        create_resource_btn = wx.Button(self, label = "Submit")
        self.Bind(wx.EVT_BUTTON, self.submit, create_resource_btn)



        buttons_horizontal_sizer.Add(create_resource_btn)
        buttons_horizontal_sizer.Add(main_panel_btn)
        vertical_sizer.Add(buttons_horizontal_sizer, 0, wx.CENTER, 5)
        vertical_sizer.AddSpacer(75)

        self.SetSizer(vertical_sizer)
        vertical_sizer.SetDimension(0, 0, size[0], size[1])
        self.Bind(wx.EVT_SHOW, self.onShow, self)

        self.check_and_dump_name = self.checkAndDumpNameAddMode
        self.mount_exit_msg = self.mountSuccessAddMsg


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
        for child in self.children:
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

        for child in self.children:
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
        for child in self.children:
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


    def onImageSelected(self, event):
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