import wx

from CreatorView import Consts, CreatorConfig
from DwellersSheet import  DwellersSheet
from ResourceSheet import ResourceSheet
from BuildingSheet import  BuildingSheet
from CreatorMainPanel import CreatorMainPanel
from RelativePaths import relative_music_path
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
            Consts.SET_NAME : CreatorConfig.DEPENDENCIES_DEFAULT_SET_NAME,
            Consts.TEXTURE_ONE: CreatorConfig.TEXTURE_ONE_DEFAULT_NAME,
            Consts.TEXTURE_TWO: CreatorConfig.TEXTURE_TWO_DEFAULT_NAME,
            Consts.PANEL_TEXTURE: CreatorConfig.PANEL_TEXURE_DEFAULT_NAME,
            Consts.MP3 : CreatorConfig.MP3_DEFAULT_NAME,
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
            Consts.RESOURCES: ResourceSheet(self, self.size, self, current_dependencies),
            Consts.DWELLERS: DwellersSheet(self, self.size, self, current_dependencies),
            Consts.BUILDINGS: BuildingSheet(self, self.size, self, current_dependencies)
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
        self.views["main_panel"].resetContents()

    def readMsg(self, msg):
        self.views["main_panel"].readMsg(msg)