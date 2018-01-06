import wx

from utils.RelativePaths import relative_textures_path


class MainTab(wx.Panel):
    def __init__(self, parent, master, tabID):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.master = master
        self.centerSizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.centerSizer)
        self.listCtrls = []
        self.indexList = []
        self.tabID = tabID
        self.isInitialized = False

        self.initContentList()

    def addListElem(self, font, i):
        #print("Add list item: " + str(i))
        elemField = wx.StaticText(self, label="                         ") #elemField = wx.StaticText(self, label=self.master.content[i])
        elemID = i
        elemField.SetFont(font)
        arrowNew = wx.Bitmap(relative_textures_path+"new\\arrow_green_head_small.png", wx.BITMAP_TYPE_ANY)
        arrowButton = wx.Button(self, id=elemID, label="  ", 
            size=(arrowNew.GetWidth()+10, arrowNew.GetHeight()+5),
            name="Tab"+str(self.tabID)+"Button")
        arrowButton.SetBitmap(arrowNew)

        listItem = {'elemField': elemField, 'arrowButton': arrowButton}
        self.listCtrls.append(listItem)

    def initContentList(self):
        """ This function creates content list and buttons, sets theirs positions and size and
            binds logic to them."""
        self.leftBox = wx.BoxSizer(wx.VERTICAL)
        self.middleBox = wx.BoxSizer(wx.VERTICAL)
        self.rightBox = wx.BoxSizer(wx.VERTICAL)
        self.contentBox = wx.BoxSizer(wx.HORIZONTAL)

        listFont = self.master.tutorialFont
        listFont.SetPointSize(18)

        contentSize = self.master.maxNrOfItemsOnList

        for i in range(contentSize):
            self.addListElem(listFont, i)

        self.contentBox.Add(self.leftBox,0)
        self.contentBox.AddSpacer(50)
        self.contentBox.Add(self.middleBox,0)
        self.contentBox.AddSpacer(50)
        self.contentBox.Add(self.rightBox,0)

        self.centerSizer.Add(self.contentBox, 0, wx.CENTER) 
        self.centerSizer.AddSpacer(20)
        self.centerSizer.Layout()

    def fillListItem(self, i, box):
        listItem = self.listCtrls[i]
        if self.indexList[i] is not None:
            #print "Lable type: " + str(type(self.indexList[i]))
           # print "Lable : " + str(self.indexList[i]) + "\n"

            # print "Filling listItem"
            # print "i: " + str(i)+", title = "+str(self.indexList[i])

            listItem['elemField'].SetLabel(self.indexList[i])
            listItem['arrowButton'].SetId(i + 100*self.tabID)
            self.Bind(wx.EVT_BUTTON, self.master.showPageView, listItem['arrowButton'])

            tmpBox = wx.BoxSizer(wx.HORIZONTAL)
            tmpBox.Add(listItem['elemField'], 0, wx.CENTER)
            tmpBox.AddSpacer(10)
            tmpBox.Add(listItem['arrowButton'], 0, wx.CENTER)

            box.Add(tmpBox,0,wx.ALIGN_RIGHT)
            box.AddSpacer(10)

    def fillContentList(self, indexList):
        # print "\nFilling content list"
        self.leftBox.Clear()
        self.middleBox.Clear()
        self.rightBox.Clear()


        for i in range(len(self.leftBox.GetChildren())):
            self.leftBox.Hide(child.Window)
            self.leftBox.Detach(child.Window)
            self.leftBox.Layout()
        for i in range(len(self.middleBox.GetChildren())):
            self.leftBox.Hide(child.Window)
            self.leftBox.Detach(child.Window)
            self.middleBox.Layout()
        for i in range(len(self.rightBox.GetChildren())):
            self.leftBox.Hide(child.Window)
            self.leftBox.Detach(child.Window)
            self.rightBox.Layout()

        self.indexList = indexList
        print("indexList:")
        print(self.indexList)
        contentSize = len(indexList)
        if contentSize > self.master.maxNrOfItemsOnList:
            contentSize = self.master.maxNrOfItemsOnList

        contentOne = contentTwo = contentSize//3
        if contentSize % 3 >= 1:
            contentOne += 1
        if contentSize % 3 == 2:
            contentTwo +=1

        #contentHalf = contentSize - (contentSize // 2)
        for i in range(contentOne):
            self.fillListItem(i, self.leftBox)

        for i in range(contentOne, contentOne+contentTwo):
            self.fillListItem(i, self.middleBox)

        for i in range(contentOne+contentTwo, contentSize):
            self.fillListItem(i, self.rightBox)

        self.leftBox.Layout()
        self.middleBox.Layout()
        self.rightBox.Layout()
        self.contentBox.Layout()
        self.centerSizer.Layout()
        self.Layout()
