import wx
import pygame
from bgCreatorView.CreatorView import CreatorView
from MenuView import MenuView
from ExchangeView import ExchangeView
from MapView import MapView

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, strTitle, tplSize):
        wx.Frame.__init__(self, parent, ID, strTitle, size = tplSize)
        self.views = {
            "Menu": MenuView(self,tplSize,"Menu"),
            "Creator": CreatorView(self,tplSize,"Creator"), 
            "Exchange": ExchangeView(self,tplSize, "Exchange"),
            "Map": MapView(self,tplSize,"Map")
        }
        self.setView("Menu")
        self.ShowFullScreen(True)


    def setView(self, viewName):
        for name in self.views:
            if name == viewName:    
                self.views[name].Show()
            else:
                self.views[name].Hide()

    def closeWindow(self,event):
        self.Destroy()

app = wx.PySimpleApp()
screenDims = wx.GetDisplaySize()

try:
    pygame.mixer.init()
    pygame.mixer.music.load("TwoMandolins.mp3")
    pygame.mixer.music.play()
except Exception:
    print "problem with music"

frame = MyFrame(None, wx.ID_ANY, "SDL Frame", screenDims)
frame.Show()
print "showing app"
app.MainLoop()


