from wx import wx

from Converter import Converter


class GameMenuViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayGameMenu(self):
        print "displaying game menu"
        wx.CallAfter(self.viewSetter.setView, "GameMenu")

    def animateCurrentPrices(self, currentPricesJavaMap):
        wx.CallAfter(
            self.viewSetter.getView("GameMenu").animateCurrentPrices,
            Converter(self.viewSetter.gateway).convertJavaMapToDict(currentPricesJavaMap)
        )

    class Java:
        implements = ["py4jmediator.ViewModel$GameMenuViewModel"]