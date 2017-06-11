import wx
from wx.lib.scrolledpanel import ScrolledPanel
import traceback
from RelativePaths import relative_textures_path
import json

class GraphPanel(ScrolledPanel):
    def __init__(self, parent, space_name):
        super(GraphPanel, self).__init__(parent, size =(500,500),style = wx.SIMPLE_BORDER)
        self.space_name = space_name
        self.rootSizer = wx.BoxSizer(wx.VERTICAL)

        description_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        description_label = wx.StaticText(self, -1, self.space_name)
        description_label_sizer.Add(description_label,0,wx.CENTER)
        self.rootSizer.Add(description_label_sizer, 0, wx.CENTER)

        self.SetSizer(self.rootSizer)
        self.tree = [[],[],[]]
        self.jsonDesc = {"Dwellers":[], "Buildings":[], "Resources":[]}
        self.Bind(wx.EVT_SHOW, self.onShow, self)


    def onShow(self, ev):
        if ev.GetShow():
            print self.space_name, "on show in graph panel"
            print json.dumps(self.jsonDesc, indent = 4)
            self.resetViewFromJSON()

    def resetViewFromJSON(self):
        self.rootSizer.Clear(True)
        description_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        description_label = wx.StaticText(self, -1, self.space_name)
        description_label_sizer.Add(description_label,0,wx.CENTER)

        rootVerticalSizer = self.rootSizer
        rootVerticalSizer.Add(description_label_sizer, 0, wx.CENTER)
        rootVerticalSizer.AddSpacer(20)

        container_vertical_sizer = wx.BoxSizer(wx.VERTICAL)
        for tree in self.jsonDesc:
            self.drawJSONTree(0, tree, container_vertical_sizer)

        rootVerticalSizer.Add(container_vertical_sizer, 0,wx.CENTER)
        rootVerticalSizer.Layout()
        self.SetupScrolling()

    def drawJSONTree(self, lvl_index, tree, parent_vertical_sizer):
        try:
            arrow_sizer = wx.BoxSizer(wx.HORIZONTAL)
            arrow_img = wx.Image(name = relative_textures_path + ("graph_right_arrow.png" if lvl_index % 2 == 0 else "rightBlueArrow.png"))
            arrow_img = arrow_img.Scale(32,32)
            arrow_bmp =  wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(arrow_img), size = (32,32))

            image = wx.Image(name = tree["Texture path"]) #"..\\..\\resources\\Textures\\house.png"
            image = image.Scale(32,32)
            imageBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(image), size = (32,32))

            arrow_sizer.Add(arrow_bmp)
            arrow_sizer.AddSpacer(10)
            arrow_sizer.Add(imageBitmap)

            lvlHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
            lvlHorizontalSizer.Add(arrow_sizer, 0,wx.CENTER)
            lvlHorizontalSizer.AddSpacer(10)

            lvlVerticalSizer = wx.BoxSizer(wx.VERTICAL)

            for child in tree["Children"]:
                self.drawJSONTree(lvl_index + 1, child, lvlVerticalSizer)

            lvlHorizontalSizer.Add(lvlVerticalSizer, 0,wx.CENTER)

            parent_vertical_sizer.Add(lvlHorizontalSizer)
            parent_vertical_sizer.AddSpacer(10)
        except Exception:
            traceback.print_exc()

    def resetView(self):
        self.rootSizer.Clear(True)
        description_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        description_label = wx.StaticText(self, -1, self.space_name)
        description_label_sizer.Add(description_label,0,wx.CENTER)

        rootHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        rootVerticalSizer = self.rootSizer
        self.SetSizer(rootVerticalSizer)
        #rootHorizontalSizer.AddStretchSpacer()
        self.drawTree(0, self.tree, rootHorizontalSizer)
        #rootHorizontalSizer.AddStretchSpacer()

        rootVerticalSizer.Add(description_label_sizer, 0, wx.CENTER)
        rootVerticalSizer.AddSpacer(10)
        rootVerticalSizer.Add(rootHorizontalSizer, 0, wx.CENTER | wx.ALL, 15)
        rootVerticalSizer.Layout()
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

