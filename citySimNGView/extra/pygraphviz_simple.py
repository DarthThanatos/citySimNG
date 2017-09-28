#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pygraphviz as pgv
import wx


class GraphImgPanel(wx.Panel):
    def __init__(self, parent, size):
        wx.Panel.__init__(self, parent = parent, size = size)
        self.size = size
        rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddStretchSpacer()
        rootSizer.Add(verticalSizer, flag = wx.CENTER)
        rootSizer.AddStretchSpacer()
        verticalSizer.Add(self.newScaledImgBitmap("resources\\sysFiles\\graphFiles\\simple.png"), flag = wx.CENTER)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, size[0], size[1])

    def newScaledImg(self, non_relative_path):
        image = wx.Image(name = non_relative_path) #"..\\..\\resources\\Textures\\DefaultBuilding.jpg"
        return image.Scale(self.size[0], self.size[1]) if self.size != wx.DefaultSize else image

    def newScaledImgBitmap(self, non_relative_path):
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(self.newScaledImg(non_relative_path)), size = self.size)

class MainFrame(wx.Frame):
    def __init__(self, size = wx.DefaultSize):
        print "size = ", size
        wx.Frame.__init__(self, None, title='Test', size = size)
        GraphImgPanel(self, size)


def initNode(G, id, img, label):
    n = G.get_node(id)
    n.attr["shape"]="box"
    n.attr["image"] = img
    # n.attr["imagepos"]= "tc"
    n.attr["xlabel"] = label
    # n.attr["labelloc"] = "b"

def addSubGraph(A, n):
    A.add_edge(1 + n,2 + n)
    A.add_edge(1 + n,4 + n)
    A.add_edge(3+ n,5 +n)
    A.add_edge(1 +n,3+n)

A=pgv.AGraph()
addSubGraph(A, 0)
addSubGraph(A, 5)
addSubGraph(A, 10)

for i in range(1,14):
    initNode(A, id=str(i), img="resources\Textures\dweller.JPG",label="dweller")

print(A.string()) # print to screen

# B=pgv.AGraph('resources\sysFiles\graphFiles\simple.dot') # create a new graph from file
A.layout() # layout with default (neato)
A.draw('resources\sysFiles\graphFiles\simple.png') # draw png
print("Wrote simple.png")

app = wx.App(False)
screenDims = wx.GetDisplaySize()
frm = MainFrame(size=screenDims)
# frm.ShowFullScreen(True)
frm.Show()
app.MainLoop()
