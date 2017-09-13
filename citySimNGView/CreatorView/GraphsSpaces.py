import wx
from GraphPanel import GraphPanel

class GraphsSpaces(wx.Panel):
    def __init__(self, parent):
        super(GraphsSpaces, self).__init__(parent, size =(1500,500),style = wx.SIMPLE_BORDER)
        self.initRootSizer()

    def initRootSizer(self):
        self.rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rootSizer.Add(self.newResourcesGraphSpace())
        self.rootSizer.AddSpacer(10)
        self.rootSizer.Add(self.newDwellersGraphSpace())
        self.rootSizer.AddSpacer(10)
        self.rootSizer.Add(self.newBuildingsGraphSpace())
        self.rootSizer.AddSpacer(10)
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