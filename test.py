import os
import requests
import urllib
from PIL import Image
from io import BytesIO

# create the folder automatically
'''nowpath = os.getcwd()
print("The current path：", nowpath)
filename = u'alina'
filnamePath = nowpath+"\\"+filename
os.mkdir(filnamePath)'''

# create folders
'''nowpath = os.getcwd()
filename = u'alina'
image_filename = u'Image'
video_filename = u'Video'
filnamePath1 = nowpath + "\\" + filename + "\\" + image_filename
filnamePath2 = nowpath + "\\" + filename + "\\" + video_filename
os.makedirs(filnamePath1)
os.makedirs(filnamePath2)'''

# download the video by urls
'''url = 'https://video.twimg.com/ext_tw_video/1140752458425221120/pu/vid/720x900/EcTIr1lHhSp--sUG.mp4?tag=10'
r = requests.get(url, stream=True)
with open('test.mp4', "wb") as mp4:
    for chunk in r.iter_content(chunk_size=1024*1024):
        if chunk:
            mp4.write(chunk)'''


# get the width and height of a remote picture by urls
'''path = "http://pbs.twimg.com/media/D9MY3kZU4AAfywA.jpg"
response = requests.get(path)
tmpIm = BytesIO(response.content)
im = Image.open(tmpIm)
w = im.size[0]
h = im.size[1]
print("width：%s" % (w))
print("height：%s" % (h))'''
