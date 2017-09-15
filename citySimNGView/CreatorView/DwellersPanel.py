import wx
from wx.lib.scrolledpanel import ScrolledPanel
from NumberFillingChecker import NumberFillingChecker
import traceback
import re
import json
from RelativePaths import relative_textures_path
import Consts

class DwellersPanel(ScrolledPanel):
    def __init__(self,parent, size, frame, currentDependencies):
        ScrolledPanel.__init__(self, size = size, parent = parent, style = wx.SIMPLE_BORDER)
        self.SetupScrolling()
        self.wakeUpData = None

        self.frame = frame
        self.currentDependencies = currentDependencies
        self.sheet_name = Consts.DWELLERS

        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        dweller_name_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        predecessor_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        successor_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        image_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        between_lines_part_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        between_lines_part_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        log_area_vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        self.NameLabel = wx.StaticText(self,-1, "Name of this dweller")
        self.NameInput = wx.TextCtrl(self, -1, "Dweller")
        dweller_name_horizontal_sizer.Add(self.NameLabel)
        dweller_name_horizontal_sizer.AddSpacer(5)
        dweller_name_horizontal_sizer.Add(self.NameInput)
        vertical_sizer.AddSpacer(75)

        vertical_sizer.Add(dweller_name_horizontal_sizer, 0, wx.CENTER)
        vertical_sizer.AddSpacer(10)

        header_ln = wx.StaticLine(self, -1)
        vertical_sizer.Add(header_ln, 0, wx.EXPAND)
        vertical_sizer.AddSpacer(10)

        #===============================================================================================================
        descriptionFieldLabel = wx.StaticText(self, -1, "Description of this dweller for Tutorial module")
        between_lines_part_vertical_sizer.Add(descriptionFieldLabel, 0, wx.CENTER)
        self.descriptionArea = wx.TextCtrl(self, -1,size=(400, 200), style=wx.TE_MULTILINE)
        between_lines_part_vertical_sizer.Add(self.descriptionArea, 0, wx.CENTER)
        between_lines_part_vertical_sizer.AddSpacer(10)

        predecessor_label = wx.StaticText(self, -1, "Predecessor dweller:", size = (125, -1))
        predecessorChoiceList = ["None"] + self.currentDependencies["Dwellers"].keys()
        self.predecessorSelector = wx.ComboBox(self, choices=predecessorChoiceList, style=wx.CB_READONLY)
        self.predecessorSelector.Bind(wx.EVT_COMBOBOX, self.onPredecessorSelected)
        predecessor_horizontal_sizer.Add(predecessor_label)
        predecessor_horizontal_sizer.AddSpacer(10)
        predecessor_horizontal_sizer.Add(self.predecessorSelector)
        between_lines_part_vertical_sizer.Add(predecessor_horizontal_sizer, 0, wx.CENTER)
        between_lines_part_vertical_sizer.AddSpacer(5)

        successor_label = wx.StaticText(self, -1, "Successor dweller:", size = (125,-1))
        successorChoiceList = ["None"] + self.currentDependencies["Dwellers"].keys()
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
        image = wx.Image(name =relative_textures_path + "dweller.jpg" )#"..\\..\\resources\\Textures\\dweller.jpg"
        self.texture_name = "dweller.jpg"
        image = image.Scale(32,32)
        self.imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))
        image_horizontal_sizer.Add(img_info_label)
        image_horizontal_sizer.AddSpacer(10)
        image_horizontal_sizer.Add(self.imageBitmap)
        image_horizontal_sizer.AddSpacer(10)
        image_horizontal_sizer.Add(img_selector_btn)
        between_lines_part_vertical_sizer.Add(image_horizontal_sizer, 0, wx.CENTER)
        between_lines_part_vertical_sizer.AddSpacer(10)

        ln = wx.StaticLine(self, -1)
        between_lines_part_vertical_sizer.Add(ln, 0, wx.EXPAND)
        between_lines_part_vertical_sizer.AddSpacer(10)

        self.resources_consumed_panel = NumberFillingChecker(self,
                                                             "Resource:",
                                                             "Consumed in quantity:",
                                                             "Consumed resources",
                                                             json_key="Consumes")

        between_lines_part_horizontal_sizer.Add(between_lines_part_vertical_sizer,0, wx.LEFT)
        log_area_label = wx.StaticText(self,-1,"Below lies logging area, showing error msgs")
        self.log_area = wx.TextCtrl(self, -1, size = (500,350), style=wx.TE_MULTILINE | wx.TE_READONLY)
        log_area_vertical_sizer.Add(log_area_label,0,wx.CENTER)
        log_area_vertical_sizer.Add(self.log_area, 0, wx.CENTER)
        log_area_vertical_sizer.AddSpacer(50)
        between_lines_part_horizontal_sizer.AddSpacer(50)

        separating_ln = wx.StaticLine(self, -1, style = wx.VERTICAL)
        between_lines_part_horizontal_sizer.Add(separating_ln, 0, wx.EXPAND)
        between_lines_part_horizontal_sizer.AddSpacer(50)

        between_lines_part_horizontal_sizer.Add(log_area_vertical_sizer,0,wx.RIGHT)
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
        for dwellerName in self.currentDependencies["Dwellers"].keys() + ["None"]:
            self.predecessorSelector.Append(dwellerName)
            self.successorSelector.Append(dwellerName)
        self.predecessorSelector.SetStringSelection("None")
        self.successorSelector.SetStringSelection("None")
        self.log_area.SetValue("")


    def mountSuccessAddMsg(self, dweller_name):
        return {"Log": "Successfully added " + dweller_name + " to dwellers list\n"}

    def mountSuccessEditMsg(self, dweller_name):
        return {"Log": "Successfully edited " + dweller_name + " dweller\n"}


    def setUpAddMode(self):
        print "Add mode"
        self.check_and_dump_name = self.checkAndDumpNameAddMode
        self.NameInput.SetValue("Dweller")
        self.NameInput.Enable()
        self.mount_exit_msg = self.mountSuccessAddMsg
        self.descriptionArea.SetValue("")

        self.texture_name = "dweller.jpg"
        image = wx.Image(relative_textures_path + self.texture_name) #"..\\..\\resources\\Textures\\"
        image = image.Scale(32,32)
        self.imageBitmap.SetBitmap(wx.BitmapFromImage(image))
        self.resources_consumed_panel.reset_init_mode = self.resources_consumed_panel.resetContentsInit_AddMode
        self.resources_consumed_panel.resetContents(None)


    def setUpEditMode(self, edit_element_name):
        print "Editing", edit_element_name
        self.check_and_dump_name = self.checkAndDumpNameEditMode
        self.NameInput.SetValue(edit_element_name)
        self.NameInput.Disable()
        self.mount_exit_msg = self.mountSuccessEditMsg
        self.descriptionArea.SetValue(self.currentDependencies["Dwellers"][edit_element_name]["Description"])

        self.texture_name = self.currentDependencies["Dwellers"][edit_element_name]["Texture path"]
        try:
            image = wx.Image(relative_textures_path + self.texture_name) #"..\\..\\resources\\Textures\\"
            image = image.Scale(32,32)
            self.imageBitmap.SetBitmap(wx.BitmapFromImage(image))
        except Exception:
            traceback.print_exc()

        self.resources_consumed_panel.reset_init_mode = self.resources_consumed_panel.resetContentsInit_EditMode
        self.resources_consumed_panel.resetContents(edit_element_name)
        successorVal = self.currentDependencies["Dwellers"][edit_element_name]["Successor"]
        successorVal = successorVal if successorVal in self.currentDependencies["Dwellers"].keys() else "None"
        predecessorVal = self.currentDependencies["Dwellers"][edit_element_name]["Predecessor"]
        predecessorVal = predecessorVal if predecessorVal in self.currentDependencies["Dwellers"].keys() else "None"
        self.successorSelector.SetStringSelection(successorVal)
        self.predecessorSelector.SetStringSelection(predecessorVal)

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
        result_struct["Result"]["Dweller\nName"] = self.NameInput.GetValue()
        return True

    def checkAndDumpNameAddMode(self,result_struct):
        dwellers_names = self.currentDependencies["Dwellers"].keys()
        dweller_name = self.NameInput.GetValue()
        if  re.sub(r'\s', "", dweller_name) == "":
            error_msg =  "-> Not a valid name\n"
            result_struct["ErrorMsg"] += error_msg
            return False
        if dweller_name in dwellers_names:
            error_msg ="-> Resource name already taken\n"
            result_struct["ErrorMsg"] += error_msg
            return False
        result_struct["Result"][Consts.DWELLER_NAME] = dweller_name
        return True

    def checkAndDumpPredAndSucc(self, result_struct):
        predecessor_name = self.predecessorSelector.GetStringSelection()
        successor_name = self.successorSelector.GetStringSelection()
        dweller_name = self.NameInput.GetValue()
        if successor_name == predecessor_name and successor_name != "None":
            result_struct["ErrorMsg"] += "-> Predecessor and Successor cannot be the same (both can be None though)\n"
            return False
        if successor_name == dweller_name :
            result_struct["ErrorMsg"] += "-> A dweller cannot be its own successor\n"
            return False
        if predecessor_name == dweller_name :
            result_struct["ErrorMsg"] += "-> A dweller cannot be its own predeccessor\n"
            return False
        result_struct["Result"][Consts.PREDECESSOR] = predecessor_name
        result_struct["Result"][Consts.SUCCESSOR] = successor_name
        return True

    def checkAndDumpDescriptionArea(self, result_struct):
        description_content = self.descriptionArea.GetValue()
        if re.sub(r'\s', "", description_content) == "":
            result_struct["ErrorMsg"] += "-> Please enter description of this dweller\n"
            return False
        result_struct["Result"][Consts.DESCRIPTION] = description_content
        return True


    def checkAndDumpTexture(self, result_struct):
        result_struct["Result"][Consts.TEXTURE_PATH] = self.texture_name
        return True

    def submit(self, event):
        correct = True
        result_struct = {"ErrorMsg":"Errors detected:\n", "Result":{}} # init error msg displayed if sth went wrong

        correct &= self.check_and_dump_name(result_struct)
        correct &= self.checkAndDumpPredAndSucc(result_struct)
        correct &= self.checkAndDumpDescriptionArea(result_struct)
        correct &= self.checkAndDumpTexture(result_struct)
        correct &= self.resources_consumed_panel.checkAndDumpCheckers(result_struct)

        if not correct:
            self.log_area.SetValue(result_struct["ErrorMsg"])
            return

        resources_names = self.currentDependencies["Resources"].keys()
        resource_name = self.NameInput.GetValue()
        resources_names.append(resource_name)
        result_msg = self.mount_exit_msg(resource_name)
        self.currentDependencies["Dwellers"][resource_name] = result_struct["Result"]
        print result_struct["Result"]
        print json.dumps(result_struct["Result"])
        self.frame.showPanel("main_panel", initDataForSearchedPanel=result_msg)


    def onImageSelected(self, event):
        dlg = wx.FileDialog(
            self,
            defaultDir= relative_textures_path,#"..\\..\\resources\\Textures\\",
            message="Choose an image",
            wildcard="*.png|*.jpg",
            style=wx.FD_OPEN
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            print "Filename:", dlg.GetFilename()
            image = wx.Image(path)
            image = image.Scale(32,32)
            self.imageBitmap.SetBitmap(wx.BitmapFromImage(image))

    def fillDepenendenciesPanelWithContent(self, content_dict):
        self.resetContents()
        try:
            pass
        except Exception:
            return False
        return True

    def onPredecessorSelected(self, event):
        pass

    def onSuccessorSelected(self, event):
        pass

    def checkDependenciesPanelsCorrectness(self):
        pass

    def moveToMainPanel(self,event):
        self.frame.showPanel("main_panel", initDataForSearchedPanel=None)