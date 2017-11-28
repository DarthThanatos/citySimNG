import json
import unittest

import wx
import os

from CreatorView.ResourceSheet import ResourceSheet
from ViewSetter import CreatorHolder
from viewmodel.SheetEntityChecker import AddModeSheetEntityChecker, EditModeSheetEntityChecker

DIR_TO_TEST_DEPS = "citySimNGView\\CreatorView\\test\\deps\\resource_sheet_test_deps\\"
DEBUG = False
class ResourceSheetTest(unittest.TestCase):

    def setUp(self):
        self.app = wx.App(False)
        os.chdir("..")
        ch = CreatorHolder( parent = None , tplSize = (0,0), sender = None, gateway = None)
        self.resourceSheetView = ResourceSheet(parent = ch, size = (0,0), frame = None, currentDependencies = {})
        self.addMode = AddModeSheetEntityChecker(self.resourceSheetView)
        self.editMode = EditModeSheetEntityChecker(self.resourceSheetView)

    def tearDown(self):
        os.chdir("citySimNGView")

    def expect(self, path_to_dep, entityName, shouldAssertCorrect, expectedMsgs = None, notExpectedMsgs = None):
        with open(DIR_TO_TEST_DEPS + path_to_dep, "r+") as f:
            content = f.read()
            currentDependencies = json.loads(content)
            self.resourceSheetView.currentDependencies = currentDependencies
            try:
                self.resourceSheetView.setUpEditMode(edit_element_name = entityName)
            except Exception as e:
                print e.message
            result_struct = self.editMode.newResultStruct()
            correct = self.resourceSheetView.getEntityChecker().entityCorrect(self.editMode, result_struct)
            if shouldAssertCorrect: self.assertTrue(correct)
            else:
                if DEBUG:
                    print result_struct["ErrorMsg"]
                self.assertFalse(correct)
            if expectedMsgs is not None:
                for expectedMsg in expectedMsgs:
                    self.assertTrue(
                        expectedMsg in result_struct["ErrorMsg"],
                        "Expected error msg: \"" + expectedMsg + "\" but it was not there!"
                    )
            if notExpectedMsgs is not None:
                for notExpectedMsg in notExpectedMsgs:
                    self.assertTrue(
                        notExpectedMsg not in result_struct["ErrorMsg"],
                        "Got unexpected error msg: \"" + notExpectedMsg + "\""
                    )

    def test_that_correct(self):
        self.expect(
            path_to_dep="correct_deps",
            entityName="ToConsumeByD",
            shouldAssertCorrect=True
        )

    def test_that_white_space_name_invalid(self):
        if DEBUG: print "white space"
        self.expect(
            path_to_dep="incorrect_resource_name",
            entityName=" ",
            shouldAssertCorrect=False,
            expectedMsgs = [
                "Not a valid name"
            ]
        )

    def test_that_name_discrepancies_detected(self):
        if DEBUG: print "name discrepancies"
        self.expect(
            path_to_dep="name-key-differs-from-name-record",
            entityName="Resource",
            shouldAssertCorrect=False,
            expectedMsgs = [
                "Resource name is different than the name record: NotResource"
            ]
        )

    # def test_that_missings_keys_detected(self):
    #     self.expect(
    #         path_to_dep="buildings-lacking-keys",
    #         entityName="NoPredeccessor",
    #         shouldAssertCorrect=False,
    #         expectedMsgs=[
    #             "NoPredeccessor misses record: Predecessor"
    #         ]
    #     )

    def test_that_invalid_paths_detected(self):
        if DEBUG: print "invalid paths"
        self.expect(
            path_to_dep="invalid-textures",
            entityName="InvalidTextureResource",
            shouldAssertCorrect=False,
            expectedMsgs=[
                "does not contain a valid graphical file"
            ]
        )

    def test_that_multiple_invalid_fields_detected(self):
        if DEBUG: print "invalid fields"
        self.expect(
            path_to_dep="invalid-multiple-fields",
            entityName="InvalidResource",
            shouldAssertCorrect=False,
            expectedMsgs=[
                "Please enter description of this Resource",
                "Start income of this Resource is not valid, needs to be >= 0"
            ]
        )



if __name__ == "__main__":
    unittest.main()