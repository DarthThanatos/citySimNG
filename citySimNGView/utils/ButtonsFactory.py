from wx import wx, DefaultSize


class ButtonsFactory(object):

    def createButton(self, binder, label, size = None):
        return wx.Button(binder, size = DefaultSize if size == None else size, label = label)

    def bindButton(self, binder, onClickCallback, btn):
        binder.Bind(wx.EVT_BUTTON, onClickCallback, btn)

    def newTip(self, hint):
        tip = wx.ToolTip(hint)
        tip.SetAutoPop(30 * 1000)
        tip.SetReshow(0)
        tip.SetDelay(0)
        return tip

    def newButton(self, binder, label, onClickCallback = None, size = None, hint = None):
        btn = self.createButton(binder, label, size)
        font = wx.Font(14, wx.DECORATIVE, wx.ITALIC, wx.NORMAL)
        btn.SetFont(font)
        if onClickCallback != None: self.bindButton(binder, onClickCallback, btn)
        if hint is not None: btn.SetToolTip(self.newTip(hint))
        return btn
