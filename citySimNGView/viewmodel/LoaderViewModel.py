import json

from wx import wx

from utils.Converter import Converter


class LoaderViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayLoader(self):
        wx.CallAfter(self.viewSetter.setView, "Loader")

    def displayDependenciesGraph(self, jsonGraph):
        wx.CallAfter(
            self.viewSetter.getView("Loader").displayDependenciesGraph,
            json.loads(jsonGraph.toString())
        )

    def displayPossibleDependenciesSets(self, possibleSets):
        wx.CallAfter(
            self.viewSetter.getView("Loader").displayPossibleDependenciesSets,
            Converter(self.viewSetter.gateway).convertPyCollectionToJavaList(possibleSets)
        )

    class Java:
        implements = ["py4jmediator.ViewModel$LoaderViewModel"]