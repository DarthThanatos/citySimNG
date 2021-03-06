import json

import math

import matplotlib.pyplot as plt
import networkx as nx
import wx
from math import sqrt
from math import pi

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from networkx.drawing.nx_agraph import graphviz_layout
relative_textures_path = "resources\\Textures\\"
import matplotlib.lines as mlines

class NetworkPanel(wx.Panel):

    def __init__(self, parent, space_name):
        wx.Panel.__init__(self, parent, size = screenDims)
        self.space_name = space_name
        self.parent = parent
        self.jsonDesc = self.neDefaultJSONDesc()
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.G = None
        self.pos = None
        self.main_axis = None
        self.axesDict = None
        self.initRootSizer()

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self.newCanvas(), 1, wx.LEFT | wx.TOP | wx.GROW)
        self.SetSizer(rootSizer)
        rootSizer.Fit(self)

    def newCanvas(self):
        self.canvas = FigCanvas(self, -1, plt.gcf())
        self.canvas.mpl_connect('button_press_event', self.onClick)
        return self.canvas

    def onClick(self, event):
        if self.G is None or self.pos is None: return
        if event.inaxes is self.main_axis: return
        (x,y)   = event.inaxes.transData.transform((event.xdata, event.ydata))
        xs, xe = event.inaxes.get_xlim()
        ys, ye = event.inaxes.get_ylim()
        xs_disp, ys_disp = event.inaxes.transData.transform((xs, ys))
        xe_dips, ye_disp = event.inaxes.transData.transform((xe, ye))
        radius = max(xe_dips - xs_disp, ye_disp - ys_disp) / 2
        for i in self.G.nodes():
            node = self.main_axis.transData.transform(self.pos[i])
            distance = sqrt(pow(x-node[0],2)+pow(y-node[1],2))
            if distance < radius:
                print "clicked:", i

    def neDefaultJSONDesc(self):
        return {"Dwellers":[], "Buildings":[], "Resources":[]}

    def newGraphFromJSON(self):
        G = nx.DiGraph()
        self.mountRec(G, self.jsonDesc)
        return G

    def angleToRad(self, angle):
        return math.pi / 180 * angle

    def k(self, r, gamma):
        return r / sqrt(1 / pow(math.tan(gamma), 2) + 1)

    def xFromY(self, y, xlim, ylim, gamma):
        return (y - ylim) / math.tan(gamma) + xlim

    def arrowLine(self, r, gamma, xlim, ylim):
        if gamma != pi/2:
            y = ylim + self.k(r, gamma)
            x = self.xFromY(y, xlim, ylim, gamma)
        else:
            x = xlim
            y = ylim + r
        self.drawLine(xlim,x,ylim,y)

    def drawLine(self, x1, x2, y1, y2):
        l = mlines.Line2D([x1, x2], [y1, y2], color="black", linewidth=1)
        self.main_axis.add_line(l)

    def startEndPoints(self, edge):
        n1, n2 = edge
        return self.pos[n1], self.pos[n2]

    def r(self, edge, arrowLength = 0.125):
        (xs, ys), (xe, ye) = self.startEndPoints(edge)
        edgeLength = sqrt(pow(xs - xe,2) + pow(ys - ye, 2))
        return edgeLength * arrowLength

    def radBeta(self, edge):
        (xs, ys), (xe, ye) = self.startEndPoints(edge)
        return math.atan((ye - ys) / (xe - xs)) if xe - xs != 0 else math.pi / 2

    def yLim(self, endNode):
        ax = self.axesDict[endNode]
        (ylim_neg, ylim_pos) = self.main_axis.transData.inverted().transform(ax.transData.transform(ax.get_ylim()))
        return ylim_pos

    def xLim(self, y_lim, edge):
        (xs, ys), (xe, ye) = self.startEndPoints(edge)
        return (y_lim - ys + (ye - ys) / (xe - xs) * xs) * (xe - xs )/ (ye - ys) if xs != xe and ys != ye else xe

    def addArrowTo(self, (n1,n2), r, alpha = 10):
        rad_beta = self.radBeta((n1,n2))
        rad_alpha = self.angleToRad(alpha)
        y_lim = self.yLim(n2)
        x_lim = self.xLim(y_lim, (n1,n2))
        self.arrowLine(r, rad_beta - rad_alpha, x_lim, y_lim)
        self.arrowLine(r,rad_beta + rad_alpha, x_lim, y_lim)

    def findMinR(self, G):
        return min([self.r(edge) for edge in G.edges()])

    def addArrowsToGraph(self,G):
        r = self.findMinR(G)
        for e in G.edges():
            self.addArrowTo(e,r)

    def jsonTreeHeight(self, lvlList):
        return (max([self.jsonTreeHeight(childDesc["Children"]) for childDesc in lvlList]) if lvlList.__len__() != 0 else 0)+ 1

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

    def fillGraph(self, G, pos):
        plt.clf()
        self.axesDict = {}
        self.G = G
        self.pos = pos
        treeHeight = self.jsonTreeHeight(self.jsonDesc) - 1
        nx.draw(G, pos, arrows = False)
        self.main_axis = plt.gca()
        ax =  plt.gca()
        labelsPosDict = self.drawNodesYieldingNewPos(G, pos, treeHeight)
        if treeHeight <= 5:
            nx.draw_networkx_labels(G, labelsPosDict, self.fetchLabelsOfVertices(G), ax = ax, font_size=10)
        self.addArrowsToGraph(G)

    def drawRectsRoundLabels(self, G, labelsPosDict):
        fig = plt.gcf()
        for nodeName in G.nodes():
            label_x, label_y = fig.transFigure.inverted().transform(self.main_axis.transData.transform(labelsPosDict[nodeName]))
            txt = fig.text(label_x, label_y, nodeName, fontsize = 10)
            renderer = self.canvas.get_renderer()
            bbox = txt.get_window_extent(renderer)
            rect = Rectangle([bbox.x0 - bbox.width/2, bbox.y0 - bbox.height/4], bbox.width, bbox.height, color = [0,0,0], fill = False)
            fig.patches.append(rect)
            txt.remove()

    def getLabelHeight(self, nodeName):
        txt = plt.gcf().text(0, 0, nodeName, fontsize=10)
        renderer = self.canvas.get_renderer()
        bbox = txt.get_window_extent(renderer)
        txt.remove()
        return self.main_axis.transData.inverted().transform((bbox.width, bbox.height))[1]

    def drawNodesYieldingNewPos(self, G, pos, treeHeight):
        ax_transData = plt.gca().transData.transform
        ax_inv_trans = plt.gca().transData.inverted().transform
        fig_invtrans = plt.gcf().transFigure.inverted().transform
        newLabelsPos = {}
        for node in G.nodes():
            xa, ya = fig_invtrans(ax_transData(pos[node]))  # axes coordinates
            self.addImageAxis(xa, ya, img = G.node[node]['image'], nodeName= node, pos = pos, ax_inv_trans = ax_inv_trans, newLabelsPos=newLabelsPos, treeHeight=treeHeight)
        return newLabelsPos

    def addImageAxis(self, xa, ya, img, nodeName,  pos, newLabelsPos, treeHeight, ax_inv_trans):
        imsize = max (0.04, 0.1 - 0.02 * (treeHeight - 1) / 5)
        a = plt.axes([xa - imsize / 2.0, ya - imsize / 2.0, imsize, imsize]) # normalized units from (0,1)
        xs, xe = a.get_xlim()
        ys, ye = a.get_ylim()
        xs_disp,ys_disp = ax_inv_trans(a.transData.transform((xs,ys)))
        xe_disp, ye_disp = ax_inv_trans(a.transData.transform([xe, ye]))
        newLabelsPos[nodeName] = pos[nodeName][0], pos[nodeName][1] - (ye_disp - ys_disp + self.getLabelHeight(nodeName))/2
        a.imshow( mpimg.imread(img) )
        a.axis('off')
        self.axesDict[nodeName] = a

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
    frm = MainFrame(json_desc)
    frm.Show()

app.MainLoop()