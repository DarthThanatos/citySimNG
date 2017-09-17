import wx
from GraphPanel import GraphPanel

class GraphsSpaces(wx.Panel):
    def __init__(self, parent):
        super(GraphsSpaces, self).__init__(parent, size =(1500,500),style = wx.SIMPLE_BORDER)
        self.initRootSizer()

    def addToSizerWithSpace(self, sizer, view, space = 10, alignment = wx.CENTER):
        sizer.Add(view, 0, alignment)
        sizer.AddSpacer(space)

    def newRootSizer(self):
        self.rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.addToSizerWithSpace(self.rootSizer, self.newResourcesGraphSpace())
        self.addToSizerWithSpace(self.rootSizer, self.newDwellersGraphSpace())
        self.addToSizerWithSpace(self.rootSizer, self.newBuildingsGraphSpace())
        return self.rootSizer

    def initRootSizer(self):
        self.rootSizer = self.newRootSizer()
        self.SetSizer(self.rootSizer)
        self.rootSizer.Layout()

    def newResourcesGraphSpace(self):
        self.resourcesGraphSpace = GraphPanel(self, "Resources")
        return self.resourcesGraphSpace

    def newDwellersGraphSpace(self):
        self.dwellersGraphSpace = GraphPanel(self, "Dwellers")
        return self.dwellersGraphSpace

    def newBuildingsGraphSpace(self):
        self.buildingsGraphSpace = GraphPanel(self, "Buildings")
        return self.buildingsGraphSpace

    def getGraphSpaces(self):
        return [self.dwellersGraphSpace, self.resourcesGraphSpace, self.buildingsGraphSpace]

    def resetViewFromJSON(self, jsonGraphDesc):
        for graphSpace in self.getGraphSpaces():
            graphSpace.triggerGraphResetFromJSON(jsonGraphDesc)