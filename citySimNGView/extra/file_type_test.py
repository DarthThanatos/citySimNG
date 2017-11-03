import imghdr
import os
dir = "..\\..\\resources\\Textures\\"
files = os.listdir(dir)
for file in files:
    print "type of ", file, "=", imghdr.what(dir + file)