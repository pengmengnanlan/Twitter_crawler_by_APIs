import os
import requests
import urllib
from urllib import request
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

# download the radios
'''user_agent = r'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
headers = {'User-Agent': user_agent}
filename = r'D:\p\crawler\code.mp3'
urllib.request.urlretrieve(
    url="https://cf-media.sndcdn.com/bA1dsXOxA0j5.128.mp3?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiKjovL2NmLW1lZGlhLnNuZGNkbi5jb20vYkExZHNYT3hBMGo1LjEyOC5tcDMiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE1NjE0NTYzNTR9fX1dfQ__&Signature=RBzbQppVuOndaNdUvCm5mDgj7WtInMIVHyANURaIiMMxxfAe~BuZnGe2wmqdqEt~sSgOsqnhHD7wQNT2oUQv60B8Znb9YnZ8-0knutkGH2~e4Z2BbGdeKz1fDdLMvDRH5Qq7z7cOo39cjNXVppjEM-sQy8Ip-E6sjuXP10ssTnCpIcydNY1OdJFLY6pxlhTKjmML2hKaJxpyFnXchVYV71lg8us-QTySswmT4qS4nM~NSDj~rJZWRUm9nh9RVTyok~DIhC4maAij9i9zCMmTuQeFJGS6Yyd5eWE5CsPRfs2FBEolE0V7fH01r~MqMAr0hHw7anh-16LqCArEzWyCgA__&Key-Pair-Id=APKAI6TU7MMXM5DG6EPQ",
    filename=None, reporthook=None, data=(filename, headers))'''

'''url = "https://cf-media.sndcdn.com/bA1dsXOxA0j5.128.mp3?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiKjovL2NmLW1lZGlhLnNuZGNkbi5jb20vYkExZHNYT3hBMGo1LjEyOC5tcDMiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE1NjE0NTYzNTR9fX1dfQ__&Signature=RBzbQppVuOndaNdUvCm5mDgj7WtInMIVHyANURaIiMMxxfAe~BuZnGe2wmqdqEt~sSgOsqnhHD7wQNT2oUQv60B8Znb9YnZ8-0knutkGH2~e4Z2BbGdeKz1fDdLMvDRH5Qq7z7cOo39cjNXVppjEM-sQy8Ip-E6sjuXP10ssTnCpIcydNY1OdJFLY6pxlhTKjmML2hKaJxpyFnXchVYV71lg8us-QTySswmT4qS4nM~NSDj~rJZWRUm9nh9RVTyok~DIhC4maAij9i9zCMmTuQeFJGS6Yyd5eWE5CsPRfs2FBEolE0V7fH01r~MqMAr0hHw7anh-16LqCArEzWyCgA__&Key-Pair-Id=APKAI6TU7MMXM5DG6EPQ"
filename = 'D:\p\crawler\code.128.mp3'
r = requests.get(url, stream=True).content
with open(filename, "wb") as mp3:
    mp3.write(r)'''

hashtag = 'youtube'
print(hashtag == 'youtube')