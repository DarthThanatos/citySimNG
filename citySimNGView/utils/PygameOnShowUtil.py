class PygameOnShowUtil(object):

    def __init__(self, musicPath=None):
        self.musicPath = musicPath

    def switch_music_on_show_changed(self, event, onShowCallback = None):
        global pygame
        if event.GetShow():
            if onShowCallback != None: onShowCallback()
            try:
                import pygame
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load(
                    self.musicPath)
                pygame.mixer.music.play()
            except Exception:
                print "Problem with music"
        else:
            try:
                pygame.quit()
            except Exception:
                pass
