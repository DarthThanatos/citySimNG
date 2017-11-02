import wx

class ImageUtils(object):

    def __init__(self, view):
        self.view = view

    def newScaledImgBmpInDir(self,path_to_dir,file_name):
        #path_to_dir: if the root folder is citySimNG, then its in the form: dir\\in\\resources\\
        return self.newScaledImgBitmap(path_to_dir + file_name)

    def newScaledImg(self, non_relative_path):
        image = wx.Image(name = non_relative_path) #"..\\..\\resources\\Textures\\DefaultBuilding.jpg"
        return image.Scale(32,32)

    def newScaledImgBitmap(self, non_relative_path):
        return wx.StaticBitmap(self.view, wx.ID_ANY, wx.BitmapFromImage(self.newScaledImg(non_relative_path)), size = (32,32))