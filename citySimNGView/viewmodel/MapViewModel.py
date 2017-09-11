from wx import wx
import pygame


class MapViewModel(object):

    def __init__(self, viewSetter):
        self.viewSetter = viewSetter

    def displayMap(self):
        print "displaying map"
        wx.CallAfter(self.viewSetter.setView, 'Map')
        print "after wx call after"

    def init(self, resources, buildings, texture_one, texture_two, initial_resources_values, initial_resources_incomes):
        wx.CallAfter(self.viewSetter.views['Map'].init, resources, buildings, texture_one, texture_two,
                     initial_resources_values, initial_resources_incomes)

    def updateResourcesValues(self, actualResourcesValues, actualResourcesIncomes):
        wx.CallAfter(self.viewSetter.views['Map'].update_resources_values, actualResourcesValues,
                     actualResourcesIncomes)

    class Java:
        implements = ["py4jmediator.ViewModel$MapViewModel"]
