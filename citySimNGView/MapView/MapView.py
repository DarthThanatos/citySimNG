import json
import os
import threading
import traceback
import pygame
import thread
import wx

from CreatorView.RelativePaths import relative_music_path, relative_textures_path

from Consts import RESOURCES_PANEL_HEIGHT, PURPLE, get_font, TEXT_PANEL_HEIGHT, \
    TEXT_PANEL_WIDTH, MENU_BUTTON_WIDTH, NAVIGATION_PANEL_WIDTH, \
    INFO_PANEL_WIDTH, TEXT_PANEL_FONT_SIZE, YELLOW, \
    BUILDINGS_PANEL_WIDTH, HINT_TEXTURE
from Game import Game
from GameThread import GameThread
from Utils import draw_text, draw_text_with_wrapping_and_centering
from Converter import Converter
from Modals.ClosedHintModal import ClosedHintModal, HINT_WIDTH, HINT_HEIGHT
from Items.Resources import resources as game_resources
from Items.Dwellers import dwellers as game_dwellers


BUTTON_HEIGHT = 0.15
SUMMARY_MENU_BUTTON_HEIGHT = 0.1
SUMMARY_MENU_BUTTON_WIDTH = 0.1
FONT_SIZE = 25

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

        self.sizer_elements = []

        # bind EVT_SHOW to onShow() function
        self.Bind(wx.EVT_SHOW, self.on_show, self)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.SetSizer(self.sizer)

    def add_log_panel(self):
        style = wx.TE_MULTILINE | wx.TE_READONLY
        self.log = wx.TextCtrl(self, wx.ID_ANY,
                               size=(self.width * TEXT_PANEL_WIDTH,
                                     TEXT_PANEL_HEIGHT * self.height),
                               style=style,
                               pos=(self.width * NAVIGATION_PANEL_WIDTH +
                                    self.width * INFO_PANEL_WIDTH,
                                    int(self.height - TEXT_PANEL_HEIGHT *
                                        self.height)))
        font = wx.Font(TEXT_PANEL_FONT_SIZE, wx.MODERN, wx.NORMAL, wx.NORMAL,
                       False, get_font())
        self.log.SetFont(font)
        self.sizer.Add(self.log, 1, wx.ALL | wx.EXPAND, 5)
        self.sizer_elements.append(self.log)

    def init_btns_in_game_screen(self):
        """ Function initializing buttons. """
        menu_btn = wx.Button(
            self, label="Menu", pos=(
                self.width - BUILDINGS_PANEL_WIDTH / 2 * self.width,
                self.screen_height - self.screen_height * TEXT_PANEL_HEIGHT),
            size=(BUILDINGS_PANEL_WIDTH / 2 * self.width,
                  self.screen_height * TEXT_PANEL_HEIGHT))

        end_game_btn = wx.Button(self, label="End game", pos=(
            self.width - 2 * BUILDINGS_PANEL_WIDTH / 2 * self.width,
            self.screen_height - self.screen_height * TEXT_PANEL_HEIGHT),
            size=(BUILDINGS_PANEL_WIDTH / 2 * self.width,
                  self.screen_height * TEXT_PANEL_HEIGHT))

        self.sizer.Add(menu_btn)
        self.sizer.Add(end_game_btn)
        self.Bind(wx.EVT_BUTTON, self.ret_to_menu, menu_btn)
        self.Bind(wx.EVT_BUTTON, self.end_game, end_game_btn)
        self.sizer_elements.append(menu_btn)
        self.sizer_elements.append(end_game_btn)

    def init_btns_in_end_game_screen(self):
        menu_btn = wx.Button(
            self, label="Menu", pos=(
                self.width/2 - SUMMARY_MENU_BUTTON_WIDTH * self.screen_height/2,
                self.screen_height - self.screen_height * SUMMARY_MENU_BUTTON_HEIGHT),
            size=(SUMMARY_MENU_BUTTON_WIDTH * self.screen_height,
                  self.screen_height * SUMMARY_MENU_BUTTON_HEIGHT))
        self.sizer.Add(menu_btn)
        self.Bind(wx.EVT_BUTTON, self.ret_to_menu, menu_btn)
        self.sizer_elements.append(menu_btn)

    def remove_button(self, btn):
        """"""
        self.sizer.Hide(btn)
        self.sizer.Remove(btn)

    def on_show(self, event):
        """ Function receiving events sent to map view. """
        if event.GetShow():
            self.init_view()
            try:
                pygame.mixer.init()
            except Exception:
                print "Problem with music"
        # else:
        #     try:
        #         pygame.quit()
        #     except Exception:
        #         print "first appearance of MapView: pygame not initialized in map"

    def init_view(self):
        """ Function initializing map view. """
        self.add_log_panel()
        self.init_btns_in_game_screen()
        self.hackPygame()
        pygame.init()
        pygame.display.init()
        self.sender.entry_point.getMapPresenter().viewInitialized()

    def hackPygame(self):
        global pygame
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame  # this has to happen after setting the environment variables.
        pygame.init()
        pygame.quit()

    def end_game(self, event):
        self.game.game_on = False
        self.game.listener_thread.join()

        [self.remove_button(elem) for elem in self.sizer_elements]
        self.init_btns_in_end_game_screen()
        image = pygame.image.load(self.game.panel_texture)
        image = pygame.transform.scale(image,
                                       (self.game.board_width,
                                        self.game.board_height))
        self.game.game_board.blit(image, (0, 0))

        res = self.sender.entry_point.getMapPresenter().endGame()
        resources = Converter().convertJavaMapToDict(res.getResourcesSummary())
        domestic = Converter().convertJavaMapToDict(res.getDomesticBuildingsSummary())
        industrial = Converter().convertJavaMapToDict(res.getIndustrialBuildingsSummary())
        dwellers = Converter().convertJavaMapToDict(res.getDwellersSummary())
        score = res.getScore()

        self.draw_summary(resources, domestic, industrial, dwellers, score)
        self.game.background.blit(self.game.game_board, (0, 0))

        pygame.display.flip()

    def draw_summary(self, resources, domestic, industrial, dwellers, score):
        curr_y = 0
        max_y = 0

        curr_y = draw_text_with_wrapping_and_centering(
            0, 0, self.width, "Game Summary\n ", self.game.game_board, YELLOW,
        FONT_SIZE + 10)

        mes = ' '.join(['{} {}\n'.format(key, val) for key, val in
               resources.iteritems()])
        mes = 'Resources summary\n\n ' + mes
        max_y = max(max_y, draw_text_with_wrapping_and_centering(
            0, curr_y, self.width / 4, mes, self.game.game_board, YELLOW,
            FONT_SIZE, True))

        mes = ' '.join(['{} {}\n'.format(key, val) for key, val in
                        domestic.iteritems()])
        mes = 'Domestic buildings\n summary\n\n ' + mes
        max_y = max(max_y, draw_text_with_wrapping_and_centering(
            self.width / 4, curr_y, 2 * self.width / 4, mes,
            self.game.game_board, YELLOW, FONT_SIZE, True))

        mes = ' '.join(['{} {}\n'.format(key, val) for key, val in
                        industrial.iteritems()])
        mes = 'Industrial buildings\n summary\n\n ' + mes
        max_y = max(max_y, draw_text_with_wrapping_and_centering(
            2 * self.width / 4, curr_y, 3 * self.width / 4, mes, self.game.game_board,
            YELLOW, FONT_SIZE, True))

        mes = ' '.join(['{} {}\n'.format(key, val) for key, val in
                        dwellers.iteritems()])
        mes = 'Dwellers summary\n\n ' + mes
        max_y = max(max_y, draw_text_with_wrapping_and_centering(
            3 * self.width / 4, curr_y, self.width, mes, self.game.game_board,
            YELLOW, FONT_SIZE, True))

        curr_y = max(max_y, int(0.85 * self.height))
        mes = "Score: {}".format(score)
        draw_text_with_wrapping_and_centering(0, curr_y, self.width, mes,
                                              self.game.game_board, YELLOW,
                                              FONT_SIZE + 10)

# =================================================================================================================== #
# Communication with model
# =================================================================================================================== #

# =================================================================================================================== #
# Functions sending messages to model
# =================================================================================================================== #

    def ret_to_menu(self, event):
        """ Send node change message to model. """
        [self.remove_button(elem) for elem in self.sizer_elements]
        self.game.game_on = False
        self.game.listener_thread.join()
        self.map_view_initialized = False
        self.sender.entry_point.getMapPresenter().goToMenu()

    def erected_building(self, building):
        """ Send message to model that new building has been erected. """
        result = self.sender.entry_point.getMapPresenter().placeBuilding(building.name, building.id)
        self.game.resources_panel.resources_values = \
            Converter().convertJavaMapToDict(result.getActualResourcesValues())
        self.game.resources_panel.resources_incomes = Converter().convertJavaMapToDict(
            result.getActualResourcesIncomes())
        self.game.resources_panel.resources_consumption = Converter().convertJavaMapToDict(
            result.getActualResourcesConsumption())
        self.game.resources_panel.resources_balance = Converter().convertJavaMapToDict(result.getResourcesBalance())
        self.game.resources_panel.curr_dwellers_amount = result.getNeededDwellers()
        self.game.resources_panel.curr_max_dwellers_amount = result.getAvailableDwellers()
        self.game.buildings_panel.enable_buildings(result.getEnabledBuildings())
        building.working_dwellers = result.getWorkingDwellers()

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
        self.game.resources_panel.resources_incomes = Converter().convertJavaMapToDict(
            result.getActualResourcesIncomes())
        self.game.resources_panel.resources_consumption = Converter().convertJavaMapToDict(
            result.getActualResourcesConsumption())
        self.game.resources_panel.resources_balance = Converter().convertJavaMapToDict(result.getResourcesBalance())
        self.game.resources_panel.curr_dwellers_amount = result.getNeededDwellers()
        self.game.resources_panel.curr_max_dwellers_amount = result.getAvailableDwellers()

    def stop_production(self, building_id):
        """ Stop production in given building.

        :param building_id: id of the building where production will be stopped
        """
        result = self.sender.entry_point.getMapPresenter().stopProduction(building_id)
        self.game.resources_panel.resources_values = \
            Converter().convertJavaMapToDict(result.getActualResourcesValues())
        self.game.resources_panel.resources_incomes = Converter().convertJavaMapToDict(
            result.getActualResourcesIncomes())
        self.game.resources_panel.resources_consumption = Converter().convertJavaMapToDict(
            result.getActualResourcesConsumption())
        self.game.resources_panel.resources_balance = Converter().convertJavaMapToDict(result.getResourcesBalance())
        self.game.resources_panel.curr_dwellers_amount = result.getNeededDwellers()
        self.game.resources_panel.curr_max_dwellers_amount = result.getAvailableDwellers()
        self.game.info_panel.curr_building.is_running = result.isRunning()
        self.game.info_panel.set_stop_production_button_texture()

    def set_dwellers_working_in_building(self, building_id):
        """ Get number of dwellers working in given building.

        :param building: building for which get information
        """
        result = self.sender.entry_point.getMapPresenter().getWorkingDwellers(building_id)
        self.game.info_panel.curr_building.working_dwellers = result

# =================================================================================================================== #
# Reading messages from model
# =================================================================================================================== #
    def init(self, resources, domestic_buildings, industrial_buildings, dwellers,
             texture_one, texture_two,  panelTexture, mp3, initial_resources_values,
             initial_resources_incomes, initial_resources_consumption,
             initial_resources_balance, available_dwellers):
        """ Initialize game -> create game instance. After creating game instance send acknowledgement to model. """
        self.music_path = relative_music_path + mp3
        pygame.mixer.music.load(self.music_path)
        pygame.mixer.music.play()

        game_resources.clear()
        game_dwellers.clear()

        self.game = Game(
            self.width,
            self.height,
            texture_one,
            texture_two,
            domestic_buildings,
            industrial_buildings,
            resources,
            dwellers,
            initial_resources_values,
            initial_resources_incomes,
            initial_resources_consumption,
            initial_resources_balance,
            self,
            available_dwellers,
            panelTexture)
        self.sender.entry_point.getMapPresenter().viewInitialized()
        self.parent.parent.turnLoadingScreenOff()

    def update_values_for_cycle_thread(self, actual_resources_values,
                                actual_resources_incomes,
                                actual_resources_consumption,
                                resources_balance, needed_dwellers,
                                available_dwellers):
        """ Update resources values """
        res_vals = Converter().convertJavaMapToDict(actual_resources_values)
        self.game.resources_panel.resources_values = res_vals
        res_incomes = Converter().convertJavaMapToDict(actual_resources_incomes)
        self.game.resources_panel.resources_incomes = res_incomes
        res_consumption = Converter().convertJavaMapToDict(actual_resources_consumption)
        self.game.resources_panel.resources_consumption = res_consumption
        res_balance = Converter().convertJavaMapToDict(resources_balance)
        self.game.resources_panel.resources_balance = res_balance
        self.game.resources_panel.curr_dwellers_amount = needed_dwellers
        self.game.resources_panel.curr_max_dwellers_amount = available_dwellers

    def update_values_for_cycle(self, actual_resources_values,
                                actual_resources_incomes,
                                actual_resources_consumption,
                                resources_balance, needed_dwellers,
                                available_dwellers):
        thread.start_new_thread(self.update_values_for_cycle_thread, ( actual_resources_values,
                                actual_resources_incomes,
                                actual_resources_consumption,
                                resources_balance, needed_dwellers,
                                available_dwellers))

    def resume_game(self):
        """ Resume game. """
        self.game.set_display_mode()
        self.game.game_on = True
        self.game.listener_thread = GameThread(self.game)
        self.game.listener_thread.start()
        self.parent.parent.turnLoadingScreenOff()

    def handle_hints(self, hints):
        print hints[:5]
        hint_modal_sprite = ClosedHintModal(self.game.board_height,
                                            HINT_WIDTH * self.game.board_width,
                                            HINT_HEIGHT * self.game.board_height,
                                            HINT_TEXTURE,
                                            self.game.game_board, hints,
                                            self.game.expand_hint_modal,
                                            min(4, len(self.game.hint_modals_sprites)))
        if len(self.game.hint_modals_sprites) >= 5:
            self.game.hint_list.append(hint_modal_sprite)
        else:
            self.game.hint_modals_sprites.add(hint_modal_sprite)

