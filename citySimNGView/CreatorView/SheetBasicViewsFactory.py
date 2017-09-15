from wx import wx

from utils.ButtonsFactory import ButtonsFactory
from utils.RelativePaths import relative_textures_path


class SheetBasicViewsFactory(object):

    def __init__(self, sheet_view):
        self.sheet_view = sheet_view

    def newEntityNameHorizontalSizer(self, entity_type, defaultName= None):
        entityNameHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        entityNameHorizontalSizer.Add(self.newNameFieldLabel(entity_type))
        entityNameHorizontalSizer.AddSpacer(5)
        entityNameHorizontalSizer.Add(self.newNameInput(defaultName if defaultName != None else entity_type))
        return entityNameHorizontalSizer

    def newNameFieldLabel(self, entity_type):
         return wx.StaticText(self.sheet_view,-1, "Name of this " + entity_type)

    def newNameInput(self, defaultName):
        self.sheet_view.NameInput = wx.TextCtrl(self.sheet_view, -1, defaultName)
        return self.sheet_view.NameInput

    def newLine(self, style = wx.HORIZONTAL):
        return wx.StaticLine(self.sheet_view, -1, style = style)

    def newMainSheetPartHorizontalSizer(self, entityCharacteristicsVerticalSizer):
        mainSheetPartHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        mainSheetPartHorizontalSizer.Add(entityCharacteristicsVerticalSizer,0, wx.LEFT)
        mainSheetPartHorizontalSizer.AddSpacer(50)
        mainSheetPartHorizontalSizer.Add(self.newLine(wx.VERTICAL), 0, wx.EXPAND)
        mainSheetPartHorizontalSizer.AddSpacer(50)
        mainSheetPartHorizontalSizer.Add(self.newLogAreaVerticalSizer(),0,wx.RIGHT)
        return mainSheetPartHorizontalSizer

    def newLogAreaVerticalSizer(self):
        log_area_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        log_area_vertical_sizer.Add(self.newLogAreaLabel(),0,wx.CENTER)
        log_area_vertical_sizer.Add(self.newLogArea(), 0, wx.CENTER)
        log_area_vertical_sizer.AddSpacer(50)
        return log_area_vertical_sizer

    def newLogAreaLabel(self):
        return wx.StaticText(self.sheet_view,-1,"Below lies logging area, showing error msgs")

    def newLogArea(self):
        self.sheet_view.log_area = wx.TextCtrl(self.sheet_view, -1, size = (500,350), style=wx.TE_MULTILINE | wx.TE_READONLY)
        return self.sheet_view.log_area

    def newButtonsPanelHorizontalSizer(self, onSubmit, onCancel):
        buttons_panel_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_panel_horizontal_sizer.Add(self.newCreateEntityButton(onSubmit))
        buttons_panel_horizontal_sizer.Add(self.newCancelButton(onCancel))
        return buttons_panel_horizontal_sizer

    def newCreateEntityButton(self, onSubmit):
        return ButtonsFactory().newButton(self.sheet_view, "Submit", onSubmit)

    def newCancelButton(self, onCancel):
        return ButtonsFactory().newButton(self.sheet_view, "Cancel", onCancel)

    def newDescriptionAreaVerticalSizer(self, entity_type):
        descriptionAreaVerticalSizer =  wx.BoxSizer(wx.VERTICAL)
        descriptionAreaVerticalSizer.Add(self.newDescriptionFieldLabel(entity_type), 0, wx.CENTER)
        descriptionAreaVerticalSizer.Add(self.newDescriptionArea(), 0, wx.CENTER)
        return descriptionAreaVerticalSizer

    def newDescriptionFieldLabel(self, entity_type):
        return wx.StaticText(self.sheet_view, -1, "Description of " + entity_type + "for Tutorial module")

    def newDescriptionArea(self):
        self.sheet_view.descriptionArea = wx.TextCtrl(self.sheet_view, -1,size=(400, 200), style=wx.TE_MULTILINE)
        return self.sheet_view.descriptionArea

    def newPredecessorPickerHorizontalSizer(self,entity_type):
        predecessor_picker_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        predecessor_picker_horizontal_sizer.Add(self.newPredeccesorLabel(entity_type))
        predecessor_picker_horizontal_sizer.AddSpacer(10)
        predecessor_picker_horizontal_sizer.Add(self.newPredecessorSelector())
        return predecessor_picker_horizontal_sizer

    def newSelector(self):
        return wx.ComboBox(self.sheet_view, choices=["None"], size = (125,-1), style=wx.CB_READONLY)

    def newPredecessorSelector(self):
        self.sheet_view.predecessorSelector = self.newSelector()
        return self.sheet_view.predecessorSelector

    def newSuccesorPickerHorizontalSizer(self, entity_type):
        successor_picker_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        successor_picker_horizontal_sizer.Add(self.newSuccesorLabel(entity_type))
        successor_picker_horizontal_sizer.AddSpacer(10)
        successor_picker_horizontal_sizer.Add(self.newSuccessorSelector())
        return successor_picker_horizontal_sizer

    def newSuccessorSelector(self):
        self.sheet_view.successorSelector = self.newSelector()
        return self.sheet_view.successorSelector

    def newPredeccesorLabel(self, entity_type):
        return wx.StaticText(self.sheet_view, -1, "Predecessor " + entity_type +":", size = (150, -1))

    def newSuccesorLabel(self,entity_type):
        return wx.StaticText(self.sheet_view, -1, "Successor " + entity_type + ":", size = (125,-1))

    def newEntityIconHorizontalSizer(self, onImgBtnClicked):
        entityIconHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        entityIconHorizontalSizer.Add(self.newImageInfoLabel())
        entityIconHorizontalSizer.AddSpacer(10)
        entityIconHorizontalSizer.Add(self.newEntityBmp())
        entityIconHorizontalSizer.AddSpacer(10)
        entityIconHorizontalSizer.Add(self.newImageSelectorButton(onImgBtnClicked))
        return entityIconHorizontalSizer

    def newImageInfoLabel(self):
        return wx.StaticText(self.sheet_view, -1, "Your texture: ")

    def newEntityBmp(self):
        self.sheet_view.imageBitmap = self.newScaledImgBitmap(relative_textures_path + "DefaultBuilding.jpg")
        return self.sheet_view.imageBitmap

    def newScaledImg(self, non_relative_path):
        image = wx.Image(name = non_relative_path) #"..\\..\\resources\\Textures\\DefaultBuilding.jpg"
        return image.Scale(32,32)

    def newScaledImgBitmap(self, non_relative_path):
        return wx.StaticBitmap(self.sheet_view, wx.ID_ANY, wx.BitmapFromImage(self.newScaledImg(non_relative_path)), size = (32,32))

    def newImageSelectorButton(self, onImgBtnClicked):
        return ButtonsFactory().newButton(self.sheet_view, "Choose another texture", onImgBtnClicked, size = (-1, 32))