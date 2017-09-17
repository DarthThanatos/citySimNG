import wx
from wx.lib.scrolledpanel import ScrolledPanel

from CreatorView.SheetBasicViewsUtils import SheetBasicViewsUtils
from NumberFillingChecker import NumberFillingChecker
import Consts
from utils.OnShowUtil import OnShowUtil
from viewmodel.SheetEntityChecker import EDIT_MODE, EditModeSheetEntityChecker, AddModeSheetEntityChecker, \
    DwellerSheetChecker


class DwellersPanel(ScrolledPanel):
    def __init__(self,parent, size, frame, currentDependencies):
        ScrolledPanel.__init__(self, size = size, parent = parent, style = wx.SIMPLE_BORDER)
        self.SetupScrolling()
        self.wakeUpData = None
        self.restorableViews = []
        self.childrenCheckers = []
        self.entityIconRelativePath = self.getDefaultIconRelativePath()
        self.sheetChecker = AddModeSheetEntityChecker(self)
        self.size = size
        self.frame = frame
        self.currentDependencies = currentDependencies
        self.sheet_name = Consts.DWELLERS
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.sheetChecker = AddModeSheetEntityChecker(self)
        SheetBasicViewsUtils(self).initRootSizer(self.newDwellerCharacteristicsVerticalSizer(), topPadding=75)

    def newDwellerCharacteristicsVerticalSizer(self):
        dwellerCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        dwellerCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newBasicCharacteristicsVerticalSizer(),0,wx.CENTER)
        dwellerCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newLine(), 0, wx.EXPAND)
        dwellerCharacteristicsVerticalSizer.Add(SheetBasicViewsUtils(self).newResourcesConsumedChecker(),0, wx.CENTER)
        dwellerCharacteristicsVerticalSizer.AddSpacer(10)
        return dwellerCharacteristicsVerticalSizer

    def getDefaultIconRelativePath(self):
        return "dweller.jpg"

    def getEntityType(self):
        return Consts.DWELLER

    def getEntityNameKey(self):
        return Consts.DWELLER_NAME

    def setupSheetMode(self, sheetMode, edit_element_name = None):
        SheetBasicViewsUtils(self).setupMode(sheetMode,edit_element_name)
        for child in self.childrenCheckers:
            child.fillWithEntries(edit_element_name if sheetMode.getMode() == EDIT_MODE else None)

    def setUpEditMode(self, edit_element_name):
        self.setupSheetMode(EditModeSheetEntityChecker(self), edit_element_name)

    def setUpAddMode(self):
        self.setupSheetMode(AddModeSheetEntityChecker(self))

    def onShow(self, event):
        OnShowUtil().onCreatorSheetShow(self, event)

    def submit(self, event):
        self.sheetChecker.onCheck(DwellerSheetChecker())

