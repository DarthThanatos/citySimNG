import unittest

import wx
import os
import json

from CreatorView import CreatorConfig, Consts
from CreatorView.CreatorSwitcher import CreatorSwitcher
from ViewSetter import CreatorHolder
from viewmodel.DependenciesFileLoader import DependenciesFileLoader

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

    def expect(self, path_to_dep,  shouldAssertCorrect, expectedMsgs = None, notExpectedMsgs = None):
        with open(DIR_TO_TEST_DEPS + path_to_dep, "r+") as f:
            content = f.read()
            currentDependencies = json.loads(content)
            for key in currentDependencies.keys():
                self.creator_main_panel.current_dependencies[key] = currentDependencies[key]

            correct = self.creator_main_panel.currentDependenciesCorrect(updateNameFromInput=False)

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

    def test_that_deps_correct(self):
        self.expect(
            path_to_dep="correct_deps",
            shouldAssertCorrect=True
        )


    def test_that_building_lacking_key_detected(self):
        self.expect(
            path_to_dep="buildings-lacking-keys",
            shouldAssertCorrect=False,
            expectedMsgs=[
                "Building misses record: Predecessor",
                "Building has a non-recognizable record: Succcessor",
                "Building misses record: Successor"
            ]
        )


    def test_dweller_key_lack_detected(self):
        self.expect(
            path_to_dep="dwellers-lacking-keys",
            shouldAssertCorrect=False,
            expectedMsgs = [
                "Dweller misses record: Description",
                "Dweller misses record: Successor",
                "Dweller has a non-recognizable record: Succcessor"
            ]
        )

    def test_resource_key_lack_detected(self):
        self.expect(
            path_to_dep="resources-lacking-keys",
            shouldAssertCorrect=False,
            expectedMsgs = [
                "NoTexturePath misses record: Texture path",
                "NoTexturePath misses record: Predecessor",
                "NoTexturePath has a non-recognizable record: Predeccessor"
            ]
        )


    def test_incorrect_textures_paths_detected(self):
        self.expect(
            path_to_dep="incorrect_textures_paths",
            shouldAssertCorrect=False,
            expectedMsgs=[
                "File resources\Textures\wrong_texture_one.xxx is not a valid graphical file",
                "File resources\Textures\wrong_texture_two.xxx is not a valid graphical file",
                "File resources\Music\wrong_mp3_file.xxx is not a valid .mp3  file",
                "File resources\Textures\wrong_panel_texture.xxx is not a valid graphical file"
            ]
        )

    def test_incorrect_set_name_detected(self):
        self.expect(
            path_to_dep="incorrect_set_name",
            shouldAssertCorrect=False,
            expectedMsgs=[
                "Dependencies set name field not correct"
            ]
        )


    def init_creator_with_deps(self, path_to_dep):
        with open(DIR_TO_TEST_DEPS + path_to_dep, "r+") as f:
            content = f.read()
            currentDependencies = json.loads(content)
            for key in currentDependencies.keys():
                self.creator_main_panel.current_dependencies[key] = currentDependencies[key]


    def test_clean(self):
        self.init_creator_with_deps("correct_deps")
        self.creator_main_panel.clean()
        assert self.creator_main_panel.current_dependencies[Consts.SET_NAME] ==  CreatorConfig.DEPENDENCIES_DEFAULT_SET_NAME
        assert self.creator_main_panel.current_dependencies[Consts.MP3] == CreatorConfig.MP3_DEFAULT_NAME
        assert self.creator_main_panel.current_dependencies[Consts.TEXTURE_ONE] == CreatorConfig.TEXTURE_ONE_DEFAULT_NAME
        assert self.creator_main_panel.current_dependencies[Consts.TEXTURE_TWO] == CreatorConfig.TEXTURE_TWO_DEFAULT_NAME
        assert self.creator_main_panel.current_dependencies[Consts.PANEL_TEXTURE] == CreatorConfig.PANEL_TEXURE_DEFAULT_NAME
        assert self.creator_main_panel.current_dependencies[Consts.RESOURCES] == {}
        assert self.creator_main_panel.current_dependencies[Consts.BUILDINGS] == {}
        assert self.creator_main_panel.current_dependencies[Consts.DWELLERS] == {}



    def test_past_deps_restored_on_wrong_input(self):
        self.init_creator_with_deps("correct_deps")
        deps_before = dict(self.creator_main_panel.current_dependencies)
        DependenciesFileLoader(self.creator_main_panel).onLoadFileSelected(DIR_TO_TEST_DEPS + "incorrect_textures_paths")
        assert deps_before == self.creator_main_panel.current_dependencies



    def expectMsg(self, expectedMsgs, error_msg):
        for expectedMsg in expectedMsgs:
            self.assertTrue(
                expectedMsg in error_msg,
                "Expected error msg: \"" + expectedMsg + "\" but it was not there!"
            )

    def test_all_not_redundant(self):
        self.init_creator_with_deps("redundant_entities")
        self.creator_main_panel.createDependencies(None)
        error_msg = self.creator_main_panel.logArea.GetValue()
        if DEBUG:
            print error_msg
        expectedMsgs=  \
            [
                "Resource1 is redundant"
             ]
        self.expectMsg(expectedMsgs, error_msg)



    def test_empty_deps_detected(self):
        self.init_creator_with_deps("empty")
        self.creator_main_panel.createDependencies(None)
        error_msg = self.creator_main_panel.logArea.GetValue()
        if DEBUG:
            print error_msg
        expectedMsgs=  \
            [
                "Dwellers list empty, please fill it",
                "Buildings list empty, please fill it",
                "Resources list empty, please fill it"
             ]
        self.expectMsg(expectedMsgs, error_msg)

    def test_missing_metadata_detected(self):
        with open(DIR_TO_TEST_DEPS + "missing_metadata_key", "r+") as f:
            content = f.read()
            no_keys_whatsoever_dict = json.loads(content)
            try:
                self.creator_main_panel.fillCurrentDependenciesWithValidContent(no_keys_whatsoever_dict)
            except Exception:
                pass
            error_msg = self.creator_main_panel.logArea.GetValue()
            if DEBUG:
                print error_msg
            self.expectMsg(
                expectedMsgs=[
                    "Selected .dep file misses record: Buildings"
                ],
                error_msg = error_msg
            )



if __name__ == "__main__":
    unittest.main()