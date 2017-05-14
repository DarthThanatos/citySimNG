import wx
from DwellersPanel import  DwellersPanel
from ResourcesPanel import ResourcesPanel
from BuildingsPanel import  BuildingsPanel
from CreatorMainEntry import CreatorMainEntry
from RelativePaths import relative_music_path,relative_dependencies_path

class CreatorSwitcher(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender=None):
        wx.Panel.__init__(self, size=size, parent=parent)

        self.musicPath = musicPath
        current_dependencies = {}
        buildingsNames = ["Building1","Building2"]
        resourcesNames = ["Res1","Res2"]
        dwellersNames = ["Dweller1","Dweller2"]
        lists_of_names = [buildingsNames, resourcesNames, dwellersNames]

        self.main_panel = CreatorMainEntry(self, size, self, current_dependencies,  lists_of_names, sender)
        self.resources_panel = ResourcesPanel(self, size, self, current_dependencies, lists_of_names)
        self.dwellers_panel = DwellersPanel(self, size, self, current_dependencies, lists_of_names)
        self.buildings_panel = BuildingsPanel(self, size, self, current_dependencies, lists_of_names)

        self.views = {
            "main_panel": self.main_panel,
            "Resources": self.resources_panel,
            "Dwellers": self.dwellers_panel,
            "Buildings": self.buildings_panel
        }
        for view in self.views: self.views[view].Hide()
        self.showPanel("main_panel", initDataForSearchedPanel=None)

    def readMsg(self, msg):
        self.main_panel.readMsg(msg)

    def showPanel(self, searchedPanelName, initDataForSearchedPanel):
        for panelName in self.views:
            if panelName == searchedPanelName:
                self.views[panelName].wakeUpData = initDataForSearchedPanel
                self.views[panelName].Show()
            else:
                self.views[panelName].Hide()

    def onShow(self, event):
        global pygame
        if event.GetShow():
            self.resetView()
            try:
                import pygame
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(
                    self.musicPath)
                pygame.mixer.music.play()
            except Exception:
                print "Problem with music"
        else:
            try:
                pygame.quit()
            except Exception:
                print "creator: problem with pygame quit"

    def resetView(self):
        pass
