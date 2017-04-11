import wx
import os


class TutorialViewCenterPart(wx.Panel):
    def __init__(self, parent, ID, tplSize, musicPath="TwoMandolins.mp3"):
        self.parent = parent
        self.ID = ID
        self.tplSize = tplSize
        self.musicPath = musicPath
        wx.Panel.__init__(self, self.parent, self.ID, size=self.tplSize)
        self.SetBackgroundColour((255, 255, 0))
        tutorial_info = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vivamus eu sapien non felis mattis\n " \
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
                        "lacinia bibendum."

        self.centerSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.ctrlMsgField = wx.StaticText(self, label=tutorial_info)
        self.centerSizer.Add(self.ctrlMsgField, 0, wx.EXPAND, 5)

    def onShow(self, event):
        if event.GetShow():
            print "shown tutorial"
            self.initView()
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(self.musicPath)
                pygame.mixer.music.play()
            except Exception:
                print "Problem with music"
        else:
            try:
                print "tutorial: quitting"
                pygame.quit()
            except Exception:
                print "first appearance of Tutorial: pygame not initialized in tutorial"

    def initView(self):
        print "Tutorial: initview"
        global pygame
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame   # this has to happen after setting the environment variables.
        pygame.init()
        pygame.display.init()
        window = pygame.display.set_mode(self.tplSize)
        pygame.display.flip()
        pygame.display.update()


class TutorialView(wx.Panel):
    def __init__(self, parent, size, name):
        wx.Panel.__init__(self, parent=parent, size=size)
        self.SetBackgroundColour((255, 255, 255))
        self.name = name
        self.parent = parent
        self.center = TutorialViewCenterPart(self, -1, (508, 195))

        self.initButtons()
        self.Bind(wx.EVT_SHOW, self.center.onShow, self)
        #self.initMenuBar()

    def initButtons(self):
        """ This function creates buttons, sets theirs positions and size and
            binds logic to them."""
        menu_btn = wx.Button(self, label="Menu", pos=(130, 225), size=(60, 30))
        next_btn = wx.Button(self, label="Next", pos=(100, 195), size=(60, 30))
        prev_btn = wx.Button(self, label="Prev", pos=(160, 195), size=(60, 30))
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)
        self.Bind(wx.EVT_BUTTON, self.nextPage, next_btn)
        self.Bind(wx.EVT_BUTTON, self.prevPage, prev_btn)

    def nextPage(self, event):
        """ This function displays next page of tutorial """
        pass

    def prevPage(self, event):
        """ This function displays previous page of tutorial """
        pass

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
