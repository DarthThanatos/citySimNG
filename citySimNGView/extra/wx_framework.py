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
        verticalSizer.Add(wx.StaticText(self, label = "Below lies logging area, showing error msgs"), flag = wx.CENTER)
        self.SetSizer(rootSizer)
        rootSizer.SetDimension(0, 0, size[0], size[1])

    def newScaledImg(self, non_relative_path):
        image = wx.Image(name = non_relative_path) #"..\\..\\resources\\Textures\\DefaultBuilding.jpg"
        return image.Scale(self.size[0], self.size[1]) if self.size != wx.DefaultSize else image

    def newScaledImgBitmap(self, non_relative_path):
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(self.newScaledImg(non_relative_path)), size = self.size)

class MainFrame(wx.Frame):
    def __init__(self, size = wx.DefaultSize):
        wx.Frame.__init__(self, None, title='Test', size = size)
        GraphImgPanel(self, size)


app = wx.App(False)
screenDims = wx.GetDisplaySize()
frm = MainFrame()
# frm.ShowFullScreen(True)
frm.Show()
app.MainLoop()
