import json
import traceback


class DependenciesFileLoader(object):

    def __init__(self, creator_view):
        self.creator_view = creator_view

    def onLoadFileSelected(self, path):
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
                # probe if json parser does not fail at this input
                dependencies_dict = self.loadDependenciesFileContentToDict(dependency_file)
                self.creator_view.fillCurrentDependenciesWithContent(dependencies_dict)
                self.onLoadFileNotCorrupted(dependenciesCopy)
            except Exception:
                traceback.print_exc()
                self.creator_view.dependencyLoadFail()

    def onLoadFileNotCorrupted(self, dependenciesCopy):
        if not self.creator_view.fileContentsCorrect():
            self.onLoadedUncorrectContent(dependenciesCopy)
            return
        self.onLoadedCorrectContent()

    def onLoadedUncorrectContent(self, dependenciesCopy):
        self.restoreDependenciesCopy(dependenciesCopy)
        errorMsg = "Error while loading file, previous dependency set still on board"
        self.creator_view.logArea.SetValue(errorMsg)

    def onLoadedCorrectContent(self):
        # we're good, just reload view and praise the Lord
        self.creator_view.resetView()
        msg = "Dependencies loaded successfully!"
        self.creator_view.logArea.SetLabelText(msg)


    def loadDependenciesFileContentToDict(self, dependency_file):
        dependency_content = dependency_file.read().replace("u'", "'").replace("'", "\"")
        return json.loads(dependency_content)

    def restoreDependenciesCopy(self, dependenciesCopy):
        self.creator_view.fillCurrentDependenciesWithContent(dependenciesCopy)  # here we restore previous state of subpanels
        self.creator_view.resetView()

