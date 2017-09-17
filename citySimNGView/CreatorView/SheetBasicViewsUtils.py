from wx import wx

from CreatorView import Consts
from CreatorView.NumberFillingChecker import NumberFillingChecker
from CreatorView.RestorableView import RestorableNameInput, RestorableDescriptionArea, RestorableImageBmp, RestorableLogArea, RestorableStdSelector
from utils.ButtonsFactory import ButtonsFactory
from utils.RelativePaths import relative_textures_path


class SheetBasicViewsUtils(object):

    def __init__(self, sheet_view):
        self.sheet_view = sheet_view

    def addViewToRootSizerWithSpace(self, view, space = 0, alignment = wx.CENTER):
        self.sheet_view.rootSizer.Add(view,0,alignment)
        self.sheet_view.rootSizer.AddSpacer(space)

    def newBasicCharacteristicsVerticalSizer(self):
        basicCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        basicCharacteristicsVerticalSizer.Add(self.newDescriptionAreaVerticalSizer(),0,wx.CENTER)
        basicCharacteristicsVerticalSizer.AddSpacer(10)
        basicCharacteristicsVerticalSizer.Add(self.newPredecessorPickerHorizontalSizer(), 0, wx.CENTER)
        basicCharacteristicsVerticalSizer.AddSpacer(5)
        basicCharacteristicsVerticalSizer.Add(self.newSuccesorPickerHorizontalSizer(), 0, wx.CENTER)
        basicCharacteristicsVerticalSizer.AddSpacer(10)
        basicCharacteristicsVerticalSizer.Add(self.newEntityIconHorizontalSizer(), 0, wx.CENTER)
        basicCharacteristicsVerticalSizer.AddSpacer(10)
        return basicCharacteristicsVerticalSizer

    def initRootSizer(self, characteristicVerticalSizer, topPadding = 10):
        self.sheet_view.rootSizer = wx.BoxSizer(wx.VERTICAL)
        self.sheet_view.rootSizer.AddSpacer(topPadding)
        self.addViewToRootSizerWithSpace(self.newEntityNameHorizontalSizer(self.sheet_view.getEntityType()), 10)
        self.addViewToRootSizerWithSpace(self.newLine(), space= 10, alignment=wx.EXPAND)
        self.addViewToRootSizerWithSpace(self.newMainSheetPartHorizontalSizer(characteristicVerticalSizer))
        self.addViewToRootSizerWithSpace(self.newLine(), space=10, alignment=wx.EXPAND)
        self.addViewToRootSizerWithSpace(self.newButtonsPanelHorizontalSizer(self.sheet_view.submit), 75)
        self.sheet_view.SetSizer(self.sheet_view.rootSizer)
        self.sheet_view.rootSizer.SetDimension(0, 0, self.sheet_view.size[0], self.sheet_view.size[1])

    def newEntityNameHorizontalSizer(self, defaultName= None):
        entityNameHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        entityNameHorizontalSizer.Add(self.newNameFieldLabel(self.sheet_view.getEntityType()))
        entityNameHorizontalSizer.AddSpacer(5)
        entityNameHorizontalSizer.Add(self.newNameInput(defaultName if defaultName is not None else self.sheet_view.getEntityType()))
        return entityNameHorizontalSizer

    def newNameFieldLabel(self, entity_type):
         return wx.StaticText(self.sheet_view,-1, "Name of this " + entity_type)

    def newNameInput(self, defaultName):
        self.sheet_view.NameInput = wx.TextCtrl(self.sheet_view, -1, defaultName)
        self.sheet_view.restorableViews.append(RestorableNameInput(self.sheet_view, self.sheet_view.NameInput))
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
        self.sheet_view.restorableViews.append(RestorableLogArea(self.sheet_view, self.sheet_view.log_area))
        return self.sheet_view.log_area

    def newButtonsPanelHorizontalSizer(self, onSubmit):
        buttons_panel_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        buttons_panel_horizontal_sizer.Add(self.newCreateEntityButton(onSubmit))
        buttons_panel_horizontal_sizer.Add(self.newCancelButton(self.moveToMainPanel))
        return buttons_panel_horizontal_sizer

    def newCreateEntityButton(self, onSubmit):
        return ButtonsFactory().newButton(self.sheet_view, "Submit", onSubmit)

    def newCancelButton(self, onCancel):
        return ButtonsFactory().newButton(self.sheet_view, "Cancel", onCancel)

    def newDescriptionAreaVerticalSizer(self):
        descriptionAreaVerticalSizer =  wx.BoxSizer(wx.VERTICAL)
        descriptionAreaVerticalSizer.Add(self.newDescriptionFieldLabel(self.sheet_view.getEntityType()), 0, wx.CENTER)
        descriptionAreaVerticalSizer.Add(self.newDescriptionArea(), 0, wx.CENTER)
        return descriptionAreaVerticalSizer

    def newDescriptionFieldLabel(self, entity_type):
        return wx.StaticText(self.sheet_view, -1, "Description of " + entity_type + "for Tutorial module")

    def newDescriptionArea(self):
        self.sheet_view.descriptionArea = wx.TextCtrl(self.sheet_view, -1,size=(400, 200), style=wx.TE_MULTILINE)
        self.sheet_view.restorableViews.append(RestorableDescriptionArea(self.sheet_view, self.sheet_view.descriptionArea))
        return self.sheet_view.descriptionArea

    def newPredecessorPickerHorizontalSizer(self,):
        predecessor_picker_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        predecessor_picker_horizontal_sizer.Add(self.newPredeccesorLabel(self.sheet_view.getEntityType()))
        predecessor_picker_horizontal_sizer.AddSpacer(10)
        predecessor_picker_horizontal_sizer.Add(self.newPredecessorSelector())
        return predecessor_picker_horizontal_sizer

    def newSelector(self):
        return wx.ComboBox(self.sheet_view, choices=["None"], size = (125,-1), style=wx.CB_READONLY)

    def newPredecessorSelector(self):
        self.sheet_view.predecessorSelector = self.newSelector()
        self.sheet_view.restorableViews.append(
            RestorableStdSelector(self.sheet_view, self.sheet_view.predecessorSelector, Consts.PREDECESSOR)
        )
        return self.sheet_view.predecessorSelector

    def newSuccesorPickerHorizontalSizer(self):
        successor_picker_horizontal_sizer = wx.BoxSizer(wx.HORIZONTAL)
        successor_picker_horizontal_sizer.Add(self.newSuccesorLabel(self.sheet_view.getEntityType()))
        successor_picker_horizontal_sizer.AddSpacer(10)
        successor_picker_horizontal_sizer.Add(self.newSuccessorSelector())
        return successor_picker_horizontal_sizer

    def newSuccessorSelector(self):
        self.sheet_view.successorSelector = self.newSelector()
        self.sheet_view.restorableViews.append(
            RestorableStdSelector(self.sheet_view, self.sheet_view.successorSelector, Consts.SUCCESSOR)
        )
        return self.sheet_view.successorSelector

    def newPredeccesorLabel(self, entity_type):
        return wx.StaticText(self.sheet_view, -1, "Predecessor " + entity_type +":", size = (150, -1))

    def newSuccesorLabel(self,entity_type):
        return wx.StaticText(self.sheet_view, -1, "Successor " + entity_type + ":", size = (125,-1))

    def newEntityIconHorizontalSizer(self):
        entityIconHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        entityIconHorizontalSizer.Add(self.newImageInfoLabel())
        entityIconHorizontalSizer.AddSpacer(10)
        entityIconHorizontalSizer.Add(self.newEntityBmp())
        entityIconHorizontalSizer.AddSpacer(10)
        entityIconHorizontalSizer.Add(self.newImageSelectorButton())
        return entityIconHorizontalSizer

    def newImageInfoLabel(self):
        return wx.StaticText(self.sheet_view, -1, "Your texture: ")

    def newEntityBmp(self):
        self.sheet_view.imageBitmap = self.newScaledImgBitmap(relative_textures_path + "DefaultBuilding.jpg")
        self.sheet_view.restorableViews.append(RestorableImageBmp(self.sheet_view, self.sheet_view.imageBitmap))
        return self.sheet_view.imageBitmap

    def newScaledImg(self, non_relative_path):
        image = wx.Image(name = non_relative_path) #"..\\..\\resources\\Textures\\DefaultBuilding.jpg"
        return image.Scale(32,32)

    def newScaledImgBitmap(self, non_relative_path):
        return wx.StaticBitmap(self.sheet_view, wx.ID_ANY, wx.BitmapFromImage(self.newScaledImg(non_relative_path)), size = (32,32))

    def newImageSelectorButton(self):
        return ButtonsFactory().newButton(self.sheet_view, "Choose another texture", self.selectImage, size = (-1, 32))

    def selectImage(self, event):
        dlg = self.newImgDialog()
        self.onImageSelected(dlg)

    def newImgDialog(self):
        return wx.FileDialog(
            self.sheet_view,
            defaultDir= relative_textures_path, #"..\\..\\resources\\Textures\\",
            message="Choose an image",
            wildcard="*.png|*.jpg",
            style=wx.FD_OPEN
        )

    def onImageSelected(self, dlg):
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.sheet_view.entityIconRelativePath = dlg.GetFilename()
            self.sheet_view.imageBitmap.SetBitmap(wx.BitmapFromImage(self.newScaledImg(path)))

    def moveToMainPanel(self,event):
        self.sheet_view.frame.showPanel("main_panel",initDataForSearchedPanel=None)

    def setupMode(self, modeChecker, entity_name = None):
        self.sheet_view.sheetChecker = modeChecker
        for restorableView in self.sheet_view.restorableViews:
            restorableView.restoreView(entity_name)

    def newNumberFillingChecker(self, value_desc_label_txt, intro_label_txt, json_key):
        numberFillingChecker =  NumberFillingChecker(
            self.sheet_view,
            key_label_txt="Resource:",
            value_desc_label_txt=value_desc_label_txt,
            intro_label_txt=intro_label_txt,
            json_key=json_key
        )
        self.sheet_view.childrenCheckers.append(numberFillingChecker)
        return numberFillingChecker

    def newResourcesConsumedChecker(self):
        return self.newNumberFillingChecker(
            "Consumed in quantity:",
            "Consumed resources",
            Consts.CONSUMES
        )