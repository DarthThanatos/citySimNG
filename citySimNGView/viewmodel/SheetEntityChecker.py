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

    def onCheck(self):
        self.checkCorectness(self.newResultStruct())

    def checkCorectness(self, result_struct):
        correct = self.checkAndDumpName(result_struct)
        correct &= self.checkAndDumpPredAndSucc(result_struct)
        correct &= self.checkAndDumpDescriptionArea(result_struct)
        correct &= self.checkAndDumpTexture(result_struct)
        correct &= self.checkAndDumpStartIncome(result_struct)
        self.onCorrectnessCheckFinished(correct, result_struct)

    def onCorrectnessCheckFinished(self, correct, result_struct):
        if not correct:
            self.sheet_view.log_area.SetValue(result_struct["ErrorMsg"])
            return
        self.onSheetCorrectlyFilled(result_struct)

    def getAllResourcesNames(self):
        return self.sheet_view.currentDependencies["Resources"].keys()

    def getEntityName(self):
        return self.sheet_view.NameInput.GetValue()

    def onSheetCorrectlyFilled(self, result_struct):
        self.getAllResourcesNames().append(self.getEntityName())
        self.sheet_view.currentDependencies["Resources"][self.getEntityName()] = result_struct["Result"]
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
        correct &= self.relationshipBetweenEntititesCorrect(result_struct, self.getEntityName(), self.getSuccessorName(), relationshipType=Consts.SUCCESSOR)
        correct &= self.relationshipBetweenEntititesCorrect(result_struct, self.getEntityName(), self.getPredecessorName(), relationshipType=Consts.PREDECESSOR)
        if correct: self.onSuccAndPredCheckCorrect(result_struct)
        return correct

    def onSuccAndPredCheckCorrect(self, result_struct):
        result_struct["Result"][Consts.PREDECESSOR] = self.getPredecessorName()
        result_struct["Result"][Consts.SUCCESSOR] = self.getSuccessorName()

    def getDescriptionContent(self):
        return self.sheet_view.descriptionArea.GetValue()

    def descriptionCorrect(self, result_struct):
        if re.sub(r'\s', "", self.getDescriptionContent()) == "":
            result_struct["ErrorMsg"] += "-> Please enter description of this resource\n"
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


class AddModeSheetEntityChecker(SheetEntityChecker):

    def checkAndDumpName(self, result_struct):
        correct = self.entityNameNotEmpty(result_struct)
        correct &= self.entityNameNotTakenYet(result_struct)
        if correct: self.onEntityNameCorrect(result_struct)
        return correct

    def onEntityNameCorrect(self, result_struct):
        result_struct["Result"]["Resource\nName"] = self.getEntityName()

    def entityNameNotTakenYet(self, result_struct):
        if self.getEntityName() in self.getAllResourcesNames():
            error_msg ="-> Resource name already taken\n"
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
        return {"Log": "Successfully added " + entity_name + " to resources list\n"}

class EditModeSheetEntityChecker(SheetEntityChecker):

    def checkAndDumpName(self, result_struct):
        result_struct["Result"]["Resource\nName"] = self.getEntityName()
        return True # for now, nothing can go wrong here

    def getMode(self):
        return EDIT_MODE

    def newSuccessExitMsg(self, resource_name):
        return {"Log": "Successfully edited " + resource_name + " resource\n"}