import json
import os
import threading
import traceback
import pygame

import wx
from RelativePaths import relative_music_path, relative_textures_path

from Consts import RESOURCES_PANEL_SIZE, PURPLE, FONT, TEXT_PANEL_HEIGHT, \
    TEXT_PANEL_WIDTH, MENU_BUTTON_WIDTH, NAVIGATION_PANEL_WIDTH, INFO_PANEL_WIDTH, TEXT_PANEL_FONT_SIZE
from Game import Game
from Utils import draw_text


class MapView(wx.Panel):
    """ This class represents an instance of map view. It is responsible for communication with model. """
    listener_thread = None
    has_reply_arrived = False
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

        self.del_button_sprite = None

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
                # pygame.mixer.music.play()
            except Exception:
                print "Problem with music"
        else:
            try:
                pygame.quit()
            except Exception:
                print "first appearance of MapView: pygame not initialized in map"

    def init_view(self):
        """ Function initializing map view. """
        print "Map: initview"
        global pygame
        os.environ['SDL_WINDOWID'] = str(self.GetHandle())
        os.environ['SDL_VIDEODRIVER'] = 'windib'
        import pygame  # this has to happen after setting the environment variables.
        pygame.init()
        pygame.display.init()

# =================================================================================================================== #
# Communication with model
# =================================================================================================================== #

# =================================================================================================================== #
# Functions sending messages to model
# =================================================================================================================== #

    def ret_to_menu(self, event):
        """ Send node change message to model. """
        msg = dict()
        msg["To"] = "MapNode"
        msg["Operation"] = "MoveTo"
        msg["Args"] = {}
        msg["Args"]["TargetView"] = "GameMenu"
        msg["Args"]["TargetControlNode"] = "GameMenuNode"
        self.sender.send(json.dumps(msg))

    def erected_building(self, building):
        """ Send message to model that new building has been erected. """
        msg = dict()
        msg["To"] = "MapNode"
        msg["Operation"] = "placeBuilding"
        msg["Args"] = {}
        msg["Args"]["BuildingName"] = building.name
        msg["Args"]["BuildingId"] = building.id
        stream = json.dumps(msg)
        self.sender.send(stream)

    def check_if_can_afford(self, building):
        """ Send message to model with the inquiry if player has enough resources to erect building and
        wait for response.

        :param building: building that player wants to erect
        :return: response from model telling if player can afford to erect building
        """
        msg = dict()
        msg["To"] = "MapNode"
        msg["Operation"] = "canAffordOnBuilding"
        msg["Args"] = {}
        msg["Args"]["BuildingName"] = building.name
        msg["Args"]["BuildingId"] = building.id
        stream = json.dumps(msg)

        self.send_mes_and_wait_for_response(stream)
        return self.can_afford_on_building

    def deleted_building(self, building_id):
        """ Send message to model that building has been deleted.

        :param building_id: id of building that will be deleted
        """
        msg = dict()
        msg["To"] = "MapNode"
        msg["Operation"] = "deleteBuilding"
        msg["Args"] = {}
        msg["Args"]["BuildingId"] = building_id
        stream = json.dumps(msg)
        self.sender.send(stream)

    def stop_production(self, building_id):
        """ Stop production in given building.

        :param building_id: id of the building where production will be stopped
        """
        msg = dict()
        msg["To"] = "MapNode"
        msg["Operation"] = "stopProduction"
        msg["Args"] = {}
        msg["Args"]["BuildingId"] = building_id
        stream = json.dumps(msg)
        self.sender.send(stream)


# =================================================================================================================== #
# Reading messages from model
# =================================================================================================================== #
    def readMsg(self, msg):
        """ Function receiving messages from model and setting appropriate variables.

        :param msg: received message
        """
        try:
            parsed_msg = json.loads(msg)
            args = parsed_msg["Args"]
        except:
            traceback.print_exc()
            return

        operation = parsed_msg["Operation"]

        if operation == "Init":
            # create an instance of the Game class
            self.game = Game(self.width, self.height, args["Texture One"], args["Texture Two"],
                             args["buildings"], args["resources"], args["initialResourcesValues"],
                             args["initialResourcesIncomes"], self)

        elif operation == "canAffordOnBuildingResult":
            # we can draw building with given id
            if args["canAffordOnBuilding"]:
                self.can_afford_on_building = True
            else:
                self.can_afford_on_building = False
                self.log.AppendText("You don't have enough resources to build {}\n".format(args["buildingName"]))
            self.condition.acquire()
            self.has_reply_arrived = True
            self.condition.notify()
            self.condition.release()

        elif operation == "placeBuildingResult" or operation == "deleteBuildingResult":
            # if we placed / deleted building we have to update resources
            self.last_res_info = args
            self.game.resources_panel.resources_values = args["actualValues"]
            self.game.resources_panel.resources_incomes = args["actualIncomes"]
            self.game.resources_panel.curr_dwellers_amount = args["currDwellersAmount"]

        elif operation == "Update":
            # update resources values
            self.last_res_info = args
            self.game.resources_panel.resources_values = args["actualValues"]
            self.game.resources_panel.resources_incomes = args["actualIncomes"]

        elif operation == "stopProductionResult":
            self.last_res_info = args

            self.game.info_panel.curr_building.is_running = args["buildingState"]
            self.game.info_panel.set_stop_production_button_texture()

            self.game.resources_panel.resources_values = args["actualValues"]
            self.game.resources_panel.resources_incomes = args["actualIncomes"]
            self.game.resources_panel.curr_dwellers_amount = args["currDwellersAmount"]

        else:
            print "Unknown message"

    def send_mes_and_wait_for_response(self, message):
        """ Send message to model and wait for response.

        :param message: message that will be sent to model
        """
        self.condition.acquire()
        self.has_reply_arrived = False
        self.sender.send(message)
        self.condition.wait()
        self.condition.release()
