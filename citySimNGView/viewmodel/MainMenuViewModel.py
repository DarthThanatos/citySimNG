from wx import wx


class MainMenuViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayLoader(self):
        print "displaying loader"
        wx.CallAfter(self.viewSetter.setView, "Loader")

    def displayCreator(self):
        print "displaying creator"
        wx.CallAfter(self.viewSetter.setView, "Creator")

    def displayMainMenu(self):
        print "displaying creator"
        wx.CallAfter(self.viewSetter.setView, "MainMenu")

    class Java:
        implements = ["py4jmediator.ViewModel$MainMenuViewModel"]