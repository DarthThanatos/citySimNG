import threading

import time
import wx
import wx.animate


class LoadingPanel(wx.Panel):

    def __init__(self, parent, gif_path):
        wx.Panel.__init__(self, parent)
        self.gif_path = gif_path
        self.parent = parent
        self.initRootSizer()

    def initRootSizer(self):
        screenDims = wx.GetDisplaySize()
        rootSizer = self.newRootSizer()
        rootSizer.SetDimension(0,0,screenDims[0], screenDims[1])
        self.SetSizer(rootSizer)

    def newRootSizer(self):
        rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        rootSizer.AddStretchSpacer()
        rootSizer.Add(self.newCenteredVerticalSizer(), flag = wx.CENTER)
        rootSizer.AddStretchSpacer()
        return rootSizer

    def newCenteredVerticalSizer(self):
        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        verticalSizer.Add(self.newGifCtrl(), flag = wx.CENTER)
        return verticalSizer

    def newGifCtrl(self):
        gif = wx.animate.GIFAnimationCtrl(self, wx.ID_ANY, self.gif_path)
        gif.GetPlayer().UseBackgroundColour(True)
        gif.Play()
        return gif


class LoadingScreen(wx.Frame):
    def __init__(self, gif_path):
        wx.Frame.__init__(self, None, -1)
        LoadingPanel(self, gif_path)
        self.ShowFullScreen(True)
        self.SetBackgroundColour((0,0,0))

    def closeWindow(self):
        threading._start_new_thread(self.delayClosing, ())

    def delayClosing(self):
        time_to_wait = (255*25/5.) / 1000
        time.sleep(time_to_wait)
        wx.CallAfter(self.Close)
        wx.CallAfter(self.Destroy)


if __name__ == "__main__":
    app = wx.App(False)
    loading_screen = LoadingScreen( "..\\resources\\sysFiles\\images\\loading.gif" )
    loading_screen.Show(True)
    loading_screen.ShowFullScreen(True)
    app.MainLoop()