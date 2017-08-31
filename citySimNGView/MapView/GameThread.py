import threading

import pygame

from Consts import FPS


class GameThread(threading.Thread):
    """ This class represents an instance of game thread."""
    def __init__(self, game):
        """ Constructor.

        :param game: game instance
        """
        threading.Thread.__init__(self)
        self.game = game

    def run(self):
        """ Run function. """
        clock = pygame.time.Clock()
        while self.game.game_on:
            self.game.process_events()
            self.game.update()
            self.game.display_frame()

            pygame.display.flip()
            clock.tick(FPS)
