import wx

from utils.RelativePaths import relative_textures_path


class MainTab(wx.Panel):
    def __init__(self, parent, master, tabID):
        wx.Panel.__init__(self, parent, name="Tab"+str(tabID))
        self.parent = parent
        self.master = master
        self.centerSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.centerSizer)
        self.listCtrls = []
        self.indexList = []
        self.tabID = tabID
        self.isInitialized = False

        self.initContentList()

    def initContentList(self):
        """ This function creates content list and buttons, sets theirs positions and size and
            binds logic to them."""
        self.leftBox = wx.BoxSizer(wx.VERTICAL)
        self.middleBox = wx.BoxSizer(wx.VERTICAL)
        self.rightBox = wx.BoxSizer(wx.VERTICAL)
        self.contentBox = wx.BoxSizer(wx.HORIZONTAL)

        self.contentBox.Add(self.leftBox,0)
        self.contentBox.AddSpacer(50)
        self.contentBox.Add(self.middleBox,0)
        self.contentBox.AddSpacer(50)
        self.contentBox.Add(self.rightBox,0)

        self.centerSizer.Add(self.contentBox, 0, wx.CENTER) 
        self.centerSizer.AddSpacer(20)
        self.centerSizer.Layout()

    def fillListItem(self, i, font, box):
      #  listItem = self.listCtrls[i]
        if self.indexList[i] is not None:

            elemField = wx.StaticText(self, label=self.indexList[i]) #elemField = wx.StaticText(self, label=self.master.content[i])
            elemID = i + 100*self.tabID
            elemField.SetFont(font)
            arrowNew = wx.Bitmap(relative_textures_path+"arrow_green_head_small.png", wx.BITMAP_TYPE_ANY)
            arrowButton = wx.Button(self, id=elemID, 
                label="TabBtn"+str(elemID), 
                size=(arrowNew.GetWidth()+10, arrowNew.GetHeight()+5),
                style=wx.BU_NOTEXT)
            arrowButton.SetBitmap(arrowNew)
            self.Bind(wx.EVT_BUTTON, self.master.showPageView, arrowButton)

            tmpBox = wx.BoxSizer(wx.HORIZONTAL)
            tmpBox.Add(elemField, 0, wx.CENTER)
            tmpBox.AddSpacer(10)
            tmpBox.Add(arrowButton, 0, wx.CENTER)

            box.Add(tmpBox,0,wx.ALIGN_RIGHT)
            box.AddSpacer(10)

    def fillContentList(self, indexList):
        for i in range(len(self.leftBox.GetChildren())):
            self.leftBox.Hide(0, recursive=True)
            self.leftBox.Layout()
            self.leftBox.Remove(0)
            self.leftBox.Layout()
        for i in range(len(self.middleBox.GetChildren())):
            self.middleBox.Hide(0, recursive=True)
            self.middleBox.Layout()
            self.middleBox.Remove(0)
            self.middleBox.Layout()
        for i in range(len(self.rightBox.GetChildren())):
            self.rightBox.Hide(0, recursive=True)
            self.rightBox.Layout()
            self.rightBox.Remove(0)
            self.rightBox.Layout()

        listFont = self.master.tutorialFont
        listFont.SetPointSize(18)

        self.indexList = indexList
        contentSize = len(indexList)
        # if contentSize > self.master.maxNrOfItemsOnList:
        #     contentSize = self.master.maxNrOfItemsOnList

        contentOne = contentTwo = contentSize//3
        if contentSize % 3 >= 1:
            contentOne += 1
        if contentSize % 3 == 2:
            contentTwo +=1

        for i in range(contentOne):
            self.fillListItem(i, listFont, self.leftBox)

        for i in range(contentOne, contentOne+contentTwo):
            self.fillListItem(i, listFont, self.middleBox)

        for i in range(contentOne+contentTwo, contentSize):
            self.fillListItem(i, listFont, self.rightBox)

        self.leftBox.Layout()
        self.middleBox.Layout()
        self.rightBox.Layout()
        self.contentBox.Layout()
        self.centerSizer.Layout()
        self.Layout()
