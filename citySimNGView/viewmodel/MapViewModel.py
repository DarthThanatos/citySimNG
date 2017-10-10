from wx import wx
import pygame


class MapViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayMap(self):
        wx.CallAfter(self.viewSetter.setView, 'Map')

    def init(self, resources, buildings, texture_one, texture_two, initial_resources_values, initial_resources_incomes,
             initial_resources_consumption, initial_resources_balance):
        wx.CallAfter(self.viewSetter.getView('Map').init, resources, buildings, texture_one, texture_two,
                     initial_resources_values, initial_resources_incomes, initial_resources_consumption,
                     initial_resources_balance)

    def updateResourcesValues(self, actual_resources_values, actual_resources_incomes, actual_resources_consumption,
                              resources_balance):
        wx.CallAfter(self.viewSetter.getView('Map').update_resources_values, actual_resources_values,
                     actual_resources_incomes, actual_resources_consumption, resources_balance)

    def resumeGame(self):
        wx.CallAfter(self.viewSetter.getView('Map').resume_game)

    class Java:
        implements = ["py4jmediator.ViewModel$MapViewModel"]
