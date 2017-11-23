import json

from wx import wx


class TutorialViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayTutorial(self): #ok?
        wx.CallAfter(self.viewSetter.setView, "Tutorial")

    def displayDependenciesGraph(self, jsonGraph): #chyba ok
        wx.CallAfter(
            self.viewSetter.getView("Tutorial").displayDependenciesGraph,
            json.loads(jsonGraph.toString())
        )

    def displayTutorialPage(self, jsonPage): #brak
        wx.CallAfter(self.viewSetter.getView("Tutorial").displayTutorialPage,
            json.loads(jsonPage.toString()))

    def fetchTutorialIndex(self, index):
        wx.CallAfter(self.viewSetter.getView("Tutorial").fetchTutorialIndex,
            index)

    def fetchNodes(self, buildingsList, resourcesList, dwellersList):
        wx.CallAfter(self.viewSetter.getView("Tutorial").fetchNodes,
            buildingsList, resourcesList, dwellersList)

    class Java:
        implements = ["py4jmediator.ViewModel$TutorialViewModel"]