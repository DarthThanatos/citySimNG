import json

from wx import wx


class CreatorViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayCreator(self):
        wx.CallAfter(self.viewSetter.setView, "Creator")

    def displayDependenciesGraph(self, jsonGraph):
        wx.CallAfter(
            self.viewSetter.getView("Creator").views["main_panel"].displayDependenciesGraph,
            json.loads(jsonGraph.toString())
        )

    def displayMsg(self, msg):
        wx.CallAfter(self.viewSetter.getView("Creator").views["main_panel"].displayMsg, msg)

    class Java:
        implements = ["py4jmediator.ViewModel$CreatorViewModel"]