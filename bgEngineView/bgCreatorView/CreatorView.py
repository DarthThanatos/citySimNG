import wx
import wx.grid as gridlib

class CreatorView(wx.Panel):
    def __init__(self, parent, size, name):
        wx.Panel.__init__(self,  size = size,  parent=parent)
        self.name = name
        self.parent = parent

        rootSizer = wx.BoxSizer(wx.VERTICAL)
        buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
        centerSizer = wx.BoxSizer(wx.HORIZONTAL)

        grid = gridlib.Grid(self)
        grid.CreateGrid(25,12)
        centerSizer.Add(grid, 0, wx.ALL | wx.EXPAND, 5)
        
        ctrlMsgField = wx.StaticText(self, label = "This is the place for control messages")
        centerSizer.Add(ctrlMsgField, 0 , wx.EXPAND, 5)

        menu_btn = wx.Button(self,  label="Menu")
        self.Bind(wx.EVT_BUTTON, self.retToMenu, menu_btn)
        buttonsSizer.Add(menu_btn, 0 , wx.ALL | wx.EXPAND, 5)

        create_btn = wx.Button(self, label = "Create")
        self.Bind(wx.EVT_BUTTON, self.createDependencies, create_btn)
        buttonsSizer.Add(create_btn, 0, wx.EXPAND, 5)
        
        rootSizer.Add(centerSizer, 0, wx.EXPAND, 5)
        rootSizer.Add(buttonsSizer,0, wx.CENTER)
        self.SetSizer(rootSizer)
        #rootSizer.Fit(self)
        rootSizer.SetDimension(0,0,size[0],size[1])

    def retToMenu(self, event):
        self.parent.setView("Menu")

    def createDependencies(self, event):
        print "Dependencies created"
