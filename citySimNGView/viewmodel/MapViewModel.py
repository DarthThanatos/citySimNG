from wx import wx
import pygame
import logging

class MapViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayMap(self):
        wx.CallAfter(self.viewSetter.setView, 'Map')

    def init(self, resources, domestic_buildings, industrial_buildings, dwellers,
             texture_one, texture_two, panelTexture, mp3, initial_resources_values,
             initial_resources_incomes, initial_resources_consumption,
             initial_resources_balance, available_dwellers):
        logging.warning("initializing map")
        wx.CallAfter(self.viewSetter.getView('Map').init,
                     resources,
                     domestic_buildings,
                     industrial_buildings,
                     dwellers,
                     texture_one,
                     texture_two,
                     panelTexture,
                     mp3,
                     initial_resources_values,
                     initial_resources_incomes,
                     initial_resources_consumption,
                     initial_resources_balance,
                     available_dwellers)

    def updateValuesForCycle(self, actual_resources_values,
                             actual_resources_incomes,
                             actual_resources_consumption, resources_balance,
                             needed_dwellers, available_dwellers):
        wx.CallAfter(self.viewSetter.getView('Map').update_values_for_cycle,
                     actual_resources_values,
                     actual_resources_incomes,
                     actual_resources_consumption,
                     resources_balance,
                     needed_dwellers,
                     available_dwellers)

    def resumeGame(self):
        logging.warning("resuming map")
        wx.CallAfter(self.viewSetter.getView('Map').resume_game)

    def sendTutorialHints(self, hints):
        wx.CallAfter(self.viewSetter.getView('Map').handle_hints, hints)

    class Java:
        implements = ["py4jmediator.ViewModel$MapViewModel"]
