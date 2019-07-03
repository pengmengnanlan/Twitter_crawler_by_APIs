import tweepy
import json
import wget
import csv
import time
import threading
import os
import requests
import shutil
from PIL import Image
from io import BytesIO
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


def getTweets(api, user):
    # the maximum number of twitters is 200 per time
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
        count += 1
    return all_tweets


def createFiles(user):
    now_path = os.getcwd()
    filename = u'' + user + ''
    image_filename = u'Image'
    video_filename = u'Original_Video'
    youtube_video_filename = u'Youtube_Video'
    audio_filename = u'Audio'
    f = now_path + "\\" + filename
    filename_path_photo = now_path + "\\" + filename + "\\" + image_filename
    filename_path_original_video = now_path + "\\" + filename + "\\" + video_filename
    filename_path_youtube_video = now_path + "\\" + filename + "\\" + youtube_video_filename
    filename_path_audio = now_path + "\\" + filename + "\\" + audio_filename
    if os.path.exists(f):
        shutil.rmtree(f)
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
    os.makedirs(filename_path_audio)
    return [filename, filename_path_photo, filename_path_original_video, filename_path_youtube_video,
            filename_path_audio]


def isVideo(s):
    if s.startswith('https://youtu.be/') or s.startswith('https://www.youtube.com/'):
        return True


def isAudio(s):
    if s.startswith('https://clyp.it/'):
        return True


def getPhoto(user, all_tweets, filename):
    image_files = []
    with open(filename + '/photos_of_user_' + user + '.csv', 'a', encoding='utf-8') as file_photo:
        writer = csv.writer(file_photo)
        writer.writerow(
            ['userId', 'userName', 'tweet_id', 'created_at', 'message', 'media_id', 'media_url', 'media_type',
             'media_size'])

        try:
            for status in all_tweets:
                media_id = []
                media_url = []
                info = []
                try:
                    entities = status.extended_entities
                except AttributeError:
                    entities = status.entities
                if entities:
                    media = entities.get('media', [])

                    if len(media) != 0:
                        for i in range(len(media)):
                            media_id.append(media[i]['id_str'])
                            media_type = media[i]['type']

                            if media_type == 'photo':
                                media_url.append(media[i]['media_url'])
                                image_files.append(media[i]['media_url'])
                                response = requests.get(media[i]['media_url'])
                                tmpIm = BytesIO(response.content)
                                im = Image.open(tmpIm)
                                info.append({'photo_size': {'w': im.size[0], 'h': im.size[1]}})

                                writer.writerow(
                                    [status.user.id, status.user.screen_name, status.id_str, status.created_at,
                                     status.text.encode('utf-8'), media_id, media_url, media_type, info])

        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(60)
        return image_files


def getVideo(user, all_tweets, filename):
    video_files = []
    index_of_video = []
    with open(filename + '/original_video_of_user_' + user + '.csv', 'a', encoding='utf-8') as file_video:
        writer = csv.writer(file_video)
        writer.writerow(
            ['userId', 'userName', 'tweet_id', 'created_at', 'message', 'media_url', 'media_type'])

        try:
            for status in all_tweets:
                media_url = []
                try:
                    entities = status.extended_entities
                except AttributeError:
                    entities = status.entities
                if entities:
                    media = entities.get('media', [])

                    if len(media) != 0:
                        for i in range(len(media)):
                            media_type = media[i]['type']
                            if media_type == 'video':
                                for v in media[i]['video_info']['variants']:
                                    if v['content_type'] == 'video/mp4':
                                        media_url.append(v['url'])
                                video_files.append(media_url[0])
                                index_of_video.append(status.id_str)

                                writer.writerow(
                                    [status.user.id, status.user.screen_name, status.id_str, status.created_at,
                                     status.text.encode('utf-8'), media_url, media_type])

        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(60)
    return [video_files, index_of_video]


def getVideoFromYouTube(user, all_tweets, filename, filename_path):
    print(f'getVideoFromYouTube    begin：{time.strftime("%Y-%m-%d %H:%M:%S")}')
    time.sleep(5)
    urls_of_video = set()
    with open(filename + '/Youtube_video_of_' + user + '.csv', 'a', encoding='utf-8') as the_file:
        writer = csv.writer(the_file)
        writer.writerow(['userId', "userName", 'tweet_id', 'created_at', 'message', 'media_url', 'media_type'])

        try:
            for tweet in all_tweets:
                expanded_urls = []
                try:
                    for u in tweet.entities['urls']:
                        if isVideo(u['expanded_url']):
                            expanded_urls.append(u['expanded_url'])
                            writer.writerow(
                                [tweet.user.id, tweet.user.screen_name, tweet.id_str, tweet.created_at,
                                 tweet.text.encode('utf-8'), expanded_urls, 'video'])
                            urls_of_video.add(u['expanded_url'])
                except IndexError:
                    urls_of_video.add('')
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(60)

    print('Downloading ' + str(len(urls_of_video)) + ' urls of video.....')
    with open(filename_path + '/urls_of_Youtube_video_of_' + user + '.txt', 'w', encoding='utf-8') as txt:
        for i in urls_of_video:
            txt.write(i + '\n')

    print(f'getVideoFromYouTube    end：{time.strftime("%Y-%m-%d %H:%M:%S")}')


def getAudio(user, all_tweets, filename, filename_path):
    print(f'getAudio    begin：{time.strftime("%Y-%m-%d %H:%M:%S")}')
    time.sleep(5)
    urls_of_audio = set()

    with open(filename + '/audio_of_' + user + '.csv', 'a', encoding='utf-8') as the_file:
        writer = csv.writer(the_file)
        writer.writerow(['userId', "userName", 'tweet_id', 'created_at', 'message', 'media_url', 'media_type'])

        try:
            for tweet in all_tweets:
                expanded_urls = []
                try:
                    for u in tweet.entities['urls']:
                        if isAudio(u['expanded_url']):
                            expanded_urls.append(u['expanded_url'])
                            writer.writerow(
                                [tweet.user.id, tweet.user.screen_name, tweet.id_str, tweet.created_at,
                                 tweet.text.encode('utf-8'),
                                 expanded_urls, 'audio'])
                            urls_of_audio.add(u['expanded_url'])
                except IndexError:
                    urls_of_audio.add('')
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(60)

    print('Downloading ' + str(len(urls_of_audio)) + ' urls of audio.....')
    with open(filename_path + '/urls_of_audio_of_' + user + '.txt', 'w', encoding='utf-8') as txt:
        for i in urls_of_audio:
            txt.write(i + '\n')

    print(f'getAudio    end：{time.strftime("%Y-%m-%d %H:%M:%S")}')


def downloadPhoto(image_files, filename_path_photo):
    print(f'downloadPhoto    begin：{time.strftime("%Y-%m-%d %H:%M:%S")}')
    time.sleep(5)
    print('Downloading ' + str(len(image_files)) + ' images.....')
    for image_file in image_files:
        print(image_file)
        wget.download(image_file, filename_path_photo)

    print(f'downloadPhoto    end：{time.strftime("%Y-%m-%d %H:%M:%S")}')


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


user = input("Enter twitter user_name - ")
files = createFiles(user)
api = Auth()
all_tweets = getTweets(api, user)
photo = getPhoto(user, all_tweets, files[0])
original_video = getVideo(user, all_tweets, files[0])


# Multiple-threading
if __name__ == '__main__':
    thread = []
    t1 = threading.Thread(target=downloadPhoto, args=(photo, files[1]))
    t2 = threading.Thread(target=downloadVideo, args=(original_video[0], original_video[1], files[2]))
    t3 = threading.Thread(target=getVideoFromYouTube, args=(user, all_tweets, files[0], files[3]))
    t4 = threading.Thread(target=getAudio, args=(user, all_tweets, files[0], files[4]))
    thread.append(t1)
    thread.append(t2)
    thread.append(t3)
    thread.append(t4)

    for t in thread:
        t.start()
    for t in thread:
        t.join()
    print(f'End：{time.strftime("%Y-%m-%d %H:%M:%S")}')

'''downloadPhoto(photo, files[1])
downloadVideo(original_video[0], original_video[1], files[2])
getVideoFromYouTube(user, all_tweets, files[0], files[3])
getAudio(user, all_tweets, files[0], files[4])'''