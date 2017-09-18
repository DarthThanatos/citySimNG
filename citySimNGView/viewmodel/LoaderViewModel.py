import json

from wx import wx

from utils.Converter import Converter


class LoaderViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayLoader(self):
        print "displaying loader"
        wx.CallAfter(self.viewSetter.setView, "Loader")

    def displayDependenciesGraph(self, jsonGraph):
        wx.CallAfter(
            self.viewSetter.views["Loader"].displayDependenciesGraph,
            json.loads(jsonGraph.toString())
        )

    def displayPossibleDependenciesSets(self, possibleSets):
        wx.CallAfter(
            self.viewSetter.views["Loader"].displayPossibleDependenciesSets,
            Converter(self.viewSetter.gateway).convertCollectionToList(possibleSets)
        )

    class Java:
        implements = ["py4jmediator.ViewModel$LoaderViewModel"]