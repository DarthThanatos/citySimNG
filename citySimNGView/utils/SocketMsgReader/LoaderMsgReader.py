import json


class LoaderMsgReader(object):

    def __init__(self, loader_view):
        self.loader_view = loader_view
        self.operations = {
            "Init" : self.onInit,
            "SelectConfirm" : self.onSelectConfirm,
            "ShowGraphRes" : self.onShowGraphRes
        }

    def reactOnMsg(self, msg):
        msgObj = json.loads(msg)
        operation = msgObj["Operation"]
        self.operations[operation](msgObj)

    def onInit(self, msgObj):
        ruleSetsList = msgObj["Args"]["DependenciesNames"]
        self.loader_view.displayPossibleDependenciesSets(ruleSetsList)

    def onSelectConfirm(self, msgObj):
        operationId = msgObj["Args"]["UUID"]
        self.loader_view.ackMsgs[operationId] = True

    def onShowGraphRes(self,  msgObj):
        self.loader_view.displayDependenciesGraph(msgObj["Args"]["Graph"])