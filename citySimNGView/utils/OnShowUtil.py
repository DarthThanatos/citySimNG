import traceback

from wx import wx


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
        # else:
        #     try:
        #         pygame.quit()
        #     except Exception:
        #         pass

    def onCreatorPanelShow(self, view, event):
        if event.GetShow():
            view.resetContents()
            if not view.wakeUpData == None:
                try:
                    view.logArea.SetValue(view.wakeUpData["Log"])
                except:
                    pass #no need to panic
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

