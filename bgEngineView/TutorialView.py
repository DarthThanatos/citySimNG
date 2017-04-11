import wx
import os


class TutorialView(wx.Panel):
    def __init__(self, parent, size, name, musicPath="TwoMandolins.mp3"):
        wx.Panel.__init__(self, size=size, parent=parent)
        self.Bind(wx.EVT_SHOW, self.onShow, self)
        self.parent = parent
        self.name = name
        self.size = size
        self.musicPath = musicPath
        self.initButtons()
        self.SetBackgroundColour((255, 255, 255))
        self.pageID = 0
        self.tutorial_info = [
            "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus eu sapien non felis mattis\n " \
            "luctus. Nulla sed sapien neque. Mauris vitae urna ac tellus cursus efficitur et egestas turpis.\n" \
            " Etiam vel justo scelerisque, tincidunt dui ac, iaculis felis. In hac habitasse platea dictum\n" \
            "st. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Ut \n" \
            "ante metus, vestibulum nec commodo ac, eleifend porta tortor. Etiam diam orci, luctus ac alique\n" \
            "t at, porttitor nec risus. Fusce fermentum lacinia mauris, eu hendrerit ligula convallis non. \n" \
            "Quisque faucibus tellus ac lacus fringilla malesuada. Nulla id neque eget nisi vulputate accum\n" \
            "san. Quisque euismod metus pretium justo imperdiet iaculis. Cras a ante nisi. Aliquam erat vol\n" \
            "utpat. Nulla rutrum ut velit a placerat. Maecenas laoreet ornare lacinia. Cras ultrices mi nis\n" \
            "i. Etiam euismod et magna ac mattis. Cras et quam dictum, lobortis mauris eget, pretium metus\n" \
            ". Integer pulvinar, sem non suscipit congue, erat ipsum tincidunt mi, et aliquam lectus leo eu\n" \
            " mi. Fusce blandit metus at odio consequat, a suscipit urna pharetra. Sed ullamcorper orci id \n" \
            "lacinia bibendum.",
            "Suspendisse accumsan tincidunt sagittis. Etiam tempor lacus id ante interdum, vitae faucibus \n"
            "nulla aliquet. Donec enim risus, tincidunt eu est nec, suscipit imperdiet nisi. Quisque \n"
            "laoreet magna consectetur porta gravida. Nullam id felis sapien. Suspendisse orci mi, commodo\n"
            " in lorem quis, tincidunt vehicula metus. Morbi laoreet, lectus eu blandit pharetra, tortor\n"
            " ante gravida turpis, quis mollis nisi mi vitae massa. Duis tincidunt nisi a nisi luctus tempus.\n"
            " Vivamus euismod a tortor at tempus.",
            "Aliquam pulvinar ac dui ut iaculis. Nullam ut rutrum odio. Etiam accumsan in dui in auctor. Praesent \n"
            "cursus lacus nec nisl blandit ullamcorper. Proin non est efficitur ligula ultrices pellentesque. Cras \n"
            "aliquet, ante varius commodo fermentum, nisi elit dictum lacus, ac feugiat libero felis eu mi. Nulla \n"
            "porttitor faucibus dui quis gravida. Suspendisse potenti."
            ]

        self.centerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ctrlMsgField = wx.StaticText(self, label=self.tutorial_info[self.pageID])
        self.centerSizer.Add(self.ctrlMsgField, 0, wx.EXPAND, 5)

    def onShow(self, event):
        # print "Menu on show"
        global pygame
        if event.GetShow():
            # print "menu: setting up music"
            import pygame
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(self.musicPath)
            pygame.mixer.music.play()
        else:
            try:
                # print "Menu, quitting"
                pygame.quit()
            except Exception:
                # print "menu: problem with pygame quit"
                pass

    def initButtons(self):
        """ This function creates buttons, sets theirs positions and size and
            binds logic to them."""
        menu_btn = wx.Button(self, label="Menu", pos=(130, 225), size=(60, 30))
        next_btn = wx.Button(self, label="Next", pos=(160, 195), size=(60, 30))
        prev_btn = wx.Button(self, label="Prev", pos=(100, 195), size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)
        self.Bind(wx.EVT_BUTTON, self.nextPage, next_btn)
        self.Bind(wx.EVT_BUTTON, self.prevPage, prev_btn)

    def nextPage(self, event):
        """ This function displays next page of tutorial """
        if self.pageID + 1 < self.tutorial_info.__len__():
            self.pageID += 1
            self.ctrlMsgField.Destroy()
            self.Refresh()
            self.centerSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.ctrlMsgField = wx.StaticText(self, label=self.tutorial_info[self.pageID])
            self.centerSizer.Add(self.ctrlMsgField, 0, wx.EXPAND, 5)

    def prevPage(self, event):
        """ This function displays previous page of tutorial """
        if self.pageID > 0:
            self.pageID -= 1
            self.ctrlMsgField.Destroy()
            self.Refresh()
            self.centerSizer = wx.BoxSizer(wx.HORIZONTAL)
            self.ctrlMsgField = wx.StaticText(self, label=self.tutorial_info[self.pageID])
            self.centerSizer.Add(self.ctrlMsgField, 0, wx.EXPAND, 5)


    def retToMenu(self, event):
        """ This function returns to Menu view """
        self.parent.setView("Menu")

    def initMenuBar(self):
        status = self.CreateStatusBar()
        menuBar = wx.MenuBar()

        first = wx.Menu()
        second = wx.Menu()

        first.Append(wx.NewId(), "New window", "This is a new Window")
        first.Append(wx.NewId(), "Open...", "This will open a new Window")

        menuBar.Append(first, "File")
        menuBar.Append(second, "Edit")

        self.SetMenuBar(menuBar)
