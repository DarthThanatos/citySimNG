import wx

from CreatorView.SheetView import SheetView
import Consts
from viewmodel.SheetEntityChecker import DwellerSheetChecker


class DwellersSheet(SheetView):
    def __init__(self, parent, size, frame, currentDependencies):
        super(DwellersSheet, self).__init__(parent, size, frame, currentDependencies)
        self.initRootSizer(self.newDwellerCharacteristicsVerticalSizer(), topPadding=75)

    def getDefaultIconRelativePath(self):
        return "dweller.jpg"

    def getEntityType(self):
        return Consts.DWELLER

    def getEntityNameKey(self):
        return Consts.DWELLER_NAME

    def getSheetName(self):
        return Consts.DWELLERS

    def submit(self, event):
        self.sheetChecker.onCheck(DwellerSheetChecker())

    def newDwellerCharacteristicsVerticalSizer(self):
        dwellerCharacteristicsVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        dwellerCharacteristicsVerticalSizer.Add(self.newBasicCharacteristicsVerticalSizer(), 0, wx.CENTER)
        dwellerCharacteristicsVerticalSizer.Add(self.newLine(), 0, wx.EXPAND)
        self.addToSizerWithSpace(dwellerCharacteristicsVerticalSizer, self.newResourcesConsumedChecker())
        return dwellerCharacteristicsVerticalSizer


