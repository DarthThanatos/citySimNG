import json
import traceback

from CreatorView import Consts
from utils.LogMessages import WELCOME_MSG


class DependenciesFileLoader(object):

    def __init__(self, creator_view):
        self.creator_view = creator_view

    def onLoadFileSelected(self, path):
        self.creator_view.logArea.SetValue("")
        if not self.fileSuffixedCorrectly(path):
            self.creator_view.dependencyLoadFail()
            return
        self.onFileSuffixedCorrectly(path)

    def fileSuffixedCorrectly(self, path):
        return path.endswith(".dep")

    def onFileSuffixedCorrectly(self, path):
        dependenciesCopy = self.creator_view.fetchDependenciesCopy()  # if sth goes wrong, we can restore previous state
        with open(path, "r+") as dependency_file:
            try:
                dependencies_dict = self.loadDependenciesFileContentToDict(dependency_file)
                self.onLoadFileNotCorrupted(dependencies_dict, dependenciesCopy)
            except Exception:
                traceback.print_exc()
                self.creator_view.dependencyLoadFail()

    def onLoadFileNotCorrupted(self, dependencies_dict, dependenciesCopy):
        try:
            self.creator_view.fillCurrentDependenciesWithValidContent(dependencies_dict)
            if not self.creator_view.currentDependenciesCorrect(updateNameFromInput=False): raise Exception
            self.onLoadedCorrectContent()
        except Exception:
            self.onLoadedUncorrectContent(dependenciesCopy)
            return

    def onLoadedUncorrectContent(self, dependenciesCopy):
        self.restoreDependenciesCopy(dependenciesCopy)
        errorMsg = "Error while loading file, previous dependency set still on board\n"
        self.creator_view.logArea.AppendText(errorMsg)

    def onLoadedCorrectContent(self):
        self.creator_view.resetContents("Dependencies loaded successfully!")

    def loadDependenciesFileContentToDict(self, dependency_file):
        dependency_content = dependency_file.read().replace("u'", "'").replace("'", "\"")
        return json.loads(dependency_content)

    def restoreDependenciesCopy(self, dependenciesCopy):
        self.creator_view.fillCurrentDependenciesWithValidContent(dependenciesCopy)  # here we restore previous state of subpanels
        self.creator_view.resetContents()