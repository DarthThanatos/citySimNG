import wx

class NumberFillingChecker(wx.Panel):
    def __init__(self, parent, size, choicesList, key_label_txt, value_desc_label_txt, intro_label_txt, rootSizer):
        wx.Panel.__init__(self, id = -1, parent = parent)
        self.choicesList = choicesList
        self.checked_choices = {choice:wx.CheckBox(self, -1, label = choice) for choice in choicesList}
        self.choices_values = {choice:wx.SpinCtrl(self, value='0', size=(60, -1), min=0, max=5000) for choice in choicesList}
        for choice in choicesList:
            self.choices_values[choice].Disable()
            self.Bind(wx.EVT_CHECKBOX, self.onCheck, self.checked_choices[choice])

        vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        intro_label = wx.StaticText(self, -1, intro_label_txt)
        vertical_sizer.Add(intro_label,0,wx.CENTER)
        vertical_sizer.AddSpacer(10)

        for choice in choicesList:
            horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
            key_label = wx.StaticText(self, -1, key_label_txt)
            value_label = wx.StaticText(self, -1, value_desc_label_txt)
            horizontalSizer.Add(key_label)
            horizontalSizer.AddSpacer(10)
            horizontalSizer.Add(self.checked_choices[choice])
            horizontalSizer.AddSpacer(10)
            horizontalSizer.Add(value_label)
            horizontalSizer.AddSpacer(10)
            horizontalSizer.Add(self.choices_values[choice])
            vertical_sizer.Add(horizontalSizer,0,wx.CENTER)
            vertical_sizer.AddSpacer(10)

        self.SetSizer(vertical_sizer)
        rootSizer.Add(self, 0, wx.CENTER)

    def onCheck(self, event):
        checker = event.GetEventObject()
        checked = checker.GetValue()
        choice = checker.GetLabel()
        if checked:
            self.choices_values[choice].Enable()
        else:
            self.choices_values[choice].Disable()