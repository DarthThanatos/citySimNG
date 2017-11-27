import re
from CreatorView import Consts
from utils.FileExistanceChecker import FileExistanceChecker

ADD_MODE = "Add mode"
EDIT_MODE = "Edit mode"

class SheetEntityChecker(object):

    def __init__(self, sheet_view):
        self.sheet_view = sheet_view

    def checkAndDumpName(self, result_struct):
        raise Exception("checkAndDumpName not implemented")

    def newSuccessExitMsg(self, entity_name):
        raise Exception("newExitMsg not implemented")

    def getMode(self):
        raise Exception("getMode not implemented")

    def newResultStruct(self):
        return {"ErrorMsg":"Errors detected:\n", "Result":{}} # init error msg displayed if sth went wrong

    def onCheck(self, entityChecker):
        entityChecker.onCheck(self, self.newResultStruct())

    def onCorrectnessCheckFinished(self, correct, result_struct):
        if not correct:
            self.sheet_view.log_area.SetValue(result_struct["ErrorMsg"])
            return
        self.onSheetCorrectlyFilled(result_struct)

    def getAllSheetEntitieNames(self):
        return self.sheet_view.currentDependencies[self.sheet_view.sheet_name].keys()

    def getEntityName(self):
        return self.sheet_view.NameInput.GetValue()

    def onSheetCorrectlyFilled(self, result_struct):
        self.sheet_view.currentDependencies[self.sheet_view.sheet_name][self.getEntityName()] = result_struct["Result"]
        self.sheet_view.frame.showPanel("main_panel", initDataForSearchedPanel=self.newSuccessExitMsg(self.getEntityName()))

    def getPredecessorName(self):
        return self.sheet_view.predecessorSelector.GetStringSelection()

    def getSuccessorName(self):
        return self.sheet_view.successorSelector.GetStringSelection()

    def successorCorrect(self, result_struct):
        if not self.getSuccessorName() in (self.getAllSheetEntitieNames()  + ["None"]):
            result_struct["ErrorMsg"] += "-> Successor must be one of " + self.sheet_view.sheet_name + "\n"
            return False
        return True


    def predecessorCorrect(self, result_struct):
        if not self.getPredecessorName() in (self.getAllSheetEntitieNames() + ["None"]):
            result_struct["ErrorMsg"] += "-> Predecessor must be one of " + self.sheet_view.sheet_name + "\n"
            return False
        return True

    def checkAndDumpPredAndSucc(self, result_struct):
        correct = self.successorCorrect(result_struct)
        correct &= self.predecessorCorrect(result_struct)
        if correct: self.onSuccAndPredCheckCorrect(result_struct)
        return correct

    def onSuccAndPredCheckCorrect(self, result_struct):
        result_struct["Result"][Consts.PREDECESSOR] = self.getPredecessorName()
        result_struct["Result"][Consts.SUCCESSOR] = self.getSuccessorName()

    def getDescriptionContent(self):
        return self.sheet_view.descriptionArea.GetValue()

    def descriptionCorrect(self, result_struct):
        if re.sub(r'\s', "", self.getDescriptionContent()) == "":
            result_struct["ErrorMsg"] += "-> Please enter description of this {}\n".format(self.sheet_view.getEntityType())
            return False
        return True

    def checkAndDumpDescriptionArea(self, result_struct):
        correct = self.descriptionCorrect(result_struct)
        if correct: self.onDescriptionCorrect(result_struct)
        return correct

    def onDescriptionCorrect(self,result_struct):
        result_struct["Result"][Consts.DESCRIPTION] = self.getDescriptionContent()

    def checkAndDumpTexture(self, result_struct):
        correct = FileExistanceChecker().graphicalFileExists(self.sheet_view.entityIconRelativePath)
        if not correct:
            result_struct["ErrorMsg"] += "-> Icon path does not contain a valid graphical file\n"
        else:
            result_struct["Result"][Consts.TEXTURE_PATH] = self.sheet_view.entityIconRelativePath
        return correct

    def checkAndDumpTypeOfBuilding(self, result_struct):
        correct = self.getTypeOfBuilding() in ["Industrial", "Domestic"]
        if not correct:
            result_struct["ErrorMsg"] += "-> INVALID type of building, can be either Domestic or Industrial\n"
        else:
            result_struct["Result"][Consts.TYPE] = self.getTypeOfBuilding()
        return correct

    def getStartIncome(self):
        return self.sheet_view.start_income_picker.GetValue()

    def startIncomeCorrect(self):
        try:
            # income_str = self.sheet_view.currentDependencies[self.sheet_view.getSheetName()][self.getEntityName()][Consts.START_INCOME]
            income_str = self.getStartIncome()
            income = int(income_str)
            return income >= 0
        except Exception:
            return False

    def checkAndDumpStartIncome(self, result_struct):
        correct = self.startIncomeCorrect()
        if not correct:
            result_struct["ErrorMsg"] += "-> Start income of this {} is not valid, needs to be >= 0 \n".format(self.sheet_view.getEntityType())
        else:
            result_struct["Result"][Consts.START_INCOME] = str(self.sheet_view.start_income_picker.GetValue())
        return correct

    def getDwellerName(self):
        return self.sheet_view.dwellers_names_selector.GetStringSelection()

    def getAllDwellers(self):
        return self.sheet_view.currentDependencies[Consts.DWELLERS].keys()

    def checkAndDumpDweller(self, result_struct):
        correct = self.dwellerSelected(result_struct)
        if correct: self.onDwellerSelectedCorrectly(result_struct)
        return correct

    def dwellerSelected(self, result_struct):
        if self.getDwellerName() not in self.getAllDwellers():
            result_struct["ErrorMsg"] += "-> INVALID dweller name\n"
            return False
        return True

    def onDwellerSelectedCorrectly(self, result_struct):
        result_struct["Result"][Consts.DWELLER_NAME] = self.getDwellerName()

    def checkAndDumpDwellersAmount(self, result_struct):
        correct = self.getDwellersAmount() > 0
        if not correct:
            result_struct["ErrorMsg"] += "-> Dwellers amount should be bigger than 0\n"
        else:
            result_struct["Result"][Consts.DWELLERS_AMOUNT] = self.getDwellersAmount()
        return correct

    def getDwellersAmount(self):
        return self.sheet_view.dwellers_amount.GetValue()

    def getTypeOfBuilding(self):
        return self.sheet_view.type_of_building_selector.GetValue()

    def childrenInputCorrect(self, result_struct):
        correct = True
        for child in self.sheet_view.childrenCheckers:
            correct &= child.checkAndDumpCheckers(result_struct)
        return correct

class AddModeSheetEntityChecker(SheetEntityChecker):

    def checkAndDumpName(self, result_struct):
        correct = self.entityNameNotEmpty(result_struct)
        correct &= self.entityNameNotTakenYet(result_struct)
        if correct: self.onEntityNameCorrect(result_struct)
        return correct

    def onEntityNameCorrect(self, result_struct):
        result_struct["Result"][self.sheet_view.getEntityNameKey()] = self.getEntityName()

    def entityNameNotTakenYet(self, result_struct):
        if self.getEntityName() in self.getAllSheetEntitieNames():
            error_msg ="-> {} name already taken\n".format(self.sheet_view.getEntityType())
            result_struct["ErrorMsg"] += error_msg
            return False
        return True

    def entityNameNotEmpty(self, result_struct):
        if  re.sub(r'\s', "", self.getEntityName()) == "":
            error_msg =  "-> Not a valid name\n"
            result_struct["ErrorMsg"] += error_msg
            return False
        return True

    def getMode(self):
        return ADD_MODE

    def newSuccessExitMsg(self, entity_name):
        return {"Log": "Successfully added " + entity_name + " to entities list\n"}

class EditModeSheetEntityChecker(SheetEntityChecker):

    def checkAndDumpName(self, result_struct):
        result_struct["Result"][self.sheet_view.getEntityNameKey()] = self.getEntityName()
        return True # for now, nothing can go wrong here

    def getMode(self):
        return EDIT_MODE

    def newSuccessExitMsg(self, entity_name):
        return {"Log": "Successfully edited " + entity_name + "\n"}

class OnEntityCheck(object):

    def onCheck(self, sheetEntityChecker, result_struct):
        correct = self.entityCorrect(sheetEntityChecker, result_struct)
        sheetEntityChecker.onCorrectnessCheckFinished(correct, result_struct)

    def entityCorrect(self, sheetEntityChecker, result_struct = None):
        result_struct = sheetEntityChecker.newResultStruct() if result_struct is None else result_struct
        correct = self.checkAndDumpBasicCharacteristics(sheetEntityChecker, result_struct)
        correct &= self.mainCheckPipeline(sheetEntityChecker, result_struct)
        return correct

    def checkAndDumpBasicCharacteristics(self,  sheetEntityChecker, result_struct):
        correct = sheetEntityChecker.checkAndDumpName(result_struct)
        correct &= sheetEntityChecker.checkAndDumpPredAndSucc(result_struct)
        correct &= sheetEntityChecker.checkAndDumpDescriptionArea(result_struct)
        return correct & sheetEntityChecker.checkAndDumpTexture(result_struct)

    def mainCheckPipeline(self, sheetEntityChecker, result_struct):
        raise Exception("onCheck not implemented")

class ResourceSheetChecker(OnEntityCheck):

    def mainCheckPipeline(self, sheetEntityChecker, result_struct):
        return sheetEntityChecker.checkAndDumpStartIncome(result_struct)

class BuildingSheetChecker(OnEntityCheck):

    def mainCheckPipeline(self, sheetEntityChecker, result_struct):
        correct = sheetEntityChecker.checkAndDumpDweller(result_struct)
        correct &= sheetEntityChecker.checkAndDumpDwellersAmount(result_struct)
        correct &= sheetEntityChecker.checkAndDumpTypeOfBuilding(result_struct)
        return correct & sheetEntityChecker.childrenInputCorrect(result_struct)

class DwellerSheetChecker(OnEntityCheck):

    def mainCheckPipeline(self, sheetEntityChecker, result_struct):
        return sheetEntityChecker.childrenInputCorrect(result_struct)