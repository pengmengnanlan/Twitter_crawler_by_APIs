import tweepy
import json
import time
import threading
import os
import re
import requests
import shutil
import pymysql
from tweepy import OAuthHandler


def Auth():
    with open('twitter_credentials.json') as cred_data:
        info = json.load(cred_data)
        consumer_key = info['CONSUMER_KEY']
        consumer_secret = info['CONSUMER_SECRET']
        access_token = info['ACCESS_KEY']
        access_secret = info['ACCESS_SECRET']

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, proxy="127.0.0.1:1080", wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    return api


def getTweets(api, info):
    all_tweets = []
    # search tweets with the screen_name of user
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=info, tweet_mode='extended').items():
        all_tweets.append(tweet)

    # search tweets with the keywords
    # for tweet in tweepy.Cursor(api.search, q=info, geocode='1.3552217,103.8231561,100km',
    #                            rpp=100, tweet_mode='extended').items(50):
    #     all_tweets.append(tweet)

    return all_tweets


def createFiles(info):
    now_path = os.getcwd()
    filename = u'' + info + ''
    f = now_path + "\\" + filename
    if os.path.exists(f):
        shutil.rmtree(f)
    os.mkdir(f)
    '''image_filename = u'Image'
    video_filename = u'Original_Video'
    youtube_video_filename = u'Youtube_Video'
    audio_filename = u'Audio'
    filename_path_photo = now_path + "\\" + filename + "\\" + image_filename
    filename_path_original_video = now_path + "\\" + filename + "\\" + video_filename
    filename_path_youtube_video = now_path + "\\" + filename + "\\" + youtube_video_filename
    filename_path_audio = now_path + "\\" + filename + "\\" + audio_filename

    if os.path.exists(filename_path_photo):
        shutil.rmtree(filename_path_photo)
    if os.path.exists(filename_path_original_video):
        shutil.rmtree(filename_path_original_video)
    if os.path.exists(filename_path_youtube_video):
        shutil.rmtree(filename_path_youtube_video)
    if os.path.exists(filename_path_audio):
        shutil.rmtree(filename_path_audio)
    os.makedirs(filename_path_photo)
    os.makedirs(filename_path_original_video)
    os.makedirs(filename_path_youtube_video)
    os.makedirs(filename_path_audio)'''
    return [filename, f]


def isVideo(s):
    # if s.startswith('https://youtu.be/') or s.startswith('https://www.youtube.com/') or s.startswith(
    #         'https://vimeo.com/'):
    #     return True
    if s.startswith('https://vimeo.com/'):
        return True


def isAudio(s):
    if s.startswith('https://clyp.it/'):
        return True


def downloadVideo(video_files, index_of_video, filename_path_video):
    print(f'downloadVideo    begin：{time.strftime("%Y-%m-%d %H:%M:%S")}')
    print('\nDownloading ' + str(len(video_files)) + ' videos.....')
    i = 0
    for video_file in video_files:
        print(video_file)
        r = requests.get(video_file, stream=True)
        with open(filename_path_video + '/' + index_of_video[i] + '.mp4', "wb") as mp4:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    mp4.write(chunk)
        i += 1
    print(f'downloadVideo    end：{time.strftime("%Y-%m-%d %H:%M:%S")}')


def getPhoto(urls_of_photo, filename_path):
    print('Downloading ' + str(len(urls_of_photo)) + ' urls of photo.....')
    with open(filename_path + '/urls_of_photo.txt', 'w', encoding='utf-8') as txt:
        for i in urls_of_photo:
            txt.write(i + '\n')


def getVideo(info, urls_of_video, filename_path):
    print('Downloading ' + str(len(urls_of_video)) + ' urls of video.....')
    with open(filename_path + '/urls_of_video.txt', 'w', encoding='utf-8') as txt:
        for i in urls_of_video:
            txt.write(i + '\n')
    print(f'getVideo    end：{time.strftime("%Y-%m-%d %H:%M:%S")}')


def getAudio(info, urls_of_audio, filename_path):
    print('Downloading ' + str(len(urls_of_audio)) + ' urls of audio.....')
    with open(filename_path + '/urls_of_audio.txt', 'w', encoding='utf-8') as txt:
        for i in urls_of_audio:
            txt.write(i + '\n')

    print(f'getAudio    end：{time.strftime("%Y-%m-%d %H:%M:%S")}')


info = input("Enter twitter user_name - ")
files = createFiles(info)
api = Auth()
all_tweets = getTweets(api, info)
db = pymysql.connect(host='localhost', port=3306, user='root', password='123456', db='download_info', charset='utf8')
cursor = db.cursor()

image_files = []
video_files = []
video_url = []
index_of_video = []
urls_of_video = set()
urls_of_audio = set()
url = ''
name = ''
tweet_sql = "insert into tweet_info(user_id, user_name, tweet_id, created_at, message, location) values (%s, %s, %s, %s, %s, %s);"
media_sql = "insert into media_info(date_info, user_id, user_name, tweet_id, media_type, media_url, media_name, media_store_path, is_stego, is_filter) values (%s, %s, %s, %s, %s, %s, %s, %s, 0, 0);"

try:
    for status in all_tweets:
        message = str(status.full_text.encode('utf-8'))
        message = re.split('\'', message)[1]

        try:
            entities = status.extended_entities
        except AttributeError:
            entities = status.entities
        if entities:
            media = entities.get('media', [])

            if len(media) != 0:
                cursor.execute(tweet_sql,
                               [status.user.id_str, status.user.screen_name, status.id_str, status.created_at,
                                message, status.user.location])
                db.commit()

                for i in range(len(media)):
                    media_type = media[i]['type']

                    if media_type == 'photo' or media_type == 'video':
                        if media_type == 'photo':
                            type_flag = 1
                            url = media[i]['media_url'] + ':large'
                            name = re.split('/', media[i]['media_url'])[4]
                            image_files.append(url)
                            path = files[1] + '\\'
                        elif media_type == 'video':
                            video_url = []
                            type_flag = 2
                            for v in media[i]['video_info']['variants']:
                                if v['content_type'] == 'video/mp4':
                                    video_url.append(v['url'])
                            url = video_url[0]
                            name = status.id_str + ".mp4"
                            video_files.append(url)
                            index_of_video.append(status.id_str)
                            path = files[1] + '\\'

                        cursor.execute(media_sql,
                                       [time.strftime("%Y-%m-%d %H:%M:%S"), status.user.id_str, status.user.screen_name,
                                        status.id_str, type_flag, url, name, path])
                        db.commit()
except tweepy.TweepError as e:
    print(e.reason)
    time.sleep(60)

try:
    for status in all_tweets:
        message = str(status.full_text.encode('utf-8'))
        message = re.split('\'', message)[1]

        try:
            for u in status.entities['urls']:
                if isVideo(u['expanded_url']):
                    type_flag = 2
                    cursor.execute(tweet_sql,
                                   [status.user.id_str, status.user.screen_name, status.id_str, status.created_at,
                                    message, status.user.location])
                    db.commit()
                    url = u['expanded_url']
                    if re.match('https://vimeo.com/', url):
                        name = re.split('/', url)[-1] + '.mp4'
                    # if re.match('https://youtu.be/', url):
                    #     name = re.split('/', url)[-1] + '.mp4'
                    # elif re.match('https://www.youtube.com/', url):
                    #     s = re.split('v=', url)
                    #     name = re.split('&', s[-1])[0] + '.mp4'
                    # elif re.match('https://vimeo.com/', url):
                    #     name = re.split('/', url)[-1] + '.mp4'
                    path = files[1] + '\\'
                    urls_of_video.add(u['expanded_url'])
                    cursor.execute(media_sql,
                                   [time.strftime("%Y-%m-%d %H:%M:%S"), status.user.id_str, status.user.screen_name,
                                    status.id_str, type_flag, url, name, path])
                    db.commit()

                if isAudio(u['expanded_url']):
                    type_flag = 3
                    cursor.execute(tweet_sql,
                                   [status.user.id_str, status.user.screen_name, status.id_str, status.created_at,
                                    status.full_text.encode('utf-8'), status.user.location])
                    db.commit()
                    url = u['expanded_url']
                    name = re.split('/', url)[3] + '.mp3'
                    path = files[1] + '\\'
                    urls_of_audio.add(u['expanded_url'])
                    cursor.execute(media_sql,
                                   [time.strftime("%Y-%m-%d %H:%M:%S"), status.user.id_str, status.user.screen_name,
                                    status.id_str, type_flag, url, name, path])
                    db.commit()
        except IndexError:
            urls_of_video.add('')
            urls_of_audio.add('')
except tweepy.TweepError as e:
    print(e.reason)
    time.sleep(60)

# Multiple-threading
if __name__ == '__main__':
    thread = []
    t1 = threading.Thread(target=getPhoto, args=(image_files, files[0]))
    # t2 = threading.Thread(target=downloadVideo, args=(video_files, index_of_video, files[0]))
    t3 = threading.Thread(target=getVideo, args=(info, urls_of_video, files[0]))
    t4 = threading.Thread(target=getAudio, args=(info, urls_of_audio, files[0]))
    thread.append(t1)
    # thread.append(t2)
    thread.append(t3)
    thread.append(t4)

    for t in thread:
        t.start()
    for t in thread:
        t.join()
    print(f'End：{time.strftime("%Y-%m-%d %H:%M:%S")}')
    os.system(
        'cd "C:/Users/alina/AppData/Local/Programs/Python/Python37/Scripts/Scripts" '
        '& activate & cd "' + files[1] + '" '
                                         '& youtube-dl -c -i --id --no-playlist -a urls_of_audio.txt'
                                         '& youtube-dl -c -i --id --no-playlist -a urls_of_video.txt'
                                         '& youtube-dl -c -i --id --no-playlist -a urls_of_photo.txt')
    try:
        images = os.listdir(files[1])
        for filename in images:
            portion = os.path.splitext(filename)
            if portion[1] == ".unknown_video":
                new_name = portion[0] + ".jpg"
                os.chdir(files[1])
                os.rename(filename, new_name)
    except KeyError:
        pass
