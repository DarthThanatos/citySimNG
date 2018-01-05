import wx

from utils.RelativePaths import relative_textures_path

class MainTab(wx.Panel):
    def __init__(self, parent, master, tabID):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.master = master
        self.centerSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.centerSizer)
        self.listCtrls =[]
        self.indexList = []
        self.tabID = tabID
        self.isInitialized = False

        self.initContentList()

    def addListElem(self, font, arrow, i):
        elemField = wx.StaticText(self, label="                                          ") #elemField = wx.StaticText(self, label=self.master.content[i])
        elemID = i
        elemField.SetFont(font)
        arrowNew = wx.Bitmap(relative_textures_path+"new\\arrow_green_head_small.png", wx.BITMAP_TYPE_ANY)
        arrowButton = wx.Button(self, id=elemID, label="  ", 
            size=(arrowNew.GetWidth()+10, arrowNew.GetHeight()+5),
            name="Tab"+str(self.tabID)+"Button")
        arrowButton.SetBitmap(arrowNew)
        tmpBox = wx.BoxSizer(wx.HORIZONTAL)
        tmpBox.Add(elemField, 0, wx.CENTER)
        tmpBox.AddSpacer(10)
        tmpBox.Add(arrowButton,0)

        listItem = {'elemField': elemField, 'arrowButton': arrowButton, 'box': tmpBox}
        self.listCtrls.append(listItem)


    def initContentList(self):
        """ This function creates content list and buttons, sets theirs positions and size and
            binds logic to them."""
        self.leftBox = wx.BoxSizer(wx.VERTICAL)
        self.rightBox = wx.BoxSizer(wx.VERTICAL)
        self.contentBox = wx.BoxSizer(wx.HORIZONTAL)

        listFont = self.master.tutorialFont
        listFont.SetPointSize(18)

        contentSize = self.master.maxNrOfItemsOnList
        contentHalf = contentSize - (contentSize // 2)
        for i in range(contentHalf):
            self.addListElem(listFont, i)

        for i in range(contentHalf, contentSize):
            self.addListElem(listFont, i)

        self.contentBox.Add(self.leftBox,0)
        self.contentBox.AddSpacer(50)
        self.contentBox.Add(self.rightBox,0)
        self.centerSizer.Add(self.contentBox, 0, wx.CENTER) 
        self.centerSizer.AddSpacer(20)
        self.centerSizer.Layout()

    def fillListItem(self, i, box):
        print "Filling listItem"
        print "i: " + str(i)
        listItem = self.listCtrls[i]
        if self.indexList[i] is not None:
            #print "Lable type: " + str(type(self.indexList[i]))
           # print "Lable : " + str(self.indexList[i]) + "\n"
            listItem['elemField'].SetLabel(self.indexList[i])
            listItem['arrowButton'].SetId(i + 10*self.tabID)
            self.Bind(wx.EVT_BUTTON, self.master.showPageView, listItem['arrowButton'])
            listItem['box'].Layout()

            #tu bede dodawala tmpbox
            box.Add(tmpBox,0,wx.CENTER)
            box.AddSpacer(20)
        else:
            #listItem['box'].ShowItems(False)
            #listItem['box'].Layout()
            listItem['elemField'].SetLabel("")
            listItem['arrowButton'].SetLabel("")
            listItem['arrowButton'].Hide()
            listItem['box'].Layout()

    def fillContentList(self, indexList):
        print "\nFilling content list"
        self.leftBox.Clear()
        self.rightBox.Clear()

        self.indexList = indexList
        contentSize = len(indexList)
        if contentSize > self.master.maxNrOfItemsOnList:
            contentSize = self.master.maxNrOfItemsOnList
        contentHalf = contentSize - (contentSize // 2)
        for i in range(contentHalf):
            self.fillListItem(i, self.leftBox)

        for i in range(contentHalf, contentSize):
            self.fillListItem(i, self.rightBox)
        self.leftBox.Layout()
        self.rightBox.Layout()
        self.contentBox.Layout()
        self.centerSizer.Layout()
        self.Layout()
