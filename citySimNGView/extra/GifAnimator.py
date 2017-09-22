import wx
import wx.animate

class MyPanel(wx.Panel):

    def __init__(self, parent, id):

        wx.Panel.__init__(self, parent, id)
        self.SetBackgroundColour("black")
        gif_fname = "C:\Users\Admin\Desktop\\galaxy_gif.gif"
        gif = wx.animate.GIFAnimationCtrl(self, id, gif_fname, pos=(10, 10))
        gif.GetPlayer().UseBackgroundColour(True)

        self.gif = gif
        self.CallMeLater(True)

    def CallMeLater(self, play=True):

        if play:
            self.gif.Play()
        else:
            self.gif.Stop()

app = wx.App(False)
frame = wx.Frame(None, -1, "wx.animate.GIFAnimationCtrl()", size = (200, 220))
MyPanel(frame, -1)
frame.Show(True)
app.MainLoop()