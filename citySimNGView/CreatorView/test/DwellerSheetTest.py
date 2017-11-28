import json
import unittest

import wx
import os

from CreatorView.DwellersSheet import DwellersSheet
from CreatorView.CreatorSwitcher import CreatorSwitcher
from ViewSetter import CreatorHolder
from viewmodel.SheetEntityChecker import AddModeSheetEntityChecker, EditModeSheetEntityChecker

DIR_TO_TEST_DEPS = "citySimNGView\\CreatorView\\test\\deps\\dweller_sheet_test_deps\\"
DEBUG = False

class DwellerSheetTest(unittest.TestCase):

    def setUp(self):
        self.app = wx.App(False)
        os.chdir("..")
        ch = CreatorHolder( parent = None , tplSize = (0,0), sender = None, gateway = None)
        self.dwellerSheetView = DwellersSheet(
            parent = ch,
            size = (0, 0),
            frame = None,
            currentDependencies = CreatorSwitcher(
                parent = ch, size=(0,0), name="", musicPath= "TwoMandolins.mp3", sender=None
            ).newCurrentDependencies()
        )
        self.addMode = AddModeSheetEntityChecker(self.dwellerSheetView)
        self.editMode = EditModeSheetEntityChecker(self.dwellerSheetView)

    def tearDown(self):
        os.chdir("citySimNGView")

    def expect(self, path_to_dep, entityName, shouldAssertCorrect, expectedMsgs = None, notExpectedMsgs = None):
        with open(DIR_TO_TEST_DEPS + path_to_dep, "r+") as f:
            content = f.read()
            currentDependencies = json.loads(content)
            for key in currentDependencies.keys():
                self.dwellerSheetView.currentDependencies[key] = currentDependencies[key]
            try:
                self.dwellerSheetView.setUpEditMode(edit_element_name = entityName)
            except Exception as e:
                print e.message
            result_struct = self.editMode.newResultStruct()
            correct = self.dwellerSheetView.getEntityChecker().entityCorrect(self.editMode, result_struct)
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
            entityName="Dweller",
            shouldAssertCorrect=True
        )

    def test_that_white_space_name_invalid(self):
        if DEBUG: print "white space"
        self.expect(
            path_to_dep="incorrect_dweller_name",
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
            entityName="Dweller",
            shouldAssertCorrect=False,
            expectedMsgs = [
                "Dweller name is different than the name record: NotDweller"
            ]
        )


    def test_that_invalid_paths_detected(self):
        if DEBUG: print "invalid paths"
        self.expect(
            path_to_dep="invalid-textures",
            entityName="InvalidTexture",
            shouldAssertCorrect=False,
            expectedMsgs=[
                "does not contain a valid graphical file"
            ]
        )

    def test_that_multiple_invalid_fields_detected(self):
        if DEBUG: print "invalid fields"
        self.expect(
            path_to_dep="invalid-multiple-fields",
            entityName="InvalidDweller",
            shouldAssertCorrect=False,
            expectedMsgs=[
                "Please enter description of this Dweller",
                "Pick at least one VALID element in the section \"Consumed resources\""
            ]
        )



if __name__ == "__main__":
    unittest.main()