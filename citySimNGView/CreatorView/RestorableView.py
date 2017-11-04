from wx import wx

from CreatorView import Consts, CreatorConfig
from CreatorView.RelativePaths import relative_textures_path
from utils.FileExistanceChecker import FileExistanceChecker
from utils.SheetEntitiesUtils import SheetEntitiesUtils


class RestorableView(object):

    def __init__(self, sheet_view):
        self.sheet_view = sheet_view
        self.entityUtils = SheetEntitiesUtils(sheet_view)

    def restoreView(self, entity_name=None):
        raise Exception("restoreView not implemented")

class RestorableNameInput(RestorableView):

    def __init__(self, sheet_view, NameInput):
        super(RestorableNameInput, self).__init__(sheet_view)
        self.sheet_view = sheet_view
        self.NameInput = NameInput

    def restoreView(self, entity_name = None):
        self.NameInput.SetValue(
            entity_name if entity_name != None else self.sheet_view.getEntityType()
        )
        self.NameInput.Enable(entity_name == None)


class RestorableDescriptionArea(RestorableView):

    def __init__(self, sheet_view, descriptionArea):
        super(RestorableDescriptionArea, self).__init__(sheet_view)
        self.descriptionArea = descriptionArea

    def restoreView(self, entity_name = None):
        descriptionAreaValue = \
            self.entityUtils.getEntityCharacteristic(entity_name, Consts.DESCRIPTION) \
                if entity_name is not None else ""
        self.descriptionArea.SetValue(descriptionAreaValue)

class RestorableImageBmp(RestorableView):

    def __init__(self, sheet_view, imageBitmap):
        super(RestorableImageBmp, self).__init__(sheet_view)
        self.imageBitmap = imageBitmap

    def newScaledImg(self, non_relative_path):
        image = wx.Image(name = non_relative_path) #"..\\..\\resources\\Textures\\DefaultBuilding.jpg"
        return image.Scale(32,32)

    def restoreView(self, entity_name=None):
        self.sheet_view.entityIconRelativePath  = \
            self.sheet_view.getDefaultIconRelativePath() if entity_name is None \
                else self.entityUtils.getEntityCharacteristic(entity_name, Consts.TEXTURE_PATH)
        actual_file_name =\
            self.sheet_view.entityIconRelativePath \
                if FileExistanceChecker().checkIfGraphicalFileExists(self.sheet_view.entityIconRelativePath) \
                else CreatorConfig.PANEL_TEXURE_DEFAULT_NAME
        self.imageBitmap.SetBitmap(
            wx.BitmapFromImage(
                self.newScaledImg(relative_textures_path + actual_file_name)
            )
        )

class RestorableSelector(RestorableView):

    def __init__(self, sheet_view, selector, restoreKey):
        super(RestorableSelector, self).__init__(sheet_view)
        self.selector = selector
        self.restoreKey = restoreKey

    def getSelectionList(self):
        raise Exception("getSelectionList not implemented")

    def clearSelector(self, selector, stringSelection="None"):
        selector.Clear()
        selectionList = self.getSelectionList() + ["None"]
        for entityName in selectionList:
            selector.Append(entityName)
        selector.SetStringSelection(stringSelection)

    def restoreView(self, entity_name=None):
        stringSelection = \
            self.entityUtils.getEntityCharacteristic(entity_name, self.restoreKey) \
                if entity_name is not None else "None"
        self.clearSelector(self.selector, stringSelection)

class RestorableStdSelector(RestorableSelector):

    def getSelectionList(self):
        return self.entityUtils.getSheetEntitiesNames()

class RestorableDwellersNamesSelector(RestorableSelector):

    def getSelectionList(self):
        return SheetEntitiesUtils(self.sheet_view).getAllDwellerEntities()

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
        try:
            startIncomePickerValue = \
                int(self.entityUtils.getEntityCharacteristic(entity_name, Consts.START_INCOME)) \
                    if entity_name is not None else 0
        except Exception:
            startIncomePickerValue = 0
        self.start_income_picker.SetValue(startIncomePickerValue)

class RestorableDwellersAmount(RestorableView):

    def __init__(self, sheet_view, dwellers_amount):
        super(RestorableDwellersAmount, self).__init__(sheet_view)
        self.dwellers_amount = dwellers_amount

    def restoreView(self, entity_name=None):
        dwellersAmount = \
            int(self.entityUtils.getEntityCharacteristic(entity_name, Consts.DWELLERS_AMOUNT))\
                if entity_name is not None else 0
        self.dwellers_amount.SetValue(dwellersAmount)

class RestorableTypeOfBuilding(RestorableView):

    def __init__(self, sheet_view, type_of_building_selector):
        super(RestorableTypeOfBuilding, self).__init__(sheet_view)
        self.type_of_building_selector = type_of_building_selector

    def restoreView(self, entity_name=None):
        typeOfBuilding = \
            self.entityUtils.getEntityCharacteristic(entity_name, Consts.TYPE) \
                if entity_name is not None else "Industrial"
        if typeOfBuilding not in ["Industrial", "Domestic"]: typeOfBuilding = ""
        self.type_of_building_selector.SetStringSelection(typeOfBuilding)