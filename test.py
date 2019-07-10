import os
import re
import requests
import urllib
import wget
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

# trying to download the radios
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

# api.user_timeline
'''# the maximum number of twitters is 200 per time
all_tweets = api.user_timeline(screen_name=user, count=200, include_rts=False, exclude_replies=True)
if all_tweets:
    last_tweet_id = all_tweets[-1].id
else:
    last_tweet_id = 0

# get more tweets
count = 0
while count < 5:
    # get more tweets posted earlier than max_id
    more_tweets = api.user_timeline(screen_name=user, count=200, include_rts=False, exclude_replies=True,
                                    max_id=last_tweet_id - 1)
    # break if there is no more older tweets; otherwise keep searching until all the tweets of this user can be found
    if len(more_tweets) == 0:
        break
    else:
        last_tweet_id = more_tweets[-1].id - 1
        all_tweets = all_tweets + more_tweets
    count += 1'''

# use functions without multiple thread
'''downloadPhoto(photo, files[1])
downloadVideo(original_video[0], original_video[1], files[2])
getVideoFromYouTube(user, all_tweets, files[0], files[3])
getAudio(user, all_tweets, files[0], files[4])'''

# wget.download('https://pbs.twimg.com/media/D_FZoE1UIAESADq.jpg:large')
url = 'https://pbs.twimg.com/media/D_FZoE1UIAESADq.jpg:large'
# r = requests.get(url)
# with open('./1.jpg:large', 'wb') as f:
#         f.write(r.content)
# urllib.request.urlretrieve(url, './1')

files = os.listdir("C:/Users/alina/Desktop/Twitter_crawler_by_APIs/mengnanlan/Image")
for filename in files:
    portion = os.path.splitext(filename)
    if portion[1] == ".unknown_video":
        newname = portion[0] + ".jpg"
        os.rename(filename, newname)

# s = 'https://www.youtube.com/watch?v=EwJf5fw57Yo'
# s = 'https://youtu.be/EoVP8uMMJc4'
# if re.match('https://youtu.be/', s):
#     a = re.split('/',s)[-1]
# print(a)
# s = 'https://www.youtube.com/watch?v=DL7eonPOORM&list=PLoB11Z8A5Nz9Z8KQQPG_Uxkj6H497XlgD&index=1'
# s = re.split('v=',s)
# a = re.split('&',s[-1])[0]
# print(a)