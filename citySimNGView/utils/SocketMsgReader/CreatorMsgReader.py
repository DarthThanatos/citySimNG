import json

class CreatorMsgReader(object):

    def __init__(self, creator_view):
        self.creator_view = creator_view
        self.operations = {
            "ParseConfirm": self.onParseConfirm,
            "ParseFail" : self.onParseFail
        }

    def reactOnMsg(self, msg):
        jsonMsg = json.loads(msg)
        operation = jsonMsg["Operation"]
        self.operations[operation](jsonMsg)

    def onParseConfirm(self, jsonMsg):
        self.creator_view.ackMsgs[jsonMsg["Args"]["UUID"]] = True #unblock blocked thread
        self.creator_view.graphsSpaces.resetViewFromJSON(jsonMsg["Args"]["graph"])
        log_msg = "Dependencies created successfully, please go to the Loader menu now to check what was created"
        self.creator_view.logArea.SetLabelText(log_msg)

    def onParseFail(self, jsonMsg):
        self.creator_view.ackMsgs[jsonMsg["Args"]["UUID"]] = True #unblock blocked thread
        self.creator_view.logArea.SetLabelText(jsonMsg["Args"]["errorMsg"])
