import os
import wx
from CreatorView import CreatorView
from MenuView import MenuView
from ExchangeView import ExchangeView
from MapView import MapView
import pygame


class MyFrame(wx.Frame):
    def __init__(self, parent, ID, strTitle, tplSize):
        wx.Frame.__init__(self, parent, ID, strTitle, size=tplSize)

        self.views = {
            "Menu": MenuView(self, tplSize, "Menu", "NWN2.mp3"),
            "Creator": CreatorView(self, tplSize, "Creator", "Ret Xed OST.mp3"),
            "Exchange": ExchangeView(self, tplSize, "Exchange"),
            "Map": MapView(self, tplSize, "Map")
        }

        for name in self.views:
            self.views[name].Hide()
        # ^ hiding every view, so they will react on Show() later
        # (otherwise the first view to run will be inactive, i.e. no
        # EVT_SHOW event shall be triggered for the first view to  be seen)
        
        self.ShowFullScreen(True)
        self.setView("Menu")

    def setView(self, viewName):
        objToRun = None
        for name in self.views:
            if name == viewName:    
                objToRun = self.views[name]
            else:
                self.views[name].Hide()
        objToRun.Show()

    def closeWindow(self, event):
        self.Destroy()

app = wx.PySimpleApp()
screenDims = wx.GetDisplaySize()

frame = MyFrame(None, wx.ID_ANY, "SDL Frame", screenDims)
frame.Show()
app.MainLoop()


