import wx

from utils import LogMessages


class TipButton(wx.Button):
    """Subclass of wx.Button, has the same functionality.
    Allows user to set Status Bar help by using SetStatusText method.
    """
    current = None

    def __init__(self, *args, **kwargs):
        wx.Button.__init__(self, *args, **kwargs)

    def SetStatusText(self, help_string, status_bar_frame):
        self.help_string = help_string
        self.status_bar_frame = status_bar_frame
        self.Bind(wx.EVT_ENTER_WINDOW, self._ShowHelp)
        self.Bind(wx.EVT_LEAVE_WINDOW, self._HideHelp)

    def _ShowHelp(self, e):
        TipButton.current = self.GetLabel()
        self.status_bar_frame.SetStatusText(self.help_string)

    def _HideHelp(self, e):
        if self.GetLabel() == TipButton.current:
            self.status_bar_frame.SetStatusText("")

class MainWindow(wx.Frame):
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)

        self.CreateStatusBar()

        self.panel = wx.Panel(self)
      # Instead of
      # self.button1 = wx.Button(self.panel, label="Test1", size=(150, 50))
        self.button1 = TipButton(self.panel, label="Test1", size=(150, 50))
        self.button1.SetStatusText("This is for testing purposes", self)
        self.button1.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, u'Consolas'))

      # Instead of
      # self.button2 = wx.Button(self.panel, label="Test2", size=(150, 50))
        self.button2 = TipButton(self.panel, label="Test2", size=(150, 50))
        self.button2.SetStatusText(LogMessages.CREATOR_BTN_HINT, self)
        self.button2.SetFont(wx.Font(14, wx.DEFAULT, wx.NORMAL, wx.NORMAL, 0, u'Consolas'))

        self.sizer = wx.BoxSizer()
        self.sizer.Add(self.button1)
        self.sizer.Add(self.button2)

        self.panel.SetSizerAndFit(self.sizer)
        self.Show()

app = wx.App(False)
win = MainWindow(None)
app.MainLoop()