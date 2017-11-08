import wx
import time


class LeftPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        self.text = parent.GetParent().rightPanel.text
        self.text_2 = parent.GetParent().rightPanel.text_2
        button1 = wx.Button(self, -1, 'Count', (10, 10))
        button2 = wx.Button(self, -1, 'Countdown', (10, 60))
        button3 = wx.Button(self, -1, 'Action', (10, 110))
        self.Bind(wx.EVT_BUTTON, self.OnPlus, id=button1.GetId())
        self.Bind(wx.EVT_BUTTON, self.OnMinus, id=button2.GetId())
        self.Bind(wx.EVT_BUTTON, self.button_Pressed, id=button3.GetId())
        self.timed_Out = 1

    def OnPlus(self, event):
        value = 1
        for t in range(5000):
            value = value + 1
            if value == 3: raise Exception("yolo")
            time.sleep(1)
            self.text.SetLabel(str(value))

    def OnMinus(self, event):
        import math
        value = 60
        for t in range(value):
            value = value - 1
            time.sleep(1)
            self.text.SetLabel(str(value / 60) + ':' + str(value % 60))

        self.timed_Out = 0
        self.text_2.SetLabel(str('End o\'line.'))

    def button_Pressed(self, event):
        if self.timed_Out == 1:
            if self.text_2 == 'First':
                self.text_2.SetLabel('Second')

            elif self.text_2 == 'Second':
                self.text_2.SetLabel('First')


class RightPanel(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id, style=wx.BORDER_SUNKEN)
        self.text = wx.StaticText(self, -1, '0', (10, 60))
        self.text_2 = wx.StaticText(self, -1, 'First', (10, 120))


class Communicate(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(600, 200))
        panel = wx.Panel(self, -1)
        self.rightPanel = RightPanel(panel, -1)
        leftPanel = LeftPanel(panel, -1)
        hbox = wx.BoxSizer()
        hbox.Add(leftPanel, 1, wx.EXPAND | wx.ALL, 4)
        hbox.Add(self.rightPanel, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(hbox)
        self.Centre()
        self.Show(True)


app = wx.App()
Communicate(None, -1, 'widgets communicate')
app.MainLoop()