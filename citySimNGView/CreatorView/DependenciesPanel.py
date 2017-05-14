import wx

class DependenciesPanel(wx.Panel):
    def __init__(self, parent, rootSizer, partName, choices, frame, currentDependencies):
        wx.Panel.__init__(self, parent = parent)
        self.frame = frame

        self.currentDependencies = currentDependencies
        self.partName = partName
        self.choices = choices
        self.parent = parent

        vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.desc = wx.StaticText(self, label=partName)
        vertical_sizer.Add(self.desc)
        self.list_box = wx.ListBox(self, -1, size = (300,90), choices = choices)

        button_vertical_sizer = wx.BoxSizer(wx.VERTICAL)

        add_btn = wx.Button(self, size = (200,30), label = "add to " + partName)
        self.Bind(wx.EVT_BUTTON, self.onAdd, add_btn)

        edit_btn = wx.Button(self, size = (200, 30), label = "edit selected from " + partName)
        self.Bind(wx.EVT_BUTTON, self.onEdit, edit_btn)

        delete_btn = wx.Button(self, size = (200,30), label = "delete selected from " + partName)
        self.Bind(wx.EVT_BUTTON, self.onDelete, delete_btn)

        button_vertical_sizer.Add(add_btn)
        button_vertical_sizer.Add(edit_btn)
        button_vertical_sizer.Add(delete_btn)

        horizontal_sizer.Add(self.list_box)
        horizontal_sizer.Add(button_vertical_sizer)

        vertical_sizer.Add(horizontal_sizer)
        self.SetSizer(vertical_sizer)
        rootSizer.Add(self, 0, wx.CENTER)

    def onAdd(self,event):
        self.frame.showPanel(self.partName,initDataForSearchedPanel= None)

    def onDelete(self, event):
        index = self.list_box.GetSelection()
        if not index == -1:
            self.list_box.Delete(index)
            removed_element = self.choices[index]
            print "removing", removed_element
            self.choices.__delitem__(index)
            self.parent.logArea.SetValue("Successfully removed " + removed_element)
        else:
            self.parent.logArea.SetValue("Please, select element to be removed from " + self.partName + " first")

    def onEdit(self, event):
        index = self.list_box.GetSelection()
        if not index == -1:
            edited_element = self.choices[index]
            print "editing", edited_element
            edit_arg = {"Edit":edited_element}
            self.frame.showPanel(self.partName, initDataForSearchedPanel=edit_arg)
        else:
            self.parent.logArea.SetValue("Please, select element to be edited from " + self.partName + " first")