import wx

class MenuView(wx.Panel):
    def __init__(self, parent, size, name):
        wx.Panel.__init__(self, size = size, parent=parent)
        self.parent = parent
        self.name = name
        self.size = size
        self.initButtons()


    def initButtons(self):
        buttonsSizer = wx.BoxSizer(wx.VERTICAL)
        newgame_btn = wx.Button(self, label = "New Game")
        creator_btn = wx.Button(self,label="Creator")
        tutorial_btn = wx.Button(self,label="Tutorial")
        exchange_btn = wx.Button(self,label="Exchange")
        load_btn = wx.Button(self,label="Load")
        save_btn = wx.Button(self,label="Save")
        exit_btn = wx.Button(self, label="Exit")
        buttonsSizer.AddSpacer(self.size[1]/3)
        buttonsSizer.Add(newgame_btn, 0, wx.CENTER | wx.ALL, 5)
        buttonsSizer.Add(creator_btn, 0, wx.CENTER | wx.ALL)
        buttonsSizer.Add(tutorial_btn, 0, wx.CENTER)
        buttonsSizer.Add(exchange_btn, 0, wx.CENTER)
        buttonsSizer.Add(load_btn, 0, wx.CENTER)
        buttonsSizer.Add(save_btn, 0, wx.CENTER)
        buttonsSizer.Add(exit_btn, 0, wx.CENTER | wx.ALL, 5)
        self.Bind(wx.EVT_BUTTON, self.closeButton, exit_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToCreator, creator_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToExchange, exchange_btn)
        self.Bind(wx.EVT_BUTTON, self.moveToNewGame, newgame_btn)
        self.SetSizer(buttonsSizer)
        buttonsSizer.SetDimension(0,0,self.size[0], self.size[1])

    def closeButton(self, event):
        self.Close(True)
        self.parent.closeWindow(None)

    def moveToNewGame(self, event):
        self.parent.setView("Map")

    def moveToCreator(self, event):
        self.parent.setView("Creator")

    def moveToExchange(self,event):
        self.parent.setView("Exchange")



