import json


class JSONMonter(object):

    def mountMoveToMsg (self, src, target):
        msg = {}
        msg["To"] = src
        msg["Operation"] = "MoveTo"
        msg["Args"] = {}
        msg["Args"]["TargetView"] = target
        msg["Args"]["TargetControlNode"] = target + "Node"
        return json.dumps(msg)

    def mountShowGraphMsg(self, setChosen):
        msg = {}
        msg["To"] = "LoaderNode"
        msg["Operation"] = "ShowGraph"
        msg["Args"] = {}
        msg["Args"]["SetChosen"] = setChosen
        return json.dumps(msg)

    def mountSelectMsg(self, setChosen, operationId):
        msg = {}
        msg["To"] = "LoaderNode"
        msg["Operation"] = "Select"
        msg["Args"] = {}
        msg["Args"]["SetChosen"] = setChosen
        msg["Args"]["UUID"] = operationId
        return json.dumps(msg)

    def mountExitMsg(self):
        msg = {}
        msg["To"] = "MainMenuNode"
        msg["Args"] = {}
        msg["Operation"] = "Exit"
        return msg