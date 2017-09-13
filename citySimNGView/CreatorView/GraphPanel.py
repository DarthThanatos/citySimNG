import wx
from wx.lib.scrolledpanel import ScrolledPanel
from RelativePaths import relative_textures_path

class GraphPanel(ScrolledPanel):
    def __init__(self, parent, space_name):
        super(GraphPanel, self).__init__(parent, size =(500,500),style = wx.SIMPLE_BORDER)
        self.space_name = space_name
        self.tree = [[],[],[]]
        self.jsonDesc = {"Dwellers":[], "Buildings":[], "Resources":[]}
        self.initRootSizer()
        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def initRootSizer(self):
        self.rootSizer = wx.BoxSizer(wx.VERTICAL)
        self.rootSizer.Add(self.newDescriptionLabelSizer(), 0, wx.CENTER)
        self.SetSizer(self.rootSizer)

    def newDescriptionLabelSizer(self):
        description_label_sizer = wx.BoxSizer(wx.HORIZONTAL)
        description_label_sizer.Add(self.newDescriptionLabel(),0,wx.CENTER)
        return description_label_sizer

    def newDescriptionLabel(self):
        return wx.StaticText(self, -1, self.space_name)

    def triggerGraphResetFromJSON(self,jsonGraphDesc):
        self.jsonDesc = jsonGraphDesc[self.space_name]
        self.Hide()
        self.Show()

    def onShow(self, ev):
        if ev.GetShow():
            self.resetViewFromJSON()

    def resetViewFromJSON(self):
        self.rootSizer.Clear(True)
        rootVerticalSizer = self.rootSizer
        rootVerticalSizer.Add(self.newDescriptionLabelSizer(), 0, wx.CENTER)
        rootVerticalSizer.AddSpacer(20)
        rootVerticalSizer.Add(self.newJSONTreeLvlVerticalSizer(0, self.jsonDesc), 0, wx.CENTER)
        rootVerticalSizer.Layout()
        self.SetupScrolling()

    def newJSONTreeLvlVerticalSizer(self, lvl_index, childrenJSONDesc):
        lvlVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.attachHorizontalBranchesToSizer(lvlVerticalSizer, childrenJSONDesc, lvl_index)
        return lvlVerticalSizer

    def attachHorizontalBranchesToSizer(self, root, childrenJsonDesc, root_lvl):
        for childJsonDesc in childrenJsonDesc:
            root.Add(self.newTreeLvlHorizontalSizer(root_lvl, childJsonDesc))
            root.AddSpacer(10)

    def newScaledBmp(self, imagePath):
        img = wx.Image(name = imagePath)
        img = img.Scale(32,32)
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img), size = (32,32))

    def newArrowBmp(self, lvl_index):
        return self.newScaledBmp(relative_textures_path + ("graph_right_arrow.png" if lvl_index % 2 == 0 else "rightBlueArrow.png"))

    def newEntityBmp(self, tree_lvl_json_desc):
        return self.newScaledBmp(tree_lvl_json_desc["Texture path"])

    def newTreeLvlImagesSizer(self, lvl_index, tree):
        tree_lvl_images_sizer = wx.BoxSizer(wx.HORIZONTAL)
        tree_lvl_images_sizer.Add(self.newArrowBmp(lvl_index))
        tree_lvl_images_sizer.AddSpacer(10)
        tree_lvl_images_sizer.Add(self.newEntityBmp(tree))
        return tree_lvl_images_sizer

    def newTreeLvlHorizontalSizer(self, lvl_index, tree_lvl_json_desc):
        lvlHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        lvlHorizontalSizer.Add(self.newTreeLvlImagesSizer(lvl_index, tree_lvl_json_desc), 0, wx.CENTER)
        lvlHorizontalSizer.AddSpacer(10)
        lvlHorizontalSizer.Add(self.newJSONTreeLvlVerticalSizer(lvl_index + 1, tree_lvl_json_desc["Children"]), 0, wx.CENTER)
        return lvlHorizontalSizer