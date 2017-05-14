import wx
from CreatorSwitcher import CreatorSwitcher

class Example(wx.Frame):
    def __init__(self, *args, **kw):
        screenDims = wx.GetDisplaySize()
        wx.Frame.__init__(self,None,-1,size = screenDims)
        CreatorSwitcher(self, screenDims, "")
        self.ShowFullScreen(True)
        self.Show()

def main():
    ex = wx.App()
    Example()
    ex.MainLoop()


if __name__ == '__main__':
    main()