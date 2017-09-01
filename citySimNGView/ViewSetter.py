import os
import wx
from py4j.java_gateway import JavaGateway, GatewayParameters

from CreatorView.CreatorView import CreatorView
from CreatorView.CreatorSwitcher import CreatorSwitcher
from GameMenuView import GameMenuView
from LoaderView import LoaderView
from MainMenuView import MainMenuView
from ExchangeView import ExchangeView
from MapView.MapView import MapView
from TutorialView import TutorialView
from RankingView import RankingView
import pygame
import json
import traceback
from RelativePaths import relative_music_path

class MyFrame(wx.Frame):
    def __init__(self, parent, ID, strTitle, tplSize, sender, gateway):
        wx.Frame.__init__(self, parent, ID, strTitle, size=tplSize)
        self.views = {
            "Loader": LoaderView(self, tplSize, "Loader",sender = sender),
            "GameMenu": GameMenuView(self, tplSize, "GameMenu", relative_music_path + "NWN2.mp3", sender),
            "MainMenu": MainMenuView(self, tplSize, "MainMenu", relative_music_path + "NWN2.mp3", gateway),
            #"Creator": CreatorView(self, tplSize, "Creator", relative_music_path + "Ret Xed OST.mp3", sender),
            "Creator":CreatorSwitcher(self,tplSize,"Creator",sender = gateway),
            "Exchange": ExchangeView(self, tplSize, "Exchange", sender),
            "Map": MapView(self, tplSize, "Map", sender),
            "Tutorial": TutorialView(self, tplSize, "Tutorial", sender = sender),
            "Ranking": RankingView(self, tplSize, "Ranking", sender = sender)
        }

        for name in self.views:
            self.views[name].Hide()
        # ^ hiding every view, so they will react on Show() later
        # (otherwise the first view to run will be inactive, i.e. no
        # EVT_SHOW event shall be triggered for the first view to  be seen)
        
        self.ShowFullScreen(True)
        # self.currentViewName = "MainMenu"
        # self.setView("MainMenu")

    def passMsgToCurrentViewWithOldFormat(self, msg):
        msgParts = msg.split("@")
        # ^ here we use split() methid having "@" separator, because arguments in the message may be texts containing spaces
        if msg.startswith("SetView"):
            self.setView(msgParts[1])
            # ^ controller told us explicitely to change the current view
        else:
            # msg is in the form: ViewName@Params
            self.views[msgParts[0]].readMsg("@".join(msgParts[1:]))

    def passMsgToCurrentView(self, msg):
        try:
            jsonObj = json.loads(msg)
            operation = jsonObj["Operation"]
            receipent = jsonObj["To"]
            args = jsonObj["Args"]
            if receipent == "ViewSetter":
                target_view = args["TargetView"]
                self.setView(target_view)
                # ^ controller told us explicitely to change the current view
            else:
                self.views[receipent].readMsg(msg)
        except:
            print "Not a valid json msg:", json.dumps(json.loads(msg),indent=4), "skipping..."
            traceback.print_exc()
            return

    def setView(self, viewName):
        print "setting view " + viewName
        objToRun = None
        for name in self.views:
            if name == viewName:    
                objToRun = self.views[name]
            else:
                self.views[name].Hide()
        objToRun.Show()

    def closeWindow(self, event):
        self.Destroy()



