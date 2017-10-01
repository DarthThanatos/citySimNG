from math import pi, tan, sqrt, atan
import matplotlib.lines as mlines

class ArrowsArtist(object):

    def __init__(self, main_axis, pos, axesDict):
        self.main_axis = main_axis
        self.pos = pos
        self.axesDict = axesDict

    def angleToRad(self, angle):
        return pi / 180 * angle

    def k(self, r, gamma):
        return r / sqrt(1 / pow(tan(gamma), 2) + 1)

    def xFromY(self, y, xlim, ylim, gamma):
        return (y - ylim) / tan(gamma) + xlim

    def arrowLine(self, r, gamma, xlim, ylim):
        if gamma != pi / 2:
            y = ylim + self.k(r, gamma)
            x = self.xFromY(y, xlim, ylim, gamma)
        else:
            x = xlim
            y = ylim + r
        self.drawLine(xlim, x, ylim, y)

    def drawLine(self, x1, x2, y1, y2):
        l = mlines.Line2D([x1, x2], [y1, y2], color="black", linewidth=1)
        self.main_axis.add_line(l)

    def startEndPoints(self, edge):
        n1, n2 = edge
        return self.pos[n1], self.pos[n2]

    def r(self, edge, arrowLength=0.125):
        (xs, ys), (xe, ye) = self.startEndPoints(edge)
        edgeLength = sqrt(pow(xs - xe, 2) + pow(ys - ye, 2))
        return edgeLength * arrowLength

    def radBeta(self, edge):
        (xs, ys), (xe, ye) = self.startEndPoints(edge)
        return atan((ye - ys) / (xe - xs)) if xe - xs != 0 else pi / 2

    def yLim(self, endNode):
        ax = self.axesDict[endNode]
        (ylim_neg, ylim_pos) = self.main_axis.transData.inverted().transform(ax.transData.transform(ax.get_ylim()))
        return ylim_pos

    def xLim(self, y_lim, edge):
        (xs, ys), (xe, ye) = self.startEndPoints(edge)
        return (y_lim - ys + (ye - ys) / (xe - xs) * xs) * (xe - xs) / (ye - ys) if xs != xe and ys != ye else xe

    def addArrowTo(self, (n1, n2), r, alpha=10):
        rad_beta = self.radBeta((n1, n2))
        rad_alpha = self.angleToRad(alpha)
        y_lim = self.yLim(n2)
        x_lim = self.xLim(y_lim, (n1, n2))
        self.arrowLine(r, rad_beta - rad_alpha, x_lim, y_lim)
        self.arrowLine(r, rad_beta + rad_alpha, x_lim, y_lim)

    def findMinR(self, G):
        return min([self.r(edge) for edge in G.edges()])

    def addArrowsToGraph(self, G):
        if G.edges().__len__() == 0: return
        r = self.findMinR(G)
        for e in G.edges():
            self.addArrowTo(e, r)