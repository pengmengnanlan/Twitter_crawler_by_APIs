import tweepy
import csv
import json
import time
import os
import shutil
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


def createFiles(user):
    now_path = os.getcwd()
    filename = u'' + user + ''
    audio_filename = u'Audio'
    video_filename = u'Video'
    f = now_path + "\\" + filename
    filename_path1 = now_path + "\\" + filename + "\\" + audio_filename
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


def isVideo(s):
    # if s.startswith('https://youtu.be/') or s.startswith('https://www.youtube.com/'):
    #     return True
    if s.startswith('https://vimeo.com/'):
        return True


def isAudio(s):
    if s.startswith('https://clyp.it/'):
        return True


def isPhoto(s):
    if s.startswith('https://flic.kr/p/'):
        return True


def getTweets(api, user, filename, filename_path1, filename_path2):
    urls_of_video = set()
    urls_of_audio = set()
    urls_of_photo = set()

    with open(filename + '/tweets_of_' + user + '.csv', 'a', encoding='utf-8') as the_file:
        writer = csv.writer(the_file)
        writer.writerow(['userId', "userName", 'tweet_id', 'created_at', 'message', 'media_url', 'media_type'])

        try:
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=user).items():
                expanded_urls = []
                try:
                    for u in tweet.entities['urls']:
                        if isVideo(u['expanded_url']) or isAudio(u['expanded_url']) or isPhoto(u['expanded_url']):
                            expanded_urls.append(u['expanded_url'])
                            if isVideo(u['expanded_url']):
                                writer.writerow(
                                    [tweet.user.id, tweet.user.screen_name, tweet.id_str, tweet.created_at,
                                     tweet.text.encode('utf-8'),
                                     expanded_urls, 'video'])
                                urls_of_video.add(u['expanded_url'])
                            elif isAudio(u['expanded_url']):
                                writer.writerow(
                                    [tweet.user.id, tweet.user.screen_name, tweet.id_str, tweet.created_at,
                                     tweet.text.encode('utf-8'),
                                     expanded_urls, 'audio'])
                                urls_of_audio.add(u['expanded_url'])
                            elif isPhoto(u['expanded_url']):
                                writer.writerow(
                                    [tweet.user.id, tweet.user.screen_name, tweet.id_str, tweet.created_at,
                                     tweet.text.encode('utf-8'),
                                     expanded_urls, 'flickr'])
                                urls_of_photo.add(u['expanded_url'])

                except IndexError:
                    urls_of_video.add('')
                    urls_of_audio.add('')
                    urls_of_photo.add('')

        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(60)

    with open(filename_path2 + '/urls_of_video_of_' + user + '.txt', 'w', encoding='utf-8') as txt:
        for i in urls_of_video:
            txt.write(i + '\n')

    with open(filename_path1 + '/urls_of_audio_of_' + user + '.txt', 'w', encoding='utf-8') as txt:
        for i in urls_of_audio:
            txt.write(i + '\n')

    with open(filename_path1 + '/urls_of_photo_of_' + user + '.txt', 'w', encoding='utf-8') as txt:
        for i in urls_of_photo:
            txt.write(i + '\n')


def printTweets(api, user):
    l = []
    for tweet in tweepy.Cursor(api.user_timeline, screen_name=user).items():
        try:
            for u in tweet.entities['urls']:
                l.append(u['expanded_url'])
        except IndexError:
            l.append('no urls')
    print(l)


user = input("Enter twitter user_name - ")
files = createFiles(user)
api = Auth()
getTweets(api, user, files[0], files[1], files[2])
printTweets(api, user)
