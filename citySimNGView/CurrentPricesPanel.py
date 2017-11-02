import wx

from utils.ImageUtils import ImageUtils
from utils.RelativePaths import relative_system_imgs_path

ANIMATION_PERIOD = 75

class CurrentPricesPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent,  size = (wx.GetDisplaySize()[0],50))
        self.rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.SetSizer(self.rootSizer)
        self.rootSizer.SetDimension(0,0,wx.GetDisplaySize()[0],50)
        self.actualPanelWitdh = 0
        self.currentPanelPos = 0
        self.timer = wx.Timer(self, wx.ID_ANY)

    def animateCurrentPrices(self, currentPricesDict):
        print "current prices panel: animating prices:", currentPricesDict
        self.Bind(wx.EVT_TIMER, self.onAnimate)
        self.onPreAnimate(currentPricesDict)
        self.timer.Start(ANIMATION_PERIOD, oneShot=False)

    def onPreAnimate(self, currentPricesDict):
        self.reset()
        self.Show(False)
        for resource in currentPricesDict.keys():
            price = currentPricesDict[resource]
            self.rootSizer.Add(self.newPriceIndicatorHorizontalSizer(resource, price), 0, wx.CENTER)
        self.currentPanelPos = wx.GetDisplaySize()[0]
        self.rootSizer.SetDimension(self.currentPanelPos, 0, self.actualPanelWitdh, 50)
        self.rootSizer.Layout()
        self.Show(True)

    def onAnimate(self, event):
        if self.currentPanelPos < -self.actualPanelWitdh - 20:
            self.onPostAnimate()
            return
        self.rootSizer.SetDimension(self.currentPanelPos, 0, self.actualPanelWitdh, 50)
        self.currentPanelPos -= 5
            # ANIMATION_TIME = 10000
            # ANIMATION_STEP = float(ANIMATION_PERIOD)/ANIMATION_TIME
            # int(ANIMATION_STEP * (wx.GetDisplaySize()[0] + self.actualPanelWitdh))

    def onPostAnimate(self):
        self.timer.Stop()

    def newPriceIndicator(self, resource, price):
        priceIndicator  = wx.StaticText(self, -1, resource + ": " + str(price))
        priceIndicator.SetForegroundColour((255,0,0) if price < 0 else (0,255,0))
        font = wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        priceIndicator.SetFont(font)
        return priceIndicator

    def newPriceIndicatorHorizontalSizer(self, resource, price):
        priceIndicatorHorizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        print "creating indicator for:",resource,price
        priceIndicatorHorizontalSizer.Add(
            ImageUtils(self).newScaledImgBmpInDir(relative_system_imgs_path, "green_bolthead.png" if price >= 0 else "red_bolthead.png")
        )
        priceIndicatorHorizontalSizer.AddSpacer(10)
        priceIndicatorHorizontalSizer.Add(self.newPriceIndicator(resource, price))
        priceIndicatorHorizontalSizer.AddSpacer(20)
        self.actualPanelWitdh += sum(map(lambda x: x.GetSize()[0], priceIndicatorHorizontalSizer.GetChildren()))
        return priceIndicatorHorizontalSizer

    def reset(self):
        self.rootSizer.Clear(True)
        self.actualPanelWitdh = 0