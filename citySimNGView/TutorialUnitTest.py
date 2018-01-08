import unittest

import os
import wx

from TutorialView import TutorialView
from ViewSetter import TutorialHolder

class TutorialUnitTest(unittest.TestCase):

    def setUp(self):
        self.app = wx.App(False)
        os.chdir("..")
        holder = TutorialHolder( parent = None , tplSize = (100,100), sender = None, gateway = None)
        self.tutorial = holder.tutorialView

    def tearDown(self):
        os.chdir("citySimNGView")

    def testDisplayTutorialIndex(self):
        TUTORIAL_INDEX = [
            "Game - overview",
            "Tutorial - how to use",
            "Map - overview",
            "Map - buildings panel",
            "Map - resources panel",
            "Exchange - overview",
            "Exchange - transactions",
            "Exchange - lottery"
        ];
        self.tutorial.fetchTutorialIndex(TUTORIAL_INDEX)
        mySum = len(self.tutorial.tab1.leftBox.GetChildren()) + len(self.tutorial.tab1.middleBox.GetChildren()) + len(self.tutorial.tab1.rightBox.GetChildren())

        self.assertEqual(mySum/2, len(TUTORIAL_INDEX))


    def testDisplayBuildingsIndex(self): 
        BUILDING_INDEX = [
            "Zamek",
            "Mennica",
            "Siedziba szlachty",
            "Dom mieszczanina",
            "Chata chlopska",
            "Kamieniolom",
            "Pole uprawne",
            "Sad",
            "Pole chmielu",
            "Browar",
        ];
        self.tutorial.fetchNodes(BUILDING_INDEX, [], [])
        mySum = len(self.tutorial.tab2.leftBox.GetChildren()) + len(self.tutorial.tab2.middleBox.GetChildren()) + len(self.tutorial.tab2.rightBox.GetChildren())
        self.assertEqual(mySum/2, len(BUILDING_INDEX))

    def testDisplayResourcesIndex(self): 
        RESOURCES_INDEX = [
            "Chleb",
            "Maka",
            "Sol",
            "Zboze",
            "Zloto"
        ];
        self.tutorial.fetchNodes([], RESOURCES_INDEX, [])
        mySum3 = len(self.tutorial.tab3.leftBox.GetChildren()) + len(self.tutorial.tab3.middleBox.GetChildren()) + len(self.tutorial.tab3.rightBox.GetChildren())
        self.assertEqual(mySum3/2, len(RESOURCES_INDEX))

    def testDisplayDwellersIndex(self): 
        DWELLER_INDEX = [
            "Moznowladca",
            "Mieszczanin",
            "Chlop",
            "Szlachcic"
        ];

        self.tutorial.fetchNodes([], [], DWELLER_INDEX)
        mySum2 = len(self.tutorial.tab4.leftBox.GetChildren()) + len(self.tutorial.tab4.middleBox.GetChildren()) + len(self.tutorial.tab4.rightBox.GetChildren())
        self.assertEqual(mySum2/2, len(DWELLER_INDEX))

    def testTutorialPage(self):
        nr = 315
        sub0 = "CitySimNG"
        img = "resources\\Tutorial\\img6.jpg";
        page = {
            "Args":
                {
                "nr": nr,
                "sub0": [sub0,],
                "sub1": ["Start!",],
              "img": img,
                "link": []
            }}
        self.tutorial.displayTutorialPage(page)
        self.assertEqual(self.tutorial.pageView.contentField.GetValue(), sub0+"\n")
        self.assertEqual(self.tutorial.pageView.subPage, 0)
        self.assertEqual(self.tutorial.pageView.nrOfSubpages, 2)
        self.assertEqual(self.tutorial.pageView.page, nr)
        self.assertEqual(self.tutorial.pageView.tabID, 3)
        # self.assertEqual(self.tutorial.pageView.hyperlinks[0]['label'], "")


if __name__ == '__main__':
    unittest.main()