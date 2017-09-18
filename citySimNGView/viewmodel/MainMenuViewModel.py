from wx import wx


class MainMenuViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayMainMenu(self):
        wx.CallAfter(self.viewSetter.setView, "MainMenu")

    class Java:
        implements = ["py4jmediator.ViewModel$MainMenuViewModel"]