import wx
import wx.animate

class MyPanel(wx.Panel):

    def __init__(self, parent, id, size):

        wx.Panel.__init__(self, parent, id, size)
        self.SetBackgroundColour("black")

        gif_fname = "C:\Users\Admin\Desktop\\giphy.gif"
        gif = wx.animate.GIFAnimationCtrl(self, id, gif_fname, size =  wx.GetDisplaySize())
        gif.GetPlayer().UseBackgroundColour(True)
        gif.Play()
        btn = wx.Button(gif, label = "btn")

app = wx.App(False)
frame = wx.Frame(None, -1, "wx.animate.GIFAnimationCtrl()", size = (200, 220))
MyPanel(frame, -1, (200, 220))
frame.Show(True)
frame.ShowFullScreen(True)
app.MainLoop()