import wx
import re
from wx.lib.scrolledpanel import ScrolledPanel
from RelativePaths import relative_textures_path

class ResourcesPanel(ScrolledPanel):
    def __init__(self,parent, size, frame, currentDependencies, lists_of_names):
        ScrolledPanel.__init__(self, size = size, parent = parent, style = wx.SIMPLE_BORDER)
        self.SetupScrolling()
        self.wakeUpData = None

        self.lists_of_names = lists_of_names
        self.frame = frame
        self.currentDependencies = currentDependencies

        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        res_name_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        predecessor_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        successor_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        image_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        start_income_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.NameLabel = wx.StaticText(self,-1, "Name of this resource")
        self.NameInput = wx.TextCtrl(self, -1, "Resource")
        res_name_horizontal_sizer.Add(self.NameLabel)
        res_name_horizontal_sizer.AddSpacer(5)
        res_name_horizontal_sizer.Add(self.NameInput)
        vertical_sizer.AddSpacer(75)

        vertical_sizer.Add(res_name_horizontal_sizer, 0, wx.CENTER)
        vertical_sizer.AddSpacer(10)
        header_ln = wx.StaticLine(self, -1)
        vertical_sizer.Add(header_ln, 0, wx.EXPAND)
        vertical_sizer.AddSpacer(10)

        descriptionFieldLabel = wx.StaticText(self, -1, "Description of Resource for Tutorial module")
        vertical_sizer.Add(descriptionFieldLabel, 0, wx.CENTER)
        self.descriptionArea = wx.TextCtrl(self, -1,size=(400, 200), style=wx.TE_MULTILINE)
        vertical_sizer.Add(self.descriptionArea, 0, wx.CENTER)
        vertical_sizer.AddSpacer(10)

        predecessor_label = wx.StaticText(self, -1, "Predecessor resource:", size = (125, -1))
        predecessorChoiceList = ["None"] + self.lists_of_names[1]
        self.predecessorSelector = wx.ComboBox(self, choices=predecessorChoiceList, style=wx.CB_READONLY)
        self.predecessorSelector.Bind(wx.EVT_COMBOBOX, self.onPredecessorSelected)
        predecessor_horizontal_sizer.Add(predecessor_label)
        predecessor_horizontal_sizer.AddSpacer(10)
        predecessor_horizontal_sizer.Add(self.predecessorSelector)
        vertical_sizer.Add(predecessor_horizontal_sizer, 0, wx.CENTER)
        vertical_sizer.AddSpacer(5)

        successor_label = wx.StaticText(self, -1, "Successor resource:", size = (125,-1))
        successorChoiceList = ["None"] + self.lists_of_names[1]
        self.successorSelector = wx.ComboBox(self, choices=successorChoiceList, style=wx.CB_READONLY)
        self.successorSelector.Bind(wx.EVT_COMBOBOX, self.onSuccessorSelected)
        successor_horizontal_sizer.Add(successor_label)
        successor_horizontal_sizer.AddSpacer(10)
        successor_horizontal_sizer.Add(self.successorSelector)
        vertical_sizer.Add(successor_horizontal_sizer, 0, wx.CENTER)
        vertical_sizer.AddSpacer(10)

        img_info_label = wx.StaticText(self, -1, "Your texture: ")
        img_selector_btn = wx.Button(self, -1, label = "Choose another texture", size = (-1, 32))
        self.Bind(wx.EVT_BUTTON, self.onImageSelected ,img_selector_btn)
        image = wx.Image(name = "..\\..\\resources\\Textures\\DefaultBuilding.jpg")
        self.imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))
        image_horizontal_sizer.Add(img_info_label)
        image_horizontal_sizer.AddSpacer(10)
        image_horizontal_sizer.Add(self.imageBitmap)
        image_horizontal_sizer.AddSpacer(10)
        image_horizontal_sizer.Add(img_selector_btn)
        vertical_sizer.Add(image_horizontal_sizer, 0, wx.CENTER)
        vertical_sizer.AddSpacer(10)

        start_income_label = wx.StaticText(self, -1, "StartIncome: ")
        self.start_income =  wx.SpinCtrl(self, value='0', size=(60, -1), min=0, max = 5000)
        start_income_sizer.Add(start_income_label)
        start_income_sizer.AddSpacer(10)
        start_income_sizer.Add(self.start_income)
        vertical_sizer.Add(start_income_sizer, 0, wx.CENTER)
        vertical_sizer.AddSpacer(10)

        bottom_ln = wx.StaticLine(self, -1)
        vertical_sizer.Add(bottom_ln, 0, wx.EXPAND)
        vertical_sizer.AddSpacer(10)

        main_panel_btn = wx.Button(self, label="Main Panel")
        self.Bind(wx.EVT_BUTTON, self.moveToMainPanel, main_panel_btn)
        create_resource_btn = wx.Button(self, label = "Submit")
        self.Bind(wx.EVT_BUTTON, self.submit, create_resource_btn)

        buttons_horizontal_sizer.Add(create_resource_btn)
        buttons_horizontal_sizer.Add(main_panel_btn)
        vertical_sizer.Add(buttons_horizontal_sizer, 0, wx.CENTER, 5)

        self.SetSizer(vertical_sizer)
        vertical_sizer.SetDimension(0, 0, size[0], size[1])
        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def onImageSelected(self, event):
        dlg = wx.FileDialog(
            self,
            defaultDir="..\\..\\resources\\Textures\\",
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

    def onPredecessorSelected(self, event):
        pass

    def onSuccessorSelected(self, event):
        pass

    def onShow(self, event):
        if event.GetShow():
            if not self.wakeUpData == None:
                try:
                    edit_element = self.wakeUpData["Edit"]
                    print "Editing", edit_element
                except:
                    pass
                self.wakeUpData = None

    def submit(self, event):
        resources_names = self.lists_of_names[1]
        resource_name = self.NameInput.GetValue()
        if not re.sub(r'\s', "", resource_name) == "":
            resources_names.append(resource_name)
            result_msg = {"Log":"Successfully added " + resource_name + " to resources list"}
            self.frame.showPanel("main_panel", initDataForSearchedPanel=result_msg)
        else:
            print "Not a valid name"

    def resetContents(self):
        pass

    def checkDependenciesPanelsCorrectness(self):
        pass

    def fillDepenendenciesPanelWithContent(self, content_dict):
        self.resetContents()
        try:
            pass
        except Exception:
            return False
        return True

    def moveToMainPanel(self,event):
        self.frame.showPanel("main_panel",initDataForSearchedPanel=None)
