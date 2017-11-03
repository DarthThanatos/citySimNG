import traceback

from wx import wx

from CreatorView import Consts


class OnShowUtil(object):

    def switch_music_on_show_changed(self, event, musicPath, onShowCallback = None):
        global pygame
        if event.GetShow():
            if onShowCallback != None: onShowCallback()
            try:
                import pygame
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(
                    musicPath)
                pygame.mixer.music.play()
            except Exception:
                print "Problem with music"

    def onCreatorPanelShow(self, view, event):
        if event.GetShow():
            if view.wakeUpData is not None:
                log_content = view.wakeUpData["Log"] if "Log" in view.wakeUpData else None
                cleanGraph = view.wakeUpData["CleanGraph"] if "CleanGraph" in view.wakeUpData else True
                view.resetContents(log_content, cleanGraph)
            else:
                view.resetContents()
            view.wakeUpData = None


    def onCreatorSheetShow(self, sheetView, event):
        if event.GetShow():
            if not sheetView.wakeUpData == None:
                try:
                    sheetView.setUpEditMode(edit_element_name = sheetView.wakeUpData["Edit"])
                except:
                    traceback.print_exc()
                sheetView.wakeUpData = None
            else:
                sheetView.setUpAddMode()

