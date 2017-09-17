from CreatorView import Consts


class SheetEntitiesUtils(object):

    def __init__(self,sheet_view):
        self.sheet_view = sheet_view

    def getEntityCharacteristic(self, edit_element_name, characteristic):
        return self.sheet_view.currentDependencies[self.sheet_view.sheet_name][edit_element_name][characteristic]

    def getSheetEntitiesNames(self):
        return self.sheet_view.currentDependencies[self.sheet_view.sheet_name].keys()

    def getEntityCharacteristicFromEntitiesSet(self, edit_element_name, characteristic):
        characteristic = self.getEntityCharacteristic(edit_element_name, characteristic)
        return characteristic if characteristic in self.getSheetEntitiesNames() else "None"

    def getAllDwellerEntities(self):
        return self.sheet_view.currentDependencies[Consts.DWELLERS].keys()