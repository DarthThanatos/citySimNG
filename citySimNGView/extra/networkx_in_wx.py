import json

import matplotlib.pyplot as plt
import networkx as nx
import wx
from math import sqrt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import matplotlib.image as mpimg
from networkx.drawing.nx_agraph import graphviz_layout

relative_textures_path = "resources\\Textures\\"

class NetworkPanel(wx.Panel):

    def __init__(self, parent, space_name):
        wx.Panel.__init__(self, parent, size = screenDims)
        self.space_name = space_name
        self.parent = parent
        self.jsonDesc = self.neDefaultJSONDesc()
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.G = None
        self.pos = None
        self.initRootSizer()

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self.newCanvas(), 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(rootSizer)
        rootSizer.Fit(self)

    def newCanvas(self):
        canvas = FigCanvas(self, -1, plt.gcf())
        canvas.mpl_connect('button_press_event', self.onClick)
        return canvas

    def neDefaultJSONDesc(self):
        return {"Dwellers":[], "Buildings":[], "Resources":[]}

    def newGraphFromJSON(self):
        G = nx.DiGraph()
        self.mountRec(G, self.jsonDesc)
        return G

    def mountRec(self, G, lvlList):
        for childDesc in lvlList:
            self.mountTreeLvl(G, childDesc)
            self.mountRec(G, childDesc["Children"])

    def mountTreeLvl(self, G, lvlDesc):
        currentNodeName = str(lvlDesc["Name"])
        for childName in self.getChildrenNames(lvlDesc):
            G.add_edge(currentNodeName, str(childName), size = 0.1)
        if self.getChildrenNames(lvlDesc).__len__() == 0:
            G.add_node(currentNodeName)
        G.node[currentNodeName]["image"] = lvlDesc["Texture path"]

    def getChildrenNames(self, lvlDesc):
        return [child["Name"] for child in lvlDesc["Children"]]

    def fetchLabelsOfVertices(self, G):
        return {name: name for name in G.nodes()}

    def newLabelsPos(self, G, pos, imgSize = 75):
        return {vertexName : (x , y - imgSize) for vertexName, (x,y) in zip(pos.keys(), pos.values())}

    def fillGraph(self, G, pos):
        plt.clf()
        self.G = G
        self.pos = pos
        nx.draw(G, pos,arrows=True)
        nx.draw_networkx_edges(G, pos)
        nx.draw_networkx_labels(G, self.newLabelsPos(G, pos), self.fetchLabelsOfVertices(G))
        self.drawNodes(G, pos)

    def onClick(self, event):
        if self.G is None or self.pos is None: return
        (x,y)   = (event.xdata, event.ydata)
        print x,y
        for i in self.G.nodes():
            node = self.pos[i]
            distance = sqrt(pow(x-node[0],2)+pow(y-node[1],2))
            print node, distance
            if distance < 500:
                print i, "clicked"
        print

    def drawNodes(self, G, pos):
        ax_transData = plt.gca().transData.transform
        fig_invtrans = plt.gcf().transFigure.inverted().transform
        for node in G.nodes():
            xa, ya = fig_invtrans(ax_transData(pos[node]))  # axes coordinates
            self.addImageAxis(xa, ya, img = G.node[node]['image'], label = node)

    def addImageAxis(self, xa, ya, img, label, imsize = 0.1):
        a = plt.axes([xa - imsize / 2.0, ya - imsize / 2.0, imsize, imsize])
        a.imshow(mpimg.imread(img))
        a.set_aspect('equal')
        a.axis('off')

    def resetViewFromJSON(self):
        G = self.newGraphFromJSON()
        self.fillGraph(G, pos = graphviz_layout(G, prog='dot'))

    def onShow(self, ev):
        if ev.GetShow(): self.resetViewFromJSON()

    def triggerGraphResetFromJSON(self,jsonGraphDesc):
        self.jsonDesc = jsonGraphDesc[self.space_name]
        self.Hide(); self.Show()


class MainFrame(wx.Frame):
    def __init__(self, jsonDesc, size=wx.DefaultSize):
        wx.Frame.__init__(self, None, title='Test', size=screenDims)
        self.jsonDesc = jsonDesc
        self.views = self.newViews()
        self.hideAllViews()
        self.initRootSizer()

    def newViews(self):
        return {
            "Resources" : NetworkPanel(self, "Resources"),
            "Buildings": NetworkPanel(self, "Buildings"),
            "Dwellers": NetworkPanel(self, "Dwellers")
        }

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self.newButtonSizer(), flag = wx.CENTER)
        self.SetSizer(rootSizer)

    def newButtonSizer(self):
        buttonSizer= wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer.Add(self.newButton("Resources"))
        buttonSizer.Add(self.newButton("Buildings"))
        buttonSizer.Add(self.newButton("Dwellers"))
        return buttonSizer

    def newButton(self, label):
        btn = wx.Button(self, label=label)
        btn.Bind(wx.EVT_BUTTON, self.onBtnClick)
        return btn

    def onBtnClick(self, ev):
        clicked_btn = ev.GetEventObject()
        for viewKey in self.views:
            if viewKey != clicked_btn.GetLabel(): self.views[viewKey].Hide()
        self.views[clicked_btn.GetLabel()].triggerGraphResetFromJSON(self.jsonDesc)

    def hideAllViews(self):
        for view in self.views.values():
            view.Hide()


app = wx.App(False)
screenDims = wx.GetDisplaySize()

with open("resources\\sysFiles\modelFiles\graph_json_desc_example.txt", "rb+") as f:
    json_desc = json.loads(f.read().replace("u'", "'").replace("'", "\""))
    print json.dumps(json_desc, indent=4)
    frm = MainFrame(json_desc)
    frm.Show()

app.MainLoop()