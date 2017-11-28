import json
import unittest

import wx
import os

from CreatorView.ResourceSheet import ResourceSheet
from ViewSetter import CreatorHolder
from viewmodel.SheetEntityChecker import AddModeSheetEntityChecker, EditModeSheetEntityChecker

DIR_TO_TEST_DEPS = "citySimNGView\\CreatorView\\test\\deps\\"

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

    def expect(self, path_to_dep, entityName, shouldAssertTrue, expectedMsgs = None, notExpectedMsgs = None):
        with open(DIR_TO_TEST_DEPS + path_to_dep, "r+") as f:
            content = f.read()
            currentDependencies = json.loads(content)
            self.resourceSheetView.currentDependencies = currentDependencies
            self.resourceSheetView.setUpEditMode(edit_element_name = entityName)
            result_struct = self.editMode.newResultStruct()
            correct = self.resourceSheetView.getEntityChecker().entityCorrect(self.editMode, result_struct)
            if shouldAssertTrue: self.assertTrue(correct)
            else: self.assertFalse(correct)
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
            shouldAssertTrue=True
        )

    def test_that_white_space_name_invalid(self):
        self.expect(
            path_to_dep="incorrect_resource_name",
            entityName=" ",
            shouldAssertTrue=False,
            expectedMsgs = [
                "Not a valid name"
            ]
        )

    def test_that_name_discrepancies_detected(self):
        self.expect(
            path_to_dep="name-key-differs-from-name-record",
            entityName="Resource",
            shouldAssertTrue=False,
            expectedMsgs = [
                "Resource name is different than the name record: NotResource"
            ]
        )


if __name__ == "__main__":
    unittest.main()