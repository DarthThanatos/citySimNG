import matplotlib.pyplot as plt
import networkx as nx
import wx
from math import sqrt

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigCanvas
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from networkx.drawing.nx_agraph import graphviz_layout

from CreatorView.GraphDetails.ArrowsArtist import ArrowsArtist
from CreatorView.GraphDetails.TreePasser import TreePasser
from utils import LogMessages
from utils.ButtonsFactory import ButtonsFactory

class DescriptionPanel(wx.Panel):
    def __init__(self, parent, spaceName, jsonDesc):
        wx.Panel.__init__(self,parent)
        self.spaceName = spaceName
        self.initRootSizer()

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.Add(self.newLogArea())
        rootSizer.AddSpacer(50)
        rootSizer.Add(self.newDescriptionArea())
        rootSizer.AddSpacer(50)
        self.SetSizer(rootSizer)
        rootSizer.Fit(self)

    def newLogArea(self):
        self.log_area = wx.TextCtrl(self, -1, size = (200, -1), style=wx.TE_MULTILINE | wx.TE_READONLY)
        return self.log_area

    def newDescriptionArea(self):
        self.descriptionArea =  wx.TextCtrl(self, -1, size = (200, 300), style=wx.TE_MULTILINE | wx.TE_READONLY)
        return self.descriptionArea

    def onEntityClicked(self, details, entityName):
        self.log_area.SetValue("Clicked: " + entityName)
        self.descriptionArea.SetValue(details[entityName])


class NetworkPanel(wx.Panel):

    def __init__(self, parent, space_name, size):
        wx.Panel.__init__(self, parent)
        self.space_name = space_name
        self.size = size
        self.parent = parent
        self.jsonDesc = self.neDefaultJSONDesc()
        self.G = None
        self.treeHeight = None
        self.pos = None
        self.main_axis = None
        self.axesDict = None
        self.details = None
        self.initRootSizer()

    def neDefaultJSONDesc(self):
        return {"Dwellers":[], "Buildings":[], "Resources":[]}

    def calcPopupWidth(self):
        return 3 * 50 + self.canvas.GetSize()[0] + self.descriptionPanel.GetSize()[0]

    def calcPopupHeight(self):
        return 3 * 50 + self.canvas.GetSize()[1]

    def initRootSizer(self):
        rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        rootSizer.AddSpacer(50)
        rootSizer.Add(self.newGraphSpaceSizer())
        rootSizer.AddSpacer(50)
        rootSizer.Add(self.newMenuSizer())
        rootSizer.AddSpacer(50)
        self.SetSizer(rootSizer)
        rootSizer.Fit(self)

    def newGraphSpaceSizer(self):
        graphSpaceSizer = wx.BoxSizer(wx.VERTICAL)
        graphSpaceSizer.AddSpacer(50)
        graphSpaceSizer.Add(self.newCanvas())
        graphSpaceSizer.AddSpacer(100)
        return graphSpaceSizer

    def newMenuSizer(self):
        menuSizer = wx.BoxSizer(wx.VERTICAL)
        menuSizer.AddSpacer(50)
        menuSizer.Add(self.newDescriptionPanel(), 1, flag= wx.CENTER)
        menuSizer.Add(self.newExitButton(), flag=wx.BOTTOM | wx.CENTER)
        return menuSizer

    def newDescriptionPanel(self):
        self.descriptionPanel = DescriptionPanel(self, self.space_name, self.jsonDesc)
        return self.descriptionPanel

    def newExitButton(self):
        return ButtonsFactory().newButton(self, "Exit",self.onExit,  hint=LogMessages.MENU_BTN_HINT)

    def onExit(self, event):
        self.parent.onExit()

    def newCanvas(self):
        self.canvas = FigCanvas(self, -1, plt.gcf())
        self.canvas.mpl_connect('button_press_event', self.onClick)
        return self.canvas

    def getRadius(self, event):
        xs, xe = event.inaxes.get_xlim()
        ys, ye = event.inaxes.get_ylim()
        xs_disp, ys_disp = event.inaxes.transData.transform((xs, ys))
        xe_disp, ye_disp = event.inaxes.transData.transform((xe, ye))
        return max(xe_disp - xs_disp, ye_disp - ys_disp) / 2

    def onClick(self, event):
        if self.G is None or self.pos is None or self.details is None: return
        if event.inaxes is self.main_axis: return
        self.detectClickedNode(
            event.inaxes.transData.transform((event.xdata, event.ydata)),
            self.getRadius(event)
        )

    def detectClickedNode(self, (x,y), radius):
        for node in self.G.nodes():
            nodePos = self.main_axis.transData.transform(self.pos[node])
            distance = sqrt(pow(x-nodePos[0],2)+pow(y-nodePos[1],2))
            if distance < radius:
                self.descriptionPanel.onEntityClicked(self.details, node)

    def newGraphFromJSON(self):
        G = nx.DiGraph()
        TreePasser().mountRec(G, self.jsonDesc)
        return G

    def fetchLabelsOfVertices(self, G):
        return {name: name for name in G.nodes()}

    def resetViewFromJSON(self, jsonGraphDesc):
        plt.clf()
        self.jsonDesc = jsonGraphDesc
        self.G = self.newGraphFromJSON()
        self.pos = graphviz_layout(self.G, prog='dot')
        self.axesDict = {}
        self.treeHeight = TreePasser().jsonTreeHeight(self.jsonDesc) - 1
        self.details = TreePasser().yieldDetails(self.jsonDesc)
        self.drawGraph()

    def drawGraph(self):
        self.performGraphDrawing()
        self.performLabelsDrawingFillingAxisDict()
        ArrowsArtist(main_axis=self.main_axis, pos=self.pos, axesDict=self.axesDict).addArrowsToGraph(self.G)

    def performGraphDrawing(self):
        nx.draw(self.G, self.pos, arrows = False)
        nx.draw_networkx_nodes(self.G, self.pos, node_color='w')
        self.main_axis = plt.gca()

    def performLabelsDrawingFillingAxisDict(self):
        labelsPosDict = self.drawNodesYieldingNewPos(self.G)
        if self.treeHeight <= 5:
            nx.draw_networkx_labels(
                self.G, labelsPosDict, self.fetchLabelsOfVertices(self.G), ax = self.main_axis, font_size=10
            )
            self.drawRectsRoundLabels(self.G,labelsPosDict)

    def getBBox(self, nodeName, label_x = 0, label_y = 0):
        txt = plt.gcf().text(label_x, label_y, nodeName, fontsize = 10)
        bbox = txt.get_window_extent(self.canvas.get_renderer())
        txt.remove()
        return bbox

    def drawRectsRoundLabels(self, G, labelsPosDict):
        for nodeName in G.nodes():
            label_x, label_y = \
                plt.gcf().transFigure.inverted().transform(
                    self.main_axis.transData.transform(labelsPosDict[nodeName])
                )
            bbox = self.getBBox(nodeName, label_x, label_y)
            plt.gcf().patches.append(
                Rectangle([bbox.x0 - bbox.width / 2, bbox.y0 - bbox.height / 4], bbox.width, bbox.height, color=[0, 0, 0], fill=False)
            )

    def getLabelHeight(self, nodeName):
        bbox = self.getBBox(nodeName)
        return self.main_axis.transData.inverted().transform((bbox.width, bbox.height))[1] - self.main_axis.get_ylim()[0]

    def drawNodesYieldingNewPos(self, G):
        newLabelsPos = {}
        for node in G.nodes():
            xa, ya = \
                plt.gcf().transFigure.inverted().transform(
                    self.main_axis.transData.transform(self.pos[node])
                )
            self.addImageAxis(xa, ya, img = G.node[node]['image'], nodeName= node, newLabelsPos=newLabelsPos)
        return newLabelsPos

    def addImageAxis(self, xa, ya, img, nodeName, newLabelsPos):
        imsize = max (0.04, 0.1 - 0.02 * (self.treeHeight - 1) / 5)
        self.axesDict[nodeName] = plt.axes([xa - imsize / 2.0, ya - imsize / 2.0, imsize, imsize]) # normalized units from (0,1)
        self.axesDict[nodeName].imshow( mpimg.imread(img) )
        self.axesDict[nodeName].axis('off')
        self.updateNewLabelsPos(newLabelsPos, nodeName)

    def updateNewLabelsPos(self, newLabelsPos, nodeName):
        xs, xe = self.axesDict[nodeName].get_xlim()
        ys, ye = self.axesDict[nodeName].get_ylim()
        xs_disp,ys_disp = self.main_axis.transData.inverted().transform(self.axesDict[nodeName].transData.transform((xs,ys)))
        xe_disp, ye_disp = self.main_axis.transData.inverted().transform(self.axesDict[nodeName].transData.transform([xe, ye]))
        newLabelsPos[nodeName] = self.pos[nodeName][0], ys_disp -  self.getLabelHeight(nodeName) / 2


class DetailsFrame(wx.Frame):
    def __init__(self, fromPanel,  spaceName,  size=wx.DefaultSize):
        wx.Frame.__init__(self, None, title='Details of ' + spaceName, size=size, style=wx.DEFAULT_FRAME_STYLE ^ (wx.CAPTION | wx.RESIZE_BORDER) ) #(wx.DEFAULT_FRAME_STYLE |
        self.ToggleWindowStyle(wx.STAY_ON_TOP)
        self.spaceName = spaceName
        self.fromPanel = fromPanel
        self.initView()
        self.detailsPanel = NetworkPanel(self, spaceName, size)
        self.SetSize((self.detailsPanel.calcPopupWidth(), self.detailsPanel.calcPopupHeight()))
        self.SetPosition((self.calculateCenter()))

    def calculateCenter(self):
        frame_width, frame_height = self.GetSize()
        desktop_width, desktop_height = wx.GetDisplaySize()
        return ((desktop_width - frame_width)/2, (desktop_height - frame_height)/2 )

    def initView(self):
        self.fromPanel.Disable()
        self.SetBackgroundColour((0,0,0))
        self.SetForegroundColour((255,255,255))

    def onAnimateShowing(self, event):
        self.SetFocus()
        if self.alpha >= 255:
            self.onPostAnimation()
            return
        self.SetTransparent(self.alpha)
        self.alpha += 5

    def onPostAnimation(self):
        self.alpha = 255
        self.timer.Stop()
        self.Enable()

    def setupAnimation(self):
        self.alpha = 0
        self.SetTransparent(0)
        self.timer = wx.Timer(self, wx.ID_ANY)
        self.fromPanel.Disable()
        self.Disable()
        self.Bind(wx.EVT_TIMER, self.onAnimateShowing)
        self.timer.Start(15, oneShot=False)

    def showDetailsFromJSON(self,jsonGraphDesc):
        self.detailsPanel.resetViewFromJSON(jsonGraphDesc)
        self.setupAnimation()
        self.Show()

    def onExit(self):
        self.fromPanel.Enable()
        self.Close()
        self.Destroy()