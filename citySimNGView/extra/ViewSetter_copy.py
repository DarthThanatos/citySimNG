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
from extra.ExchangeView import ExchangeView
from utils.RelativePaths import relative_music_path


class MyFrame(wx.Frame):
    def __init__(self, parent, ID, strTitle, tplSize, sender, gateway):
        wx.Frame.__init__(self, parent, ID, strTitle, size=tplSize)
        self.gateway = gateway
        self.sender = sender
        self.tplSize= tplSize
        self.initViews()
        self.hideAllViews()
        self.ShowFullScreen(True)

    def initViews(self):
        self.views = {
            "Loader": LoaderView(self, self.tplSize, "Loader",sender = self.gateway),
            "GameMenu": GameMenuView(self, self.tplSize, "GameMenu", relative_music_path + "NWN2.mp3", self.gateway),
            "MainMenu": MainMenuView(self, self.tplSize, "MainMenu", relative_music_path + "NWN2.mp3", self.gateway),
            "Creator":CreatorSwitcher(self,self.tplSize,"Creator",sender = self.gateway),
            "Exchange": ExchangeView(self, self.tplSize, "Exchange", self.sender),
            "Map": MapView(self, self.tplSize, "Map", sender = self.gateway),
            "Tutorial": TutorialView(self, self.tplSize, "Tutorial", sender = self.sender),
            "Ranking": RankingView(self, self.tplSize, "Ranking", sender = self.sender)
        }

    def hideAllViews(self):
        for name in self.views:
            self.views[name].Hide()

    def passMsgToCurrentView(self, msg):
        try:
            jsonObj = json.loads(msg)
            receipent = jsonObj["To"]
            args = jsonObj["Args"]
            if receipent == "ViewSetter":
                target_view = args["TargetView"]
                self.setView(target_view)
            else:
                self.views[receipent].readMsg(msg)
        except:
            traceback.print_exc()
            return

    def setView(self, viewName):
        objToRun = None
        for name in self.views:
            if name == viewName:    
                objToRun = self.views[name]
            else:
                self.views[name].Hide()
        objToRun.Show()

    def closeWindow(self, event):
        self.Destroy()