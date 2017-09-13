from wx import wx, DefaultSize


class ButtonsFactory(object):

    def createButton(self, binder, label, size = None):
        return wx.Button(binder, size = DefaultSize if size == None else size, label = label)

    def bindButton(self, binder, onClickCallback, btn):
        binder.Bind(wx.EVT_BUTTON, onClickCallback, btn)

    def newButton(self, binder, label, onClickCallback = None, size = None):
        btn = self.createButton(binder, label, size)
        if onClickCallback != None: self.bindButton(binder, onClickCallback, btn)
        return btn