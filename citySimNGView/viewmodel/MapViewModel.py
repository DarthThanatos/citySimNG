from wx import wx
import pygame


class MapViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayMap(self):
        wx.CallAfter(self.viewSetter.setView, 'Map')

    def init(self, resources, buildings, texture_one, texture_two, initial_resources_values, initial_resources_incomes):
        wx.CallAfter(self.viewSetter.getView('Map').init, resources, buildings, texture_one, texture_two,
                     initial_resources_values, initial_resources_incomes)

    def updateResourcesValues(self, actualResourcesValues, actualResourcesIncomes):
        wx.CallAfter(self.viewSetter.getView('Map').update_resources_values, actualResourcesValues,
                     actualResourcesIncomes)

    def resumeGame(self):
        wx.CallAfter(self.viewSetter.getView('Map').resume_game)

    class Java:
        implements = ["py4jmediator.ViewModel$MapViewModel"]
