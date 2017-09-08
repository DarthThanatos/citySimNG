from wx import wx

class GameMenuViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayGameMenu(self):
        print "displaying game menu"
        wx.CallAfter(self.viewSetter.setView, "GameMenu")

    class Java:
        implements = ["py4jmediator.ViewModel$GameMenuViewModel"]