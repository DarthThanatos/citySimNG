import wx
from wx.lib.scrolledpanel import ScrolledPanel
from LogMessages import CHECKER_PANEL_ERROR_MSG

class NumberFillingChecker(ScrolledPanel):
    def __init__(self, parent, size, currentDependencies, key_label_txt, value_desc_label_txt, intro_label_txt, parentSizer, json_key, part_name, dependencies_key ="Resources"):
        ScrolledPanel.__init__(self, id = -1, size = (500,100), parent = parent, style = wx.SIMPLE_BORDER)
        self.currentDependencies = currentDependencies
        self.dependencies_key = dependencies_key
        self.json_key = json_key
        self.key_label_txt = key_label_txt
        self.value_desc_label_txt = value_desc_label_txt
        self.intro_label_txt = intro_label_txt
        self.parentSizer = parentSizer
        self.part_name = part_name
        self.reset_init_mode = self.resetContentsInit_AddMode
        
        self.initRootSizer()
        self.fillWithEntries(None)

        self.parentSizer.Add(self, 0, wx.CENTER)
        self.parentSizer.AddSpacer(10)

    def initRootSizer(self):
        self.rootSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.rootSizer)

    def getChoicesList(self):
        return self.currentDependencies[self.dependencies_key].keys()

    def newChoicesValuesSpinners(self):
       self.choices_values = {choice:wx.SpinCtrl(self, value='0', size=(60, -1), min=0, max=5000) for choice in self.getChoicesList()}
       for choice_value in self.choices_values.values():choice_value.Disable()
       return self.choices_values

    def newChoicesCheckBoxes(self):
        self.checked_choices = {choice:wx.CheckBox(self, -1, label = choice) for choice in self.getChoicesList()}
        for check_box in self.checked_choices.values() : self.Bind(wx.EVT_CHECKBOX, self.onBoxChecked, check_box)
        return self.checked_choices

    def init_choices(self):
        self.newChoicesCheckBoxes()
        self.newChoicesValuesSpinners()

    def resetContentsInit_AddMode(self,unused):
        self.init_choices()

    def getChoicesDict(self, edit_element_name):
        return self.currentDependencies[self.part_name][edit_element_name][self.json_key]

    def getAlreadySelectedChoicesNames(self, edit_element_name):
        return filter(lambda x: x in self.getChoicesDict(edit_element_name) , self.getChoicesList())

    def restoreChoiceSpinner(self, edit_element_name, choice):
        value =  self.getChoicesDict(edit_element_name)[choice]
        self.choices_values[choice].Enable()
        self.choices_values[choice].SetValue(value)

    def restoreChoiceCheckBox(self, choice):
        self.checked_choices[choice].SetValue(True)

    def onChoiceAlreadySelected(self, edit_element_name, choice):
        self.restoreChoiceCheckBox(choice)
        self.restoreChoiceSpinner(edit_element_name, choice)

    def resetContentsInit_EditMode(self, edit_element_name):
        self.init_choices()
        for choice in self.getAlreadySelectedChoicesNames(edit_element_name):
            self.onChoiceAlreadySelected(edit_element_name, choice)

    def newChoiceHorizontalSizer(self, choice):
        choiceHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        choiceHorizontalSizer.Add(wx.StaticText(self, -1, self.key_label_txt))
        choiceHorizontalSizer.AddSpacer(10)
        choiceHorizontalSizer.Add(self.checked_choices[choice])
        choiceHorizontalSizer.AddSpacer(10)
        choiceHorizontalSizer.Add(wx.StaticText(self, -1, self.value_desc_label_txt))
        choiceHorizontalSizer.AddSpacer(10)
        choiceHorizontalSizer.Add(self.choices_values[choice])
        return choiceHorizontalSizer

    def fillWithEntries(self, arg):
        self.reset_init_mode(arg)
        self.reinitRootSizer()
        self.SetupScrolling()

    def reinitRootSizer(self):
        self.rootSizer.Clear(True)
        self.rootSizer.Add(wx.StaticText(self, -1, self.intro_label_txt), 0, wx.CENTER)
        self.rootSizer.AddSpacer(10)
        for choice in self.getChoicesList():
            self.rootSizer.Add(self.newChoiceHorizontalSizer(choice), 0, wx.CENTER)
            self.rootSizer.AddSpacer(10)
        self.rootSizer.Layout()

    def onBoxChecked(self, event):
        self.choices_values[event.GetEventObject().GetLabel()].Enable(event.GetEventObject().GetValue())

    def getCheckedChoicesNamesList(self):
        return filter(lambda x: self.checked_choices[x].GetValue(), self.getChoicesList())

    def getChoiceValue(self, choice):
        return self.choices_values[choice].GetValue()

    def checkAndDumpCheckers(self, result_struct):
        at_least_one_checked = self.getCheckedChoicesNamesList().__len__() != 0
        result_struct["Result"][self.json_key] = {choice : self.getChoiceValue(choice) for choice in self.getCheckedChoicesNamesList()}
        result_struct["ErrorMsg"] += CHECKER_PANEL_ERROR_MSG.format(self.intro_label_txt) if not at_least_one_checked else ""
        return at_least_one_checked

    def resetContents(self, arg):
        self.fillWithEntries(arg)

