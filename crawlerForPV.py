import tweepy
import json
import wget
import csv
import time
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
    # get 200 tweets of one user, response in json
    all_tweets = api.user_timeline(screen_name=user, count=200, include_rts=False, exclude_replies=True)
    if all_tweets:
        last_tweet_id = all_tweets[-1].id
    else:
        last_tweet_id = 0

    # get all tweets
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
    video_filename = u'Video'
    f = now_path + "\\" + filename
    filename_path1 = now_path + "\\" + filename + "\\" + image_filename
    filename_path2 = now_path + "\\" + filename + "\\" + video_filename
    if os.path.exists(f):
        shutil.rmtree(f)
    if os.path.exists(filename_path1):
        shutil.rmtree(filename_path1)
    if os.path.exists(filename_path2):
        shutil.rmtree(filename_path2)
    os.makedirs(filename_path1)
    os.makedirs(filename_path2)
    return [filename, filename_path1, filename_path2]


def download(user, all_tweets, filename, filename_path1, filename_path2):
    image_files = []
    video_files = []
    index_of_video = []
    with open(filename + '/tweets_of_user_' + user + '.csv', 'a', encoding='utf-8') as the_file:
        writer = csv.writer(the_file)
        writer.writerow(
            ['userId', 'userName', 'tweet_id', 'created_at', 'message', 'media_id', 'media_url', 'media_type',
             'media_size'])

        try:
            for status in all_tweets:
                media_id = []
                media_url = []
                media_type = ''
                info = []
                try:
                    entities = status.extended_entities
                except AttributeError:
                    entities = status.entities
                if entities:
                    media = entities.get('media', [])

                    print(len(media))
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
                            elif media_type == 'video':
                                for v in media[i]['video_info']['variants']:
                                    if v['content_type'] == 'video/mp4':
                                        media_url.append(v['url'])
                                video_files.append(media_url[0])
                                index_of_video.append(status.id_str)
                                info.append({'duration_millis': media[i]['video_info']['duration_millis'],
                                             'additional_media_info': media[i]['additional_media_info']})

                        writer.writerow(
                            [status.user.id, status.user.screen_name, status.id_str, status.created_at,
                            status.text.encode('utf-8'),
                            media_id, media_url, media_type, info])

            print('Downloading ' + str(len(image_files)) + ' images.....')
            for image_file in image_files:
                print(image_file)
                wget.download(image_file, filename_path1)

            print('\nDownloading ' + str(len(video_files)) + ' videos.....')
            i = 0
            for video_file in video_files:
                print(video_file)
                r = requests.get(video_file, stream=True)
                with open(filename_path2 + '/' + index_of_video[i] + '.mp4', "wb") as mp4:
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if chunk:
                            mp4.write(chunk)
                i += 1

        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(60)


user = input("Enter twitter user_name - ")
files = createFiles(user)
api = Auth()
all_tweets = getTweets(api, user)
download(user, all_tweets, files[0], files[1], files[2])
