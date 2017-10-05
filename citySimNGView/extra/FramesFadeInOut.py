import wx


class Fader(wx.Frame):
    def __init__(self, parent, startTransparency, delta, color, switchFunc):
        wx.Frame.__init__(self, parent = parent, size=screenDims)
        self.alpha = startTransparency
        self.delta = delta
        self.cycles = 0
        self.color = color
        rootSizer = wx.BoxSizer(wx.HORIZONTAL)
        verticalSizer = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self, wx.ID_ANY)
        panel.SetBackgroundColour(color)
        self.btn = wx.Button(panel, label = "switch")
        self.btn.Bind(wx.EVT_BUTTON, switchFunc)
        self.timer = wx.Timer(self, wx.ID_ANY)
        self.SetTransparent(self.alpha)
        exit_btn = wx.Button(panel, label="exit")
        exit_btn.Bind(wx.EVT_BUTTON, parent.onClose)
        verticalSizer.Add(self.btn, 0, wx.CENTER)
        verticalSizer.Add(exit_btn, 0, wx.CENTER)
        self.ShowFullScreen(True)
        rootSizer.AddStretchSpacer()
        rootSizer.Add(verticalSizer, 0, wx.CENTER)
        rootSizer.AddStretchSpacer()
        rootSizer.SetDimension(0, 0, screenDims[0], screenDims[1])
        self.SetSizer(rootSizer)

    def getName(self):
        return "black frame" if self.color == (0,0,0) else "red frame"

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='Test', size = screenDims)
        self.redFader = self.newFrame(0, 5, (255,0,0))
        self.blackFader = self.newFrame(255, -5, (0,0,0))
        self.redFader.Hide()
        self.blackFader.Show()

    def newFrame(self, startTransparency, delta, color):
        frame = Fader(self, startTransparency, delta, color, self.animateFrames)
        return frame

    def onClose(self, event):
        self.blackFader.Destroy()
        self.redFader.Destroy()
        self.Destroy()

    def animateFrames(self, event):
        print "animate black frame, shown:", self.blackFader.IsShown()
        self.animateFrameTransition(self.blackFader)
        print "animate red frame, shown:", self.redFader.IsShown()
        self.animateFrameTransition(self.redFader)

    def animateFrameTransition(self, frame):
        frame.Bind(wx.EVT_TIMER, self.animateShowing if not frame.IsShown() else self.animateHiding)
        frame.btn.Enable(False)
        frame.Show()
        frame.timer.Start(50, oneShot=False)

    def animateShowing(self, event):
        animatedFrame = event.GetEventObject()
        if animatedFrame.alpha >= 255:
            animatedFrame.alpha = 255
            animatedFrame.timer.Stop()
            animatedFrame.btn.Enable(True)
            return
        print "animate " + animatedFrame.getName() + " showing, alpha:",animatedFrame.alpha,"can animate: ", animatedFrame.CanSetTransparent()
        animatedFrame.SetTransparent(animatedFrame.alpha)
        animatedFrame.alpha += 5

    def animateHiding(self, event):
        animatedFrame = event.GetEventObject()
        if animatedFrame.alpha <= 0:
            animatedFrame.alpha = 0
            animatedFrame.timer.Stop()
            animatedFrame.Hide()
            animatedFrame.btn.Enable(True)
            return
        print "animate " + animatedFrame.getName() + " hiding, alpha:",animatedFrame.alpha,"can animate: ", animatedFrame.CanSetTransparent()
        animatedFrame.SetTransparent(animatedFrame.alpha)
        animatedFrame.alpha -= 5

if __name__ == '__main__':
    app = wx.App(False)
    screenDims = wx.GetDisplaySize()
    frm = MainFrame()
    app.MainLoop()