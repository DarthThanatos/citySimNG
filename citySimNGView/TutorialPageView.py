import wx
import wx.lib.agw.hyperlink as hl
from utils.RelativePaths import relative_music_path, relative_textures_path, relative_fonts_path


class TutorialPageView(wx.Panel):
    def __init__(self, parent, size, name, musicPath=relative_music_path + "TwoMandolins.mp3", sender = None):
        wx.Panel.__init__(self, size=size, parent=parent)
        self.parent = parent
        self.name = name
        self.sender = sender

        self.size = size
        self.musicPath = musicPath
        #self.SetBackgroundColour((255, 255, 255))
        self.page = 0
        self.subPage = 0
        self.nrOfSubpages = 3


        self.tutorialContent = [
        " Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed ac ex accumsan, commodo tortor a, rhoncus mauris. Mauris gravida vulputate tellus, nec ullamcorper augue pharetra non. Sed ut justo venenatis, ultrices mi gravida, commodo odio. Nulla eu fermentum sem. Proin lobortis dolor ac augue facilisis aliquam. Mauris condimentum metus purus. Duis condimentum sollicitudin diam eget tincidunt. Proin venenatis, lorem et finibus imperdiet, elit ex gravida augue, a rutrum libero odio commodo magna. Proin tempus nec nisi viverra tincidunt. Duis gravida laoreet bibendum. Nulla finibus purus ante. Maecenas sit amet pharetra tellus. Nam vitae velit quam. Duis vel tempus massa. Nam rhoncus sapien quis nulla dictum blandit varius vitae orci.",
        "Quisque congue fermentum dui. Proin et augue elementum, dignissim lectus sagittis, maximus urna. Aenean vel elit porta, mollis sem quis, iaculis erat. Aliquam quis odio at nunc tempus mollis eget nec quam. Donec in metus vulputate, egestas urna eu, interdum erat. Sed suscipit consequat ullamcorper. Sed ac dignissim arcu. Pellentesque placerat maximus turpis. Maecenas non ante tellus. Quisque vitae euismod arcu. Fusce ullamcorper gravida lacus, id porta neque scelerisque nec. Curabitur tortor nibh, maximus a nulla sit amet, ornare ullamcorper justo. Ut lectus dolor, finibus quis sodales eu, porta ut sapien. Aliquam ligula libero, rutrum a sapien et, scelerisque imperdiet mauris.",
        "Cras at tellus mi. Donec id venenatis magna, at consequat eros. Pellentesque ac magna egestas, consectetur nulla in, semper ligula. Aliquam porttitor consequat enim, sit amet semper mauris. Etiam cursus feugiat lacinia. Quisque suscipit feugiat dui ac aliquam. Quisque pellentesque vulputate orci vel semper. Ut congue sodales facilisis. Donec dui arcu, accumsan et accumsan id, cursus vel lectus. Maecenas est erat, sollicitudin ut metus molestie, sollicitudin ornare libero. Donec ac scelerisque tortor. Nam pretium erat ut aliquet laoreet. Cras nec turpis volutpat, suscipit nisi in, interdum massa. In feugiat arcu nibh, ut semper tellus ornare eget. Sed lobortis diam ut sapien facilisis, non volutpat sapien tristique."]

        self.contentField = wx.TextCtrl(parent = self, id=-1, 
            size=(self.size[0]//2-20, self.size[1]//2), 
            style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.contentField.SetValue(self.tutorialContent[self.subPage])

        self.tutorialPageFont = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.NORMAL, False, "resources\\Fonts\\18cents\\18cents.ttf")
        self.contentField.SetFont(self.tutorialPageFont)

        self.maxNrOfHyperlinks = 10
        self.hyperlinkCtrls = []
        self.hyperlinks = []
        
        self.centerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.rightSizer = wx.BoxSizer(wx.VERTICAL)
        self.leftSizer = wx.BoxSizer(wx.VERTICAL)
        self.topBtnSizer =  wx.BoxSizer(wx.HORIZONTAL)
        self.bottomBtnSizer = wx.BoxSizer(wx.HORIZONTAL)

        #all bitmaps for buttons
        leftArrow = wx.Bitmap(relative_textures_path + "new\\arrow_light_small_r.png", wx.BITMAP_TYPE_ANY)
        rightArrow = wx.Bitmap(relative_textures_path + "new\\arrow_light_small.png", wx.BITMAP_TYPE_ANY)
        leftLittleArrow = wx.Bitmap(relative_textures_path + "new\\arrow_green_head_small_r.png", wx.BITMAP_TYPE_ANY)
        rightLittleArrow = wx.Bitmap(relative_textures_path + "new\\arrow_green_head_small.png", wx.BITMAP_TYPE_ANY)
        contentsIcon = wx.Bitmap(relative_textures_path + "small_notepad2.png", wx.BITMAP_TYPE_ANY)
        
        #all needed buttons
        self.leftArrowBtn = wx.Button(self, label="  ", 
            size=(leftArrow.GetWidth()+10, leftArrow.GetHeight()+5), id=0)
        self.rightArrowBtn = wx.Button(self, label="  ", 
            size=(rightArrow.GetWidth()+10, rightArrow.GetHeight()+5), id=0)
        leftLittleArrowBtn = wx.Button(self, label="  ", 
            size=(leftLittleArrow.GetWidth()+10, leftLittleArrow.GetHeight()+5))
        rightLittleArrowBtn = wx.Button(self, label="  ", 
            size=(rightLittleArrow.GetWidth()+10, rightLittleArrow.GetHeight()+5))
        contentsBtn = wx.Button(self, label=" ",
            size=(contentsIcon.GetWidth(), contentsIcon.GetHeight()))
        self.leftArrowBtn.SetBitmap(leftArrow)
        self.rightArrowBtn.SetBitmap(rightArrow)
        leftLittleArrowBtn.SetBitmap(leftLittleArrow)
        rightLittleArrowBtn.SetBitmap(rightLittleArrow)
        contentsBtn.SetBitmap(contentsIcon)
        self.Bind(wx.EVT_BUTTON, self.showMainView, contentsBtn)
        self.Bind(wx.EVT_BUTTON, self.nextSubPage, rightLittleArrowBtn)
        self.Bind(wx.EVT_BUTTON, self.prevSubPage, leftLittleArrowBtn)

        self.rightArrowBtn.SetToolTip(wx.ToolTip("Next topic"))
        self.leftArrowBtn.SetToolTip(wx.ToolTip("Previous topic"))
        rightLittleArrowBtn.SetToolTip(wx.ToolTip("Next subpage"))
        leftLittleArrowBtn.SetToolTip(wx.ToolTip("Previous subpage"))
        contentsBtn.SetToolTip(wx.ToolTip("Tutorial menu"))

        #place for right image
        self.helperImg = wx.Image(relative_textures_path + "Grass.jpg", wx.BITMAP_TYPE_ANY)
        imgWidth = self.size[0] //2
        imgHeight = self.size[1]
        
        self.helperBitmap = wx.StaticBitmap(self, wx.ID_ANY, wx.BitmapFromImage(self.helperImg), 
            size=(imgWidth, imgHeight))

        #place everything where needed
        self.rightSizer.Add(self.helperBitmap)
        self.topBtnSizer.Add(self.leftArrowBtn, 0, wx.CENTER)
        self.topBtnSizer.AddSpacer(10)
        self.topBtnSizer.Add(contentsBtn, 0, wx.CENTER)
        self.topBtnSizer.AddSpacer(10)
        self.topBtnSizer.Add(self.rightArrowBtn, 0, wx.CENTER)

        self.bottomBtnSizer.Add(leftLittleArrowBtn)
        self.bottomBtnSizer.AddSpacer(20)
        self.bottomBtnSizer.Add(rightLittleArrowBtn)

        self.leftSizer.AddSpacer(20)
        self.leftSizer.Add(self.topBtnSizer, 0, wx.CENTER)
        self.leftSizer.AddSpacer(15)
        self.leftSizer.Add(self.contentField, 0, wx.CENTER)
        self.leftSizer.AddSpacer(15)
        self.leftSizer.Add(self.bottomBtnSizer, 0, wx.CENTER)
        self.leftSizer.AddSpacer(15)

        self.hyperlinksBox = wx.BoxSizer(wx.HORIZONTAL)
        self.initHyperlinks()

        self.centerSizer.AddSpacer(10)
        self.centerSizer.Add(self.leftSizer)
        self.centerSizer.AddSpacer(10)
        self.centerSizer.Add(self.rightSizer)
        self.centerSizer.SetDimension(0, 0, self.size[0], self.size[1])

        self.Bind(wx.EVT_SHOW, self.onShow, self)

    def moveToPage(self, event):
        self.parent.showPageView(event)

    def showMainView(self, event):
        self.parent.Show()
        self.parent.centerSizer.ShowItems(True)
        self.Hide()

    def nextSubPage(self, event):
        self.subPage += 1
        if self.subPage >= self.nrOfSubpages:
            self.subPage = 0
        self.changeSubPage()
        

    def prevSubPage(self, event):
        self.subPage -= 1;
        if self.subPage < 0:
            self.subPage = self.nrOfSubpages-1
        self.changeSubPage()

    def changeSubPage(self):
        subPageName = "sub" + str(self.subPage)
        subPageContent = self.tutorialContent[subPageName]
        subPageString = ""
        for x in subPageContent:
            subPageString +=  x
            subPageString += "\n"
        self.contentField.SetValue(subPageString)

    def initHyperlinks(self):
        hyperlinksFont = self.tutorialPageFont
        hyperlinksFont.SetPointSize(18)

        hyperlinksLabel = wx.StaticText(self, label="See also: ")
        hyperlinksLabel.SetFont(hyperlinksFont)
        self.hyperlinksBox.Add(hyperlinksLabel)

        for i in range(self.maxNrOfHyperlinks):  
            hyperlink =wx.HyperlinkCtrl(self, id=i, label="", url="")
            hyperlink.SetFont(hyperlinksFont)
            self.hyperlinkCtrls.append(hyperlink)
            space = wx.StaticText(self, label="\t")

            self.hyperlinksBox.Add(hyperlink)
            self.hyperlinksBox.Add(space)
        self.leftSizer.Add(self.hyperlinksBox)

    def updateHyperlinksAndImg(self):
        for i in range(len(self.hyperlinks)):
            child = self.hyperlinkCtrls[i]
            child.SetLabel(self.hyperlinks[i]['label'])
            child.SetId(self.hyperlinks[i]['id'])
            self.Bind(wx.EVT_HYPERLINK, self.moveToPage, child)
        for i in range (len(self.hyperlinks), self.maxNrOfHyperlinks):
            child = self.hyperlinkCtrls[i]
            child.SetLabel("")
            child.SetId(-100)
        self.helperBitmap.SetBitmap(wx.BitmapFromImage(self.helperImg))
        self.Bind(wx.EVT_BUTTON, self.parent.showPageView, self.leftArrowBtn)
        self.Bind(wx.EVT_BUTTON, self.parent.showPageView, self.rightArrowBtn)
        self.rightArrowBtn.SetId(self.page +1)
        self.leftArrowBtn.SetId(self.page -1)
        self.centerSizer.Layout()

    def onShow(self, event):
        # print "Menu on show"
        global pygame
        if event.GetShow():
            # print "menu: setting up music"
            import pygame
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(
                #os.path.dirname(os.path.abspath(__file__)) + "\\" +
                self.musicPath)
            pygame.mixer.music.play()
        else:
            try:
                # print "Menu, quitting"
                pygame.quit()
            except Exception:
                # print "menu: problem with pygame quit"
                pass

