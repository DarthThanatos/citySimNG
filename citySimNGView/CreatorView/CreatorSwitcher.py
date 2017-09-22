import wx

from CreatorView import Consts
from DwellersSheet import  DwellersSheet
from ResourceSheet import ResourceSheet
from BuildingSheet import  BuildingSheet
from CreatorMainPanel import CreatorMainPanel
from RelativePaths import relative_music_path,relative_dependencies_path
from utils.OnShowUtil import OnShowUtil


class CreatorSwitcher(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender=None):
        wx.Panel.__init__(self, size=size, parent=parent)
        self.size = size
        self.sender = sender
        self.musicPath = musicPath
        self.init_views()
        self.hideAllPanels()
        self.showPanel("main_panel", initDataForSearchedPanel=None)
        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def newCurrentDependencies(self):
        return {
            Consts.SET_NAME : "Default Set",
            Consts.TEXTURE_ONE: "Grass.png",
            Consts.TEXTURE_TWO: "Grass2.jpg",
            Consts.RESOURCES: {},
            Consts.BUILDINGS: {},
            Consts.DWELLERS: {}
        }

    def newCurrentDependenciesKeys(self):
        return self.newCurrentDependencies().keys()

    def init_views(self):
        current_dependencies = self.newCurrentDependencies()
        self.views = {
            "main_panel": CreatorMainPanel(self, self.size, self, current_dependencies, self.sender),
            "Resources": ResourceSheet(self, self.size, self, current_dependencies),
            "Dwellers": DwellersSheet(self, self.size, self, current_dependencies),
            "Buildings": BuildingSheet(self, self.size, self, current_dependencies)
        }

    def setupPanelEditMode(self, panelName, editedElementName):
        self.views[panelName].setUpEditMode(editedElementName)

    def showPanel(self, searchedPanelName, initDataForSearchedPanel):
        for panelName in self.views:
            if panelName == searchedPanelName:
                self.views[panelName].wakeUpData = initDataForSearchedPanel
                self.views[panelName].Show()
            else:
                self.views[panelName].Hide()

    def hideAllPanels(self):
        for view in self.views: self.views[view].Hide()

    def onShow(self, event):
        OnShowUtil().switch_music_on_show_changed(event, self.musicPath, onShowCallback = self.resetView)

    def resetView(self):
        self.views["main_panel"].resetView()

    def readMsg(self, msg):
        self.views["main_panel"].readMsg(msg)