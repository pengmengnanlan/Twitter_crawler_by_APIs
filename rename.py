import os

files = os.listdir("C:/Users/alina/Desktop/Twitter_crawler_by_APIs/mengnanlan/Image")
for filename in files:
    portion = os.path.splitext(filename)
    if portion[1] == ".unknown_video":
        newname = portion[0] + ".jpg"
        os.rename(filename, newname)