from wx import wx

from CreatorView import Consts
from CreatorView.RelativePaths import relative_textures_path


class RestorableView(object):

    def __init__(self, sheet_view):
        self.sheet_view = sheet_view

    def restoreView(self, entity_name=None):
        raise Exception("restoreView not implemented")

    def getEntityCharacteristic(self, edit_element_name, characteristic):
        return self.sheet_view.currentDependencies[self.sheet_view.sheet_name][edit_element_name][characteristic]

    def getSheetEntitiesNames(self):
        return self.sheet_view.currentDependencies[self.sheet_view.sheet_name].keys()

    def getEntityCharacteristicFromEntitiesSet(self, edit_element_name, characteristic):
        characteristic = self.getEntityCharacteristic(edit_element_name, characteristic)
        return characteristic if characteristic in self.getSheetEntitiesNames() else "None"

    def newScaledImg(self, non_relative_path):
        image = wx.Image(name = non_relative_path) #"..\\..\\resources\\Textures\\DefaultBuilding.jpg"
        return image.Scale(32,32)

    def clearSelector(self, selector, stringSelection="None", selectionList = None):
        selector.Clear()
        selectionList = self.getSheetEntitiesNames() + ["None"] if selectionList is None else selectionList
        for entityName in selectionList:
            selector.Append(entityName)
        selector.SetStringSelection(stringSelection)

class RestorableNameInput(RestorableView):

    def __init__(self, sheet_view, NameInput):
        super(RestorableNameInput, self).__init__(sheet_view)
        self.sheet_view = sheet_view
        self.NameInput = NameInput

    def restoreView(self, entity_name = None):
        self.NameInput.SetValue(entity_name if entity_name != None else self.sheet_view.getEntityType())
        self.NameInput.Enable(entity_name == None)


class RestorableDescriptionArea(RestorableView):

    def __init__(self, sheet_view, descriptionArea):
        super(RestorableDescriptionArea, self).__init__(sheet_view)
        self.descriptionArea = descriptionArea

    def restoreView(self, entity_name = None):
        descriptionAreaValue = \
            self.getEntityCharacteristic(entity_name, Consts.DESCRIPTION) if entity_name is not None else ""
        self.descriptionArea.SetValue(descriptionAreaValue)

class RestorableImageBmp(RestorableView):

    def __init__(self, sheet_view, imageBitmap):
        super(RestorableImageBmp, self).__init__(sheet_view)
        self.imageBitmap = imageBitmap

    def restoreView(self, entity_name=None):
        self.sheet_view.entityIconRelativePath  = \
            self.sheet_view.getDefaultIconRelativePath() if entity_name is None \
                else self.getEntityCharacteristic(entity_name, Consts.TEXTURE_PATH)
        self.imageBitmap.SetBitmap(
            wx.BitmapFromImage(
                self.newScaledImg(relative_textures_path + self.sheet_view.entityIconRelativePath)
            )
        )

class RestorableSelector(RestorableView):

    def __init__(self, sheet_view, selector, key):
        super(RestorableSelector, self).__init__(sheet_view)
        self.selector = selector
        self.key = key

    def restoreView(self, entity_name=None):
        stringSelection = \
            self.getEntityCharacteristicFromEntitiesSet(entity_name, self.key) if entity_name is not None else "None"
        self.clearSelector(self.selector, stringSelection)

class RestorableLogArea(RestorableView):

    def __init__(self, sheet_view, log_area):
        super(RestorableLogArea, self).__init__(sheet_view)
        self.log_area = log_area

    def restoreView(self, entity_name=None):
        self.log_area.SetValue("")

class RestorableStartIncomePicker(RestorableView):

    def __init__(self, sheet_view, start_income_picker):
        super(RestorableStartIncomePicker, self).__init__(sheet_view)
        self.start_income_picker = start_income_picker

    def restoreView(self, entity_name=None):
        startIncomePickerValue = \
            int(self.getEntityCharacteristic(entity_name, Consts.START_INCOME)) if entity_name is not None else 0
        self.start_income_picker.SetValue(startIncomePickerValue)

class RestorableDwellersAmount(RestorableView):

    def __init__(self, sheet_view, dwellers_amount):
        super(RestorableDwellersAmount, self).__init__(sheet_view)
        self.dwellers_amount = dwellers_amount

    def restoreView(self, entity_name=None):
        dwellersAmount = \
            int(self.getEntityCharacteristic(entity_name, Consts.DWELLERS_AMOUNT))\
                if entity_name is not None else 0
        self.dwellers_amount.SetValue(dwellersAmount)

class RestorableTypeOfBuilding(RestorableView):

    def __init__(self, sheet_view, type_of_building_selector):
        super(RestorableTypeOfBuilding, self).__init__(sheet_view)
        self.type_of_building_selector = type_of_building_selector

    def restoreView(self, entity_name=None):
        typeOfBuilding = \
            self.getEntityCharacteristic(entity_name, Consts.TYPE) \
                if entity_name is not None else "Industrial"
        self.type_of_building_selector.SetStringSelection(typeOfBuilding)

