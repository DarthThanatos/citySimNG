from viewmodel.GameMenuViewModel import GameMenuViewModel
from viewmodel.LoaderViewModel import LoaderViewModel
from viewmodel.MainMenuViewModel import MainMenuViewModel
from CreatorViewModel import  CreatorViewModel

class ViewModel(object):
    def __init__(self, viewSetter):
        self.viewSetter = viewSetter
        self.mainMenuViewModel = MainMenuViewModel(viewSetter)
        self.creatorViewModel = CreatorViewModel(viewSetter)
        self.gameMenuViewModel = GameMenuViewModel(viewSetter)
        self.loaderViewModel = LoaderViewModel(viewSetter)

    def getGameMenuViewModel(self):
        return self.gameMenuViewModel

    def getCreatorViewModel(self):
        return self.creatorViewModel

    def getMainMenuViewModel(self):
        return self.mainMenuViewModel

    def getLoaderViewModel(self):
        return self.loaderViewModel

    class Java:
        implements = ["py4jmediator.ViewModel"]