import re

from CreatorView import Consts

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

    def relationshipBetweenEntititesCorrect(self, result_struct, entityOneName, entityTwoName, relationshipType):
        if entityOneName == entityTwoName :
            result_struct["ErrorMsg"] += "-> " + entityOneName + " cannot be its own " + relationshipType + "\n"
            return False
        return True

    def successorAndPredeccessorRelationshipCorrect(self, result_struct):
        if self.getSuccessorName() == self.getPredecessorName() and self.getSuccessorName() != "None":
            result_struct["ErrorMsg"] += "-> Predecessor and Successor cannot be the same (both can be None though)\n"
            return False
        return True

    def checkAndDumpPredAndSucc(self, result_struct):
        correct = self.successorAndPredeccessorRelationshipCorrect(result_struct)
        correct &= self.relationshipBetweenEntititesCorrect(
            result_struct, self.getEntityName(), self.getSuccessorName(), relationshipType=Consts.SUCCESSOR
        )
        correct &= self.relationshipBetweenEntititesCorrect(
            result_struct, self.getEntityName(), self.getPredecessorName(), relationshipType=Consts.PREDECESSOR
        )
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
        result_struct["Result"][Consts.TEXTURE_PATH] = self.sheet_view.entityIconRelativePath
        return True # for now, nothing can go wrong here

    def checkAndDumpStartIncome(self, result_struct):
        result_struct["Result"][Consts.START_INCOME] = str(self.sheet_view.start_income_picker.GetValue())
        return True # for now, nothing can go wrong here

    def getDwellerName(self):
        return self.sheet_view.dwellers_names_selector.GetStringSelection()

    def checkAndDumpDweller(self, result_struct):
        correct = self.dwellerSelected(result_struct)
        if correct: self.onDwellerSelectedCorrectly(result_struct)
        return correct

    def dwellerSelected(self, result_struct):
        if self.getDwellerName() == "" or self.getDwellerName() == "None":
            result_struct["ErrorMsg"] += "-> Please select a dweller that lives here\n"
            return False
        return True

    def onDwellerSelectedCorrectly(self, result_struct):
        result_struct["Result"][Consts.DWELLER_NAME] = self.getDwellerName()

    def checkAndDumpDwellersAmount(self, result_struct):
        result_struct["Result"][Consts.DWELLERS_AMOUNT] = self.getDwellersAmount()
        return True

    def checkAndDumpTypeOfBuilding(self, result_struct):
        result_struct["Result"][Consts.TYPE] = self.getTypeOfBuilding()
        return True

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