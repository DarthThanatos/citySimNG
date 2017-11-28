import json
import unittest

import wx
import os

from CreatorView.CreatorSwitcher import CreatorSwitcher
from ViewSetter import CreatorHolder

DIR_TO_TEST_DEPS = "citySimNGView\\CreatorView\\test\\deps\\creator_main_panel_test_deps\\"
DEBUG = False

class DwellerSheetTest(unittest.TestCase):

    def setUp(self):
        self.app = wx.App(False)
        os.chdir("..")
        ch = CreatorHolder( parent = None , tplSize = (0,0), sender = None, gateway = None)
        self.creator_switcher = CreatorSwitcher(
                parent = ch, size=(0,0), name="", musicPath= "TwoMandolins.mp3", sender=None
            )
        current_dependencies = self.creator_switcher.newCurrentDependencies()
        self.creator_main_panel = self.creator_switcher.views["main_panel"]

    def tearDown(self):
        os.chdir("citySimNGView")

    def expect(self, path_to_dep, entityName, panel_name, shouldAssertCorrect, expectedMsgs = None, notExpectedMsgs = None):
        with open(DIR_TO_TEST_DEPS + path_to_dep, "r+") as f:
            content = f.read()
            currentDependencies = json.loads(content)
            for key in currentDependencies.keys():
                self.creator_main_panel.current_dependencies[key] = currentDependencies[key]

            correct = self.creator_main_panel.checkEntityHasValidKeys(entityName, panel_name)
            error_msg = self.creator_main_panel.logArea.GetValue()
            if shouldAssertCorrect: self.assertTrue(correct)
            else:
                if DEBUG:
                    print error_msg
                self.assertFalse(correct)
            if expectedMsgs is not None:
                for expectedMsg in expectedMsgs:
                    self.assertTrue(
                        expectedMsg in error_msg,
                        "Expected error msg: \"" + expectedMsg + "\" but it was not there!"
                    )
            if notExpectedMsgs is not None:
                for notExpectedMsg in notExpectedMsgs:
                    self.assertTrue(
                        notExpectedMsg not in error_msg,
                        "Got unexpected error msg: \"" + notExpectedMsg + "\""
                    )

    def test_that_dweller_correct(self):
        self.expect(
            path_to_dep="correct_deps",
            entityName="Dweller",
            panel_name="Dwellers",
            shouldAssertCorrect=True
        )


    def test_that_building_correct(self):
        self.expect(
            path_to_dep="correct_deps",
            entityName="ProducingBuilding",
            panel_name="Buildings",
            shouldAssertCorrect=True
        )


    def test_that_resource_correct(self):
        self.expect(
            path_to_dep="correct_deps",
            entityName="ToProduceByB",
            panel_name="Resources",
            shouldAssertCorrect=True
        )

    def test_building_key_lack_detected(self):
        self.expect(
            path_to_dep="buildings-lacking-keys",
            entityName="Building",
            panel_name="Buildings",
            shouldAssertCorrect=False,
            expectedMsgs = [
                "Building misses record: Predecessor"
            ]
        )

    def test_dweller_key_lack_detected(self):
        self.expect(
            path_to_dep="dwellers-lacking-keys",
            entityName="Dweller",
            panel_name="Dwellers",
            shouldAssertCorrect=False,
            expectedMsgs = [
                "Dweller misses record: Description"
            ]
        )

    def test_resource_key_lack_detected(self):
        self.expect(
            path_to_dep="resources-lacking-keys",
            entityName="NoTexturePath",
            panel_name="Resources",
            shouldAssertCorrect=False,
            expectedMsgs = [
                "NoTexturePath misses record: Texture path"
            ]
        )


if __name__ == "__main__":
    unittest.main()