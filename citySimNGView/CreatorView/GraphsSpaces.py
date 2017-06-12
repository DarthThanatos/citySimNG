import wx
from GraphPanel import GraphPanel
import json

class GraphsSpaces(wx.Panel):
    def __init__(self, parent):
        super(GraphsSpaces, self).__init__(parent, size =(1500,500),style = wx.SIMPLE_BORDER)
        self.rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.resourcesGraphSpace = GraphPanel(self, "Resources")
        self.buildingsGraphSpace = GraphPanel(self, "Buildings")
        self.dwellersGraphSpace = GraphPanel(self, "Dwellers")
        self.rootSizer.Add(self.resourcesGraphSpace)
        self.rootSizer.AddSpacer(10)
        self.rootSizer.Add(self.dwellersGraphSpace)
        self.rootSizer.AddSpacer(10)
        self.rootSizer.Add(self.buildingsGraphSpace)
        self.rootSizer.AddSpacer(10)
        self.SetSizer(self.rootSizer)
        self.rootSizer.Layout()

    def resetView(self, list_of_trees):
        dwellers_tree, resources_tree, buildings_tree = list_of_trees
        self.dwellersGraphSpace.tree = dwellers_tree
        self.buildingsGraphSpace.tree = buildings_tree
        self.resourcesGraphSpace.tree = resources_tree

        self.dwellersGraphSpace.Hide(); self.dwellersGraphSpace.Show()
        self.buildingsGraphSpace.Hide(); self.buildingsGraphSpace.Show()
        self.resourcesGraphSpace.Hide(); self.resourcesGraphSpace.Show()

    def resetViewFromJSON(self, jsonGraphDesc):
        #print json.dumps(jsonGraphDesc, indent = 4)
        self.dwellersGraphSpace.jsonDesc = jsonGraphDesc["Dwellers"]
        self.buildingsGraphSpace.jsonDesc = jsonGraphDesc["Buildings"]
        self.resourcesGraphSpace.jsonDesc = jsonGraphDesc["Resources"]
        self.dwellersGraphSpace.Hide(); self.dwellersGraphSpace.Show()
        self.buildingsGraphSpace.Hide(); self.buildingsGraphSpace.Show()
        self.resourcesGraphSpace.Hide(); self.resourcesGraphSpace.Show()