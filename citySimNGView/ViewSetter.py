import json
import traceback

import wx

from CreatorView.CreatorSwitcher import CreatorSwitcher
from GameMenuView import GameMenuView
from LoaderView import LoaderView
from MainMenuView import MainMenuView
from MapView.MapView import MapView
from RankingView import RankingView
from TutorialView import TutorialView
from utils.RelativePaths import relative_music_path

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, strTitle, tplSize, sender, gateway):
        wx.Frame.__init__(self, parent, ID, strTitle, size=tplSize)
        self.gateway = gateway
        self.sender = sender
        self.tplSize= tplSize
        self.initViews()
        self.currentViewName = None
        self.previousViewName = None

    def initViews(self):
        self.initRawViews()
        self.initViewHolders()

    def initRawViews(self):
        self.initRawViewsDict()
        self.hideAllRawViews()

    def initRawViewsDict(self):
        self.rawViews = {
            # "Loader": LoaderView(self, self.tplSize, "Loader",sender = self.gateway),
            # "GameMenu": GameMenuView(self, self.tplSize, "GameMenu", relative_music_path + "NWN2.mp3", self.gateway),
            # "MainMenu": MainMenuView(self, self.tplSize, "MainMenu", relative_music_path + "NWN2.mp3", self.gateway),
            # "Creator":CreatorSwitcher(self,self.tplSize,"Creator",sender = self.gateway),
            # "Exchange": ExchangeView(self, self.tplSize, "Exchange", self.sender),
            # "Map": MapView(self, self.tplSize, "Map", self.gateway),
            # "Tutorial": TutorialView(self, self.tplSize, "Tutorial", sender = self.sender),
            # "Ranking": RankingView(self, self.tplSize, "Ranking", sender = self.sender)
        }

    def initViewHolders(self):
        self.viewsHolders = {
            "Loader": LoaderHolder(self, self.tplSize, self.sender, self.gateway),
            "GameMenu": GameMenuHolder(self, self.tplSize, self.sender, self.gateway),
            "Creator":CreatorHolder(self, self.tplSize, self.sender, self.gateway),
            "MainMenu": MainMenuHolder(self, self.tplSize, self.sender, self.gateway),
            "Map": MapHolder(self, self.tplSize, self.sender, self.gateway),
            "Tutorial": TutorialHolder(self, self.tplSize, self.sender, self.gateway),
            "Ranking": RankingHolder(self, self.tplSize, self.sender, self.gateway)
        }

    def getView(self, key):
        if key in self.viewsHolders:
            return self.viewsHolders[key].getView()
        else: return self.rawViews[key]

    def hideAllRawViews(self):
        for name in self.rawViews:
            self.rawViews[name].Hide()

    def passMsgToCurrentView(self, msg):
        try:
            jsonObj = json.loads(msg)
            receipent = jsonObj["To"]
            args = jsonObj["Args"]
            if receipent == "ViewSetter":
                target_view = args["TargetView"]
                self.setView(target_view)
            else:
                self.getView(receipent).readMsg(msg)
        except:
            traceback.print_exc()
            return

    def setView(self, viewName):
        self.previousViewName = self.currentViewName
        self.currentViewName = viewName
        self.setViewsHolders(viewName)
        self.setRawViews(viewName)

    def setRawViews(self, viewName):
        for name in self.rawViews:
            wx.CallAfter(self.rawViews[name].Show, name == viewName)
            if name == self.currentViewName:
                self.hidePreviousView()
                self.ShowFullScreen(True)
                self.Show()

    def setViewsHolders(self, viewName):
        for name in self.viewsHolders:
            wx.CallAfter(
                self.viewsHolders[name].animateFrameTransition, name == viewName, viewName
            )

    def hidePreviousView(self):
        if self.previousViewName is None or  self.currentViewName == self.previousViewName: return
        self.getView(self.previousViewName).Hide()
        previousView = self.getView(self.previousViewName).GetParent()
        previousView.Enable()
        previousView.Hide()
        if self.previousViewName in self.viewsHolders:
            previousView.alpha = 0
            previousView.SetTransparent(0)

    def closeWindow(self, event):
        self.Destroy()

    def closeWindowSystem(self, arg):
        for view in self.viewsHolders.values():
            view.Close(True)
            view.Destroy()
        self.Close(True)
        self.Destroy()

class ViewHolder(wx.Frame):

    def __init__(self, parent, tplSize, sender, gateway):
        wx.Frame.__init__(self, None, size=tplSize)
        self.parent = parent
        self.sender = sender
        self.gateway= gateway
        self.alpha = 0
        self.SetTransparent(0)
        self.timer = wx.Timer(self, wx.ID_ANY)

    def passOnShowEvent(self, ev):
        self.getView().Show(ev.GetShow())

    def getView(self):
        raise Exception("getView not implemented")

    def animateFrameTransition(self, shouldShow, nextViewName):
        if not shouldShow: return
        self.Bind(wx.EVT_TIMER, self.onAnimateShowing)
        if self.parent.previousViewName is not None:
            self.parent.getView(self.parent.previousViewName).GetParent().Disable()
        self.Disable()
        self.onPreAnimateShowing()
        self.timer.Start(15, oneShot=False)

    def onPreAnimateShowing(self):
        self.Show()
        self.getView().Show(True)
        self.ShowFullScreen(True)

    def onAnimateShowing(self, event):
        self.SetFocus()
        if self.alpha >= 255:
            self.onPostAnimateShowing()
            return
        self.SetTransparent(self.alpha)
        self.alpha += 5

    def onPostAnimateShowing(self):
        self.alpha = 255
        self.timer.Stop()
        self.Enable()
        self.parent.hidePreviousView()

class LoaderHolder(ViewHolder):

    def __init__(self, parent, tplSize, sender, gateway):
        super(LoaderHolder, self).__init__(parent, tplSize, sender, gateway)
        self.loaderView = LoaderView(self, tplSize, "Loader", sender = self.gateway)
        self.loaderView.Hide()

    def getView(self):
        return self.loaderView

class GameMenuHolder(ViewHolder):

    def __init__(self, parent, tplSize, sender, gateway):
        super(GameMenuHolder, self).__init__(parent, tplSize, sender, gateway)
        self.gameMenuView = GameMenuView(self, tplSize, "GameMenu", relative_music_path + "NWN2.mp3", self.gateway)
        self.gameMenuView.Hide()

    def getView(self):
        return self.gameMenuView

class MainMenuHolder(ViewHolder):

    def __init__(self, parent, tplSize, sender, gateway):
        super(MainMenuHolder, self).__init__(parent, tplSize, sender, gateway)
        self.mainMenuView = MainMenuView(self, tplSize, "MainMenu", relative_music_path + "NWN2.mp3", self.gateway)
        self.mainMenuView.Hide()

    def getView(self):
        return self.mainMenuView

    def closeWindow(self, arg):
        self.Bind(wx.EVT_TIMER, self.onAnimateHiding)
        self.Disable()
        self.timer.Start(25, oneShot=False)

    def onAnimateHiding(self, event):
        self.SetFocus()
        if self.alpha <= 0:
            self.onPostAnimateHiding()
            return
        self.SetTransparent(self.alpha)
        self.alpha -= 5


    def onPostAnimateHiding(self):
        self.timer.Stop()
        self.parent.closeWindowSystem(None)

class CreatorHolder(ViewHolder):
    def __init__(self, parent, tplSize, sender, gateway):
        super(CreatorHolder, self).__init__(parent, tplSize, sender, gateway)
        self.creatorSwitcher =  CreatorSwitcher(self, tplSize,"Creator",sender = self.gateway)
        self.creatorSwitcher.Hide()

    def getView(self):
        return self.creatorSwitcher

class MapHolder(ViewHolder):

    def __init__(self, parent, tplSize, sender, gateway):
        super(MapHolder, self).__init__(parent, tplSize, sender, gateway)
        self.mapView = MapView(self, tplSize, "Map", self.gateway)
        self.mapView.Hide()

    def getView(self):
        return self.mapView

class TutorialHolder(ViewHolder):

    def __init__(self, parent, tplSize, sender, gateway):
        super(TutorialHolder, self).__init__(parent, tplSize, sender, gateway)
        self.tutorialView = TutorialView(self, tplSize, "Tutorial", sender = self.sender)
        self.tutorialView.Hide()

    def getView(self):
        return self.tutorialView

class RankingHolder(ViewHolder):

    def __init__(self, parent, tplSize, sender, gateway):
        super(RankingHolder, self).__init__(parent, tplSize, sender, gateway)
        self.rankingView = RankingView(self, tplSize, "Ranking", sender = self.sender)
        self.rankingView.Hide()

    def getView(self):
        return self.rankingView
