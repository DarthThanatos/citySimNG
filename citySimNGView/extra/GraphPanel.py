import wx
from wx.lib.scrolledpanel import ScrolledPanel
import traceback

relative_textures_path = "..\\..\\resources\\Textures\\"

class View(ScrolledPanel):
    def __init__(self, parent):
        super(View, self).__init__(parent, size =(750,500),style = wx.SIMPLE_BORDER)
        self.SetupScrolling()
        firstLvl = ["farma.JPG", "bakery.png"]
        secondLvl = ["farma.JPG", "browar.JPG", "house.png"]
        thirdLvl = ["farma.JPG", "browar.JPG"]
        tree = [ firstLvl, secondLvl, thirdLvl, firstLvl]
        #tree = [["pszenica.jpg"], ["maka.jpg"], ["chleb.jpg"],["gold.jpg"]]
        rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(rootSizer)
        rootSizer.AddStretchSpacer()
        self.drawTree(0,tree, rootSizer)
        rootSizer.AddStretchSpacer()
        rootSizer.Layout()
        self.rootSizer = rootSizer
        self.Bind(wx.EVT_SIZE, self.onResize)

    def onResize(self, evt):
        self.rootSizer.Layout()
        self.Layout()
        self.SetupScrolling()

    def drawTree(self, lvl_index, tree, parent_horizontal_sizer):
        lvlVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        try:
            #rotation_angle = (3.14 / 4) if (tree[lvl_index].__len__() == 1) else 0
            #delta_angle = - 3.14 / 2 * 1 / tree[lvl_index].__len__() if tree[lvl_index].__len__() != 1 else 0
            for i, leaf in enumerate(tree[lvl_index]):
                lvlHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
                #print leaf
                arrow_sizer = wx.BoxSizer(wx.HORIZONTAL)
                arrow_img = wx.Image(name = relative_textures_path + ("graph_right_arrow.png" if lvl_index % 2 == 0 else "rightBlueArrow.png"))
                arrow_img = arrow_img.Scale(32,32)
                #arrow_img_centre = wx.Point(arrow_img.GetWidth() / 2, arrow_img.GetHeight() / 2)

                #arrow_img.SetMaskColour(r=1, g=1, b=1)
                #arrow_img = arrow_img.Rotate(angle = rotation_angle, interpolating = False, centre_of_rotation = arrow_img_centre)
                arrow_bmp =  wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(arrow_img), size = (32,32))

                image = wx.Image(name = relative_textures_path + leaf) #"..\\..\\resources\\Textures\\house.png"
                image = image.Scale(32,32)
                imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))

                arrow_sizer.Add(arrow_bmp)
                arrow_sizer.AddSpacer(10)
                arrow_sizer.Add(imageBitmap)

                lvlHorizontalSizer.Add(arrow_sizer, 0, wx.CENTER)
                lvlHorizontalSizer.AddSpacer(10)
                if lvl_index != tree.__len__() - 1:
                    ln = wx.StaticLine(self, -1, style = wx.VERTICAL)
                    #lvlHorizontalSizer.Add(ln, 0, wx.EXPAND)
                    lvlHorizontalSizer.AddSpacer(10)
                self.drawTree(lvl_index + 1, tree, lvlHorizontalSizer)

                lvlVerticalSizer.Add(lvlHorizontalSizer, 0, wx.CENTER)
                lvlVerticalSizer.AddSpacer(2 * (lvl_index + 1))
                if i != tree[lvl_index].__len__() - 1:
                    ln = wx.StaticLine(self, -1)
                    #lvlVerticalSizer.Add(ln, 0, wx.EXPAND)
                    lvlVerticalSizer.AddSpacer(10)
                #rotation_angle += delta_angle
            parent_horizontal_sizer.Add(lvlVerticalSizer,0, wx.CENTER)
            parent_horizontal_sizer.AddSpacer(10)
        except Exception: #mainly KeyError
            #traceback.print_exc()
            pass