import wx
from wx.lib.scrolledpanel import ScrolledPanel

relative_textures_path = "..\\..\\resources\\Textures"

class View(ScrolledPanel):
    def __init__(self, parent):
        super(View, self).__init__(parent, size =(200,200),style = wx.SIMPLE_BORDER)
        self.SetupScrolling()
        firstLvl = ["farma.JPG", "bakery.png"]
        secondLvl = ["farma.JPG", "browar.JPG"]
        thirdLvl = ["Bakery.JPG"]
        tree = [firstLvl, secondLvl, thirdLvl]
        rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(rootSizer)
        self.drawTree(0,tree)

    def drawTree(self, lvl_index, tree):
        lvlSizer = wx.BoxSizer(wx.VERTICAL)
        for leaf in tree[lvl_index]:
            arrow_sizer = wx.BoxSizer(wx.HORIZONTAL)
            arrow_img = wx.Image(name = relative_textures_path + "graph_right_arrow.png")
            arrow_bmp =  wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(arrow_img), size = (32,32))

            image = wx.Image(name = relative_textures_path + leaf) #"..\\..\\resources\\Textures\\house.png"
            imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))

            arrow_sizer.Add(arrow_bmp)
            arrow_sizer.AddSpacer(10)
            arrow_sizer.Add(imageBitmap)

            lvlSizer.Add(arrow_sizer)
