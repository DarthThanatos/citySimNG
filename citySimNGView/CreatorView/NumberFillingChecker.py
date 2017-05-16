import wx
from wx.lib.scrolledpanel import ScrolledPanel

class NumberFillingChecker(ScrolledPanel):
    def __init__(self, parent, size, currentDependencies, key_label_txt, value_desc_label_txt, intro_label_txt, rootSizer, json_key, part_name, dependencies_key = "Resources"):
        ScrolledPanel.__init__(self, id = -1, size = (500,100), parent = parent, style = wx.SIMPLE_BORDER)
        self.currentDependencies = currentDependencies
        self.dependencies_key = dependencies_key
        self.json_key = json_key
        self.key_label_txt = key_label_txt
        self.value_desc_label_txt = value_desc_label_txt
        self.intro_label_txt = intro_label_txt
        self.rootSizer = rootSizer
        self.part_name = part_name
        self.vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.reset_init_mode = self.resetContentsInit_AddMode
        self.fillWithEntries(None)
        self.SetSizer(self.vertical_sizer)
        self.rootSizer.Add(self, 0, wx.CENTER)
        self.rootSizer.AddSpacer(10)

    def resetContentsInit_AddMode(self,unused):
        choicesList = self.currentDependencies[self.dependencies_key].keys()
        self.checked_choices = {choice:wx.CheckBox(self, -1, label = choice) for choice in choicesList}
        self.choices_values = {choice:wx.SpinCtrl(self, value='0', size=(60, -1), min=0, max=5000) for choice in choicesList}
        for choice in choicesList:
            self.choices_values[choice].Disable()
            self.Bind(wx.EVT_CHECKBOX, self.onCheck, self.checked_choices[choice])

    def resetContentsInit_EditMode(self, edit_element_name):
        choicesList = self.currentDependencies[self.dependencies_key].keys()
        self.checked_choices = {choice:wx.CheckBox(self, -1, label = choice) for choice in choicesList}
        self.choices_values = {choice:wx.SpinCtrl(
                                                      self,
                                                      value='0',
                                                      size=(60, -1),
                                                      min=0,
                                                      max=5000
                                                  )
                                    for choice in choicesList
                               }
        for choice in choicesList:
            if choice not in self.currentDependencies[self.part_name][edit_element_name][self.json_key]:
                print choice, "not in choice list"
                self.choices_values[choice].Disable()
            else:
                print "enabling", choice
                value =  self.currentDependencies[self.part_name][edit_element_name][self.json_key][choice]
                self.checked_choices[choice].SetValue(True)
                self.choices_values[choice].Enable()
                self.choices_values[choice].SetValue(value)
            self.Bind(wx.EVT_CHECKBOX, self.onCheck, self.checked_choices[choice])

    def fillWithEntries(self, arg):
        self.vertical_sizer.Clear(True)
        self.reset_init_mode(arg)
        choicesList = self.currentDependencies[self.dependencies_key].keys()

        intro_label = wx.StaticText(self, -1, self.intro_label_txt)
        self.vertical_sizer.Add(intro_label,0,wx.CENTER)
        self.vertical_sizer.AddSpacer(10)

        for choice in choicesList:
            print choice
            horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
            key_label = wx.StaticText(self, -1, self.key_label_txt)
            value_label = wx.StaticText(self, -1, self.value_desc_label_txt)
            horizontalSizer.Add(key_label)
            horizontalSizer.AddSpacer(10)
            horizontalSizer.Add(self.checked_choices[choice])
            horizontalSizer.AddSpacer(10)
            horizontalSizer.Add(value_label)
            horizontalSizer.AddSpacer(10)
            horizontalSizer.Add(self.choices_values[choice])
            self.vertical_sizer.Add(horizontalSizer,0,wx.CENTER)
            self.vertical_sizer.AddSpacer(10)
        self.vertical_sizer.Layout()
        self.SetupScrolling()


    def onCheck(self, event):
        checker = event.GetEventObject()
        checked = checker.GetValue()
        choice = checker.GetLabel()
        if checked:
            self.choices_values[choice].Enable()
        else:
            self.choices_values[choice].Disable()

    def dumpDict(self):
        choicesList = self.currentDependencies[self.dependencies_key].keys()
        res = {self.json_key:{}}
        for choice in choicesList:
            if self.checked_choices[choice].GetValue():
                res[self.json_key][choice] = self.choices_values[choice]
        return res

    def checkAndDumpCheckers(self, result_struct):
        checkedChoices = 0
        result_struct["Result"][self.json_key] = {}
        for choice in self.currentDependencies[self.dependencies_key].keys():
            if self.checked_choices[choice].GetValue():
                result_struct["Result"][self.json_key][choice] = self.choices_values[choice].GetValue()
                checkedChoices += 1
        if checkedChoices == 0:
            result_struct["ErrorMsg"] += "-> Pick at least one element in the section \"" +\
                                         self.intro_label_txt +\
                                         "\". If there is nothing to choose there, consider creating some elements in other panels\n"
            return False
        return True

    def resetContents(self, arg):
        self.fillWithEntries(arg)

