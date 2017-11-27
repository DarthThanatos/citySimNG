import json
import unittest

import wx
import os

from CreatorView.ResourceSheet import ResourceSheet
from ViewSetter import CreatorHolder
from viewmodel.SheetEntityChecker import AddModeSheetEntityChecker, EditModeSheetEntityChecker


class ResourceSheetTest(unittest.TestCase):

    def setUp(self):
        self.app = wx.App(False)
        os.chdir("..")
        ch = CreatorHolder( parent = None , tplSize = (0,0), sender = None, gateway = None)
        self.resourceSheetView = ResourceSheet(parent = ch, size = (0,0), frame = None, currentDependencies = {})
        self.addMode = AddModeSheetEntityChecker(self.resourceSheetView)
        self.editMode = EditModeSheetEntityChecker(self.resourceSheetView)

    def test_that_correct(self):
        with open("citySimNGView\\CreatorView\\test\\deps\\correct_deps", "r+") as f:
            content = f.read()
            currentDependencies = json.loads(content)
            self.resourceSheetView.currentDependencies = currentDependencies
            self.resourceSheetView.setUpEditMode(edit_element_name = "Rock")
            result_struct = self.editMode.newResultStruct()
            correct = self.resourceSheetView.getEntityChecker().entityCorrect(self.editMode, result_struct)
            self.assertTrue(correct)


if __name__ == "__main__":
    unittest.main()