
import wx
from wx.lib.scrolledpanel import ScrolledPanel

from CreatorView.GraphDetails.GraphDetails import DetailsFrame
from RelativePaths import relative_textures_path
from utils import LogMessages
from utils.ButtonsFactory import ButtonsFactory
from Consts import GRAPH_SPACE_PADDING


class GraphPanel(ScrolledPanel):
    def __init__(self, parent, space_name):
        super(GraphPanel, self).__init__(parent, size =((wx.GetDisplaySize()[0]-GRAPH_SPACE_PADDING) / 3,500),style = wx.SIMPLE_BORDER)
        self.space_name = space_name
        self.parent = parent
        self.jsonDesc = {"Dwellers":[], "Buildings":[], "Resources":[]}
        self.initRootSizer()
        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def initRootSizer(self):
        self.rootSizer = wx.BoxSizer(wx.VERTICAL)
        self.rootSizer.Add(self.newHeaderSizer(), 0, wx.CENTER)
        self.SetSizer(self.rootSizer)

    def newHeaderSizer(self):
        header_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.parent.addToSizerWithSpace(header_sizer, self.newDescriptionLabel(), space=20)
        header_sizer.Add(self.newDetailsButton(), flag=wx.CENTER)
        return header_sizer

    def newDetailsButton(self):
        self.detailsButton =  ButtonsFactory().newButton(
            self, "Show details", self.onShowDetails, hint=LogMessages.GRAPH_DETAILS_BTN_HINT
        )
        self.detailsButton.Enable(False)
        return self.detailsButton

    def onShowDetails(self, event):
        DetailsFrame(self, self.space_name).showDetailsFromJSON(self.jsonDesc)

    def newDescriptionLabel(self):
        return wx.StaticText(self, -1, self.space_name)

    def triggerGraphResetFromJSON(self,jsonGraphDesc):
        self.jsonDesc = jsonGraphDesc[self.space_name]
        self.Hide(); self.Show()

    def onShow(self, ev):
        if ev.GetShow():
            self.resetViewFromJSON()

    def setupDetailsButton(self):
        self.detailsButton.Enable(self.jsonDesc != [])

    def resetViewFromJSON(self):
        self.setupRootSizer()
        self.setupDetailsButton()
        self.SetupScrolling()

    def setupRootSizer(self):
        self.rootSizer.Clear(True)
        rootVerticalSizer = self.rootSizer
        self.parent.addToSizerWithSpace(rootVerticalSizer, self.newHeaderSizer(), space=20)
        rootVerticalSizer.Add(self.newJSONTreeLvlVerticalSizer(0, self.jsonDesc), 0, wx.CENTER)
        rootVerticalSizer.Layout()

    def newJSONTreeLvlVerticalSizer(self, lvl_index, childrenJSONDesc):
        lvlVerticalSizer = wx.BoxSizer(wx.VERTICAL)
        self.attachHorizontalBranchesToSizer(lvlVerticalSizer, childrenJSONDesc, lvl_index)
        return lvlVerticalSizer

    def attachHorizontalBranchesToSizer(self, root, childrenJsonDesc, root_lvl):
        for childJsonDesc in childrenJsonDesc:
            self.parent.addToSizerWithSpace(
                root, self.newTreeLvlHorizontalSizer(root_lvl, childJsonDesc), alignment=wx.LEFT
            )

    def newScaledBmp(self, imagePath):
        img = wx.Image(name = imagePath)
        img = img.Scale(32,32)
        return wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(img), size = (32,32))

    def newArrowBmp(self, lvl_index):
        return self.newScaledBmp(
            relative_textures_path + ("graph_right_arrow.png" if lvl_index % 2 == 0 else "rightBlueArrow.png")
        )

    def newEntityBmp(self, tree_lvl_json_desc):
        return self.newScaledBmp(tree_lvl_json_desc["Texture path"])

    def newTreeLvlImagesSizer(self, lvl_index, tree):
        tree_lvl_images_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.parent.addToSizerWithSpace(tree_lvl_images_sizer, self.newArrowBmp(lvl_index))
        tree_lvl_images_sizer.Add(self.newEntityBmp(tree))
        return tree_lvl_images_sizer

    def newTreeLvlHorizontalSizer(self, lvl_index, tree_lvl_json_desc):
        lvlHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.parent.addToSizerWithSpace(lvlHorizontalSizer, self.newTreeLvlImagesSizer(lvl_index, tree_lvl_json_desc))
        lvlHorizontalSizer.Add(self.newJSONTreeLvlVerticalSizer(lvl_index + 1, tree_lvl_json_desc["Children"]), 0, wx.CENTER)
        return lvlHorizontalSizer