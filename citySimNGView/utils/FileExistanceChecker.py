import imghdr
import os

from utils.RelativePaths import relative_textures_path

class FileExistanceChecker(object):

    def __init__(self, logArea = None):
        self.logArea = logArea

    def checkIfGraphicalFileExists(self,fileName, dir = relative_textures_path):
        fileExists = self.graphicalFileExists(fileName, dir)
        if not fileExists and self.logArea is not None:
            self.logArea.AppendText("File " + (dir + fileName) + " is not a valid graphical file\n")
        return fileExists

    def checkIfFileWithExtentionExists(self, dir, fileName, ext):
        fileExists = self.fileWithExtentionExists(dir, fileName, ext)
        if not fileExists and self.logArea is not None:
            self.logArea.AppendText("File " + (dir + fileName) + " is not a valid " + ext + "  file\n")
        return fileExists


    def graphicalFileExists(self, fileName, dir = relative_textures_path):
        return os.path.isfile(dir + fileName) and imghdr.what(dir + fileName) is not None


    def fileWithExtentionExists(self, dir, fileName, ext):
        return os.path.isfile(dir + fileName) and fileName.endswith(ext)
