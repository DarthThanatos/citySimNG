import wx

from utils.ButtonsFactory import ButtonsFactory


class DependenciesSubPanel(wx.Panel):
    def __init__(self, parent, partName, choices, frame, currentDependencies):
        wx.Panel.__init__(self, parent = parent)
        self.frame = frame
        self.currentDependencies = currentDependencies
        self.partName = partName
        self.choices = choices
        self.parent = parent
        self.partName = partName
        self.initRootSizer()

    def newDescription(self):
        self.desc = wx.StaticText(self, label=self.partName)
        return self.desc

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self.newDescription())
        rootSizer.Add(self.newHorizontalSizer())
        self.SetSizer(rootSizer)

    def newEntitiesNamesListBox(self):
        self.entities_names_listbox = wx.ListBox(self, -1, size = (300, 90), choices = self.choices)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.onEdit, self.entities_names_listbox)
        return self.entities_names_listbox

    def newHorizontalSizer(self):
        self.horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontal_sizer.Add(self.newEntitiesNamesListBox())
        self.horizontal_sizer.Add(self.newButtonsVerticalSizer())
        return self.horizontal_sizer

    def newButtonsVerticalSizer(self):
        self.button_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        self.button_vertical_sizer.Add(self.newAddButton())
        self.button_vertical_sizer.Add(self.newEditButton())
        self.button_vertical_sizer.Add(self.newDeleteButton())
        return self.button_vertical_sizer

    def newAddButton(self):
        self.add_btn = ButtonsFactory().newButton(self, "add to " + self.partName, self.onAdd, size = (200,30))
        return self.add_btn

    def newEditButton(self):
        self.edit_btn = ButtonsFactory().newButton(self, "edit selected from " + self.partName, self.onEdit, size = (200,30))
        return self.edit_btn

    def newDeleteButton(self):
        self.delete_btn = ButtonsFactory().newButton(self, "delete selected from " + self.partName, self.onDelete, size = (200,30))
        return self.delete_btn

    def resetContents(self):
        self.entities_names_listbox.Clear()
        for choice in self.currentDependencies[self.partName].keys(): self.entities_names_listbox.Append(choice)

    def onAdd(self,event):
        self.frame.showPanel(self.partName,initDataForSearchedPanel= None)

    def onDelete(self, event):
        index = self.entities_names_listbox.GetSelection()
        if not index == -1: self.onDeleteItemSelected(index)
        else: self.onDeleteItemNotSelected()
        self.parent.resetContents()

    def onDeleteItemNotSelected(self):
        self.parent.logArea.SetValue("Please, select element to be removed from " + self.partName + " first")

    def onDeleteItemSelected(self, index):
        removed_element = self.entities_names_listbox.GetStringSelection()
        self.entities_names_listbox.Delete(index)
        self.currentDependencies[self.partName].__delitem__(removed_element)
        self.parent.logArea.SetValue("Successfully removed " + removed_element)

    def onEdit(self, event):
        edited_element = self.entities_names_listbox.GetStringSelection()
        if not edited_element == "": self.onEditedItemSelected(edited_element)
        else: self.onEditedItemNotSelected()

    def onEditedItemSelected(self, edited_element):
        edit_arg = {"Edit": edited_element}
        self.frame.showPanel(self.partName, initDataForSearchedPanel=edit_arg)

    def onEditedItemNotSelected(self):
        self.parent.logArea.SetValue("Please, select element to be edited from " + self.partName + " first")