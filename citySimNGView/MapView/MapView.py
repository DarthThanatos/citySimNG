import json
import os
import threading
import traceback
import pygame

import wx
from CreatorView.RelativePaths import relative_music_path, relative_textures_path

from Consts import RESOURCES_PANEL_SIZE, PURPLE, FONT, TEXT_PANEL_HEIGHT, \
    TEXT_PANEL_WIDTH, MENU_BUTTON_WIDTH, NAVIGATION_PANEL_WIDTH, INFO_PANEL_WIDTH, TEXT_PANEL_FONT_SIZE
from Game import Game
from GameThread import GameThread
from Utils import draw_text
from Converter import Converter


class MapView(wx.Panel):
    """ This class represents an instance of map view. It is responsible for communication with model. """
    map_view_initialized = False
    can_afford_on_building = False
    last_res_info = None
    condition = threading.Condition()

    def __init__(self, parent, size, name, sender, music_path=relative_music_path + "TwoMandolins.mp3"):
        """ Constructor.

        :param parent:
        :param size: game screen size
        :param name:
        :param sender:
        :param music_path: path to music
        """
        # call base class constructor
        wx.Panel.__init__(self, parent=parent, size=size)

        # set class fields
        self.parent = parent
        self.width = size[0]
        self.height = size[1]
        self.screen_height = size[1]
        self.name = name
        self.sender = sender
        self.music_path = music_path

        # bind EVT_SHOW to onShow() function
        self.Bind(wx.EVT_SHOW, self.on_show, self)

        # add buttons
        self.init_buttons()

        style = wx.TE_MULTILINE | wx.TE_READONLY
        self.log = wx.TextCtrl(self, wx.ID_ANY, size=(size[0] * TEXT_PANEL_WIDTH, TEXT_PANEL_HEIGHT * size[1]),
                               style=style, pos=(self.width * NAVIGATION_PANEL_WIDTH + self.width * INFO_PANEL_WIDTH,
                                                 int(size[1] - TEXT_PANEL_HEIGHT * size[1])))
        font = wx.Font(TEXT_PANEL_FONT_SIZE, wx.MODERN, wx.NORMAL, wx.NORMAL, False, FONT)
        self.log.SetFont(font)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(self.sizer)

    def init_buttons(self):
        """ Function initializing buttons. """
        menu_btn = wx.Button(self, label="Menu", pos=(self.width - MENU_BUTTON_WIDTH * self.width,
                                                      self.screen_height - self.screen_height * TEXT_PANEL_HEIGHT),
                             size=(MENU_BUTTON_WIDTH * self.width, self.screen_height * TEXT_PANEL_HEIGHT))
        self.Bind(wx.EVT_BUTTON, self.ret_to_menu, menu_btn)

    def on_show(self, event):
        """ Function receiving events sent to map view. """
        if event.GetShow():
            print "shown map"
            self.init_view()
            try:
                pygame.mixer.init()
                pygame.mixer.music.load(self.music_path)
                # TODO: uncomment to play music
                pygame.mixer.music.play()
            except Exception:
                print "Problem with music"
        # else:
        #     try:
        #         pygame.quit()
        #     except Exception:
        #         print "first appearance of MapView: pygame not initialized in map"

    def init_view(self):
        """ Function initializing map view. """
        print "Map: initview", str(self.GetHandle())
        self.hackPygame()
        pygame.init()
        pygame.display.init()
        self.sender.entry_point.getMapPresenter().viewInitialized()

    def hackPygame(self):
        print "hacking pygame :)"
        global pygame
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame  # this has to happen after setting the environment variables.
        pygame.init()
        pygame.quit()
# =================================================================================================================== #
# Communication with model
# =================================================================================================================== #

# =================================================================================================================== #
# Functions sending messages to model
# =================================================================================================================== #

    def ret_to_menu(self, event):
        """ Send node change message to model. """
        self.game.game_on = False
        self.game.listener_thread.join()
        self.map_view_initialized = False
        self.sender.entry_point.getMapPresenter().goToMenu()

    def erected_building(self, building):
        """ Send message to model that new building has been erected. """
        result = self.sender.entry_point.getMapPresenter().placeBuilding(building.name, building.id)
        self.game.resources_panel.resources_values = \
            Converter().convertJavaMapToDict(result.getActualResourcesValues())
        self.game.resources_panel.resources_incomes = \
            Converter().convertJavaMapToDict(result.getActualResourcesIncomes())
        self.game.resources_panel.curr_dwellers_amount = result.getCurrentDwellersAmount()
        self.game.resources_panel.curr_max_dwellers_amount = result.getCurrentDwellersMaxAmount()

    def check_if_can_afford(self, building):
        """ Send message to model with the inquiry if player has enough resources to erect building and
        wait for response.

        :param building: building that player wants to erect
        :return: response from model telling if player can afford to erect building
        """
        return self.sender.entry_point.getMapPresenter().checkIfCanAffordOnBuilding(building.name)

    def deleted_building(self, building_id):
        """ Send message to model that building has been deleted.

        :param building_id: id of building that will be deleted
        """
        result = self.sender.entry_point.getMapPresenter().deleteBuilding(building_id)
        self.game.resources_panel.resources_values = \
            Converter().convertJavaMapToDict(result.getActualResourcesValues())
        self.game.resources_panel.resources_incomes = \
            Converter().convertJavaMapToDict(result.getActualResourcesIncomes())
        self.game.resources_panel.curr_dwellers_amount = result.getCurrentDwellersAmount()
        self.game.resources_panel.curr_max_dwellers_amount = result.getCurrentDwellersMaxAmount()

    def stop_production(self, building_id):
        """ Stop production in given building.

        :param building_id: id of the building where production will be stopped
        """
        result = self.sender.entry_point.getMapPresenter().stopProduction(building_id)
        self.game.resources_panel.resources_values = \
            Converter().convertJavaMapToDict(result.getActualResourcesValues())
        self.game.resources_panel.resources_incomes = \
            Converter().convertJavaMapToDict(result.getActualResourcesIncomes())
        self.game.resources_panel.curr_dwellers_amount = result.getCurrentDwellersAmount()
        self.game.resources_panel.curr_max_dwellers_amount = result.getCurrentDwellersMaxAmount()
        self.game.info_panel.curr_building.is_running = result.isBuildingRunning()
        self.game.info_panel.set_stop_production_button_texture()

# =================================================================================================================== #
# Reading messages from model
# =================================================================================================================== #
    def init(self, resources, buildings, texture_one, texture_two, initial_resources_values,
             initial_resources_incomes):
        """ Initialize game -> create game instance. After creating game instance send acknowledgement to model. """
        self.game = Game(self.width, self.height, texture_one, texture_two, buildings, resources,
                         initial_resources_values, initial_resources_incomes, self)
        self.sender.entry_point.getMapPresenter().viewInitialized()

    def update_resources_values(self, actual_resources_values, actual_resources_incomes):
        """ Update resources values """
        self.game.resources_panel.resources_values = Converter().convertJavaMapToDict(actual_resources_values)
        self.game.resources_panel.resources_incomes = Converter().convertJavaMapToDict(actual_resources_incomes)

    def resume_game(self):
        """ Resume game. """
        self.game.set_display_mode()
        self.game.game_on = True
        self.game.listener_thread = GameThread(self.game)
        self.game.listener_thread.start()

