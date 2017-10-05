import wx
import wx.animate

class MyPanel(wx.Panel):

    def __init__(self, parent, id, size):

        wx.Panel.__init__(self, parent, id, size)
        # self.SetBackgroundColour("black")

        self.parent = parent

        subpanel = wx.Panel(self)

        gif_fname = "C:\Users\Admin\Desktop\\giphy.gif"
        gif = wx.animate.GIFAnimationCtrl(subpanel, id, gif_fname)
        gif.GetPlayer().UseBackgroundColour(True)
        gif.Play()

        btn = wx.Button(gif, label = "btn")
        btn.Bind(wx.EVT_BUTTON, self.onClose)
        btn1 = wx.Button(gif, label = "btn1")

        rootSizer, verticalSizer = self.centeredSizers()

        sub_sizer_hor, sub_sizer_ver = self.centeredSizers()
        subpanel.SetSizer(sub_sizer_ver)
        gif_dim = gif.GetSize()

        print gif_dim, subpanel.GetSize()
        subpanel.SetBackgroundColour("white")

        sub_sizer_ver.Add(btn, flag = wx.CENTER)
        sub_sizer_ver.Add(btn1, flag= wx.CENTER)
        sub_sizer_ver.Add(gif, flag=wx.CENTER)

        verticalSizer.Add(subpanel, flag = wx.CENTER)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0,0,screenDims[0], screenDims[1])

    def centeredSizers(self):
        rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        rootSizer.AddStretchSpacer()
        rootSizer.Add(verticalSizer, flag = wx.CENTER)
        rootSizer.AddStretchSpacer()
        return rootSizer, verticalSizer

    def onClose(self, ev):
        self.parent.Close()
        self.parent.Destroy()

app = wx.App(False)
screenDims = wx.GetDisplaySize()
frame = wx.Frame(None, -1, "wx.animate.GIFAnimationCtrl()", size = (200, 220))
MyPanel(frame, -1, (200, 220))
frame.Show(True)
frame.ShowFullScreen(True)
app.MainLoop()