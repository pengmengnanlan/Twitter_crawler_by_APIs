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
    if s.startswith('https://youtu.be/') or s.startswith('https://www.youtube.com/'):
        return True


def isAudio(s):
    if s.startswith('https://clyp.it/'):
        return True


def getTweets(api, hashtag, filename, filename_path1, filename_path2):
    urls_of_audio = set()
    urls_of_video = set()

    with open(filename + '/tweets_of_' + hashtag + '.csv', 'a', encoding='utf-8') as the_file:
        writer = csv.writer(the_file)
        writer.writerow(['userId', "userName", 'created_at', 'message', 'urls_for_media'])

        if hashtag == 'youtube' or hashtag == 'YouTube':
            try:
                for tweet in tweepy.Cursor(api.search, q='#' + hashtag, rpp=100).items(100):
                    expanded_urls = []
                    try:
                        for u in tweet.entities['urls']:
                            if isVideo(u['expanded_url']):
                                expanded_urls.append(u['expanded_url'])
                                urls_of_video.add(u['expanded_url'])
                                writer.writerow(
                                    [tweet.user.id, tweet.user.screen_name, tweet.created_at,
                                     tweet.text.encode('utf-8'), expanded_urls])
                    except IndexError:
                        urls_of_video.add('')
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(60)

            with open(filename_path2 + '/urls_of_video_of_' + hashtag + '.txt', 'w', encoding='utf-8') as txt:
                for i in urls_of_video:
                    txt.write(i + '\n')

        if hashtag == 'clyp.it' or hashtag == 'Clyp.It':
            try:
                for tweet in tweepy.Cursor(api.search, q='#' + hashtag, rpp=100).items(100):
                    expanded_urls = []
                    try:
                        for u in tweet.entities['urls']:
                            if isAudio(u['expanded_url']):
                                expanded_urls.append(u['expanded_url'])
                                urls_of_audio.add(u['expanded_url'])
                                writer.writerow(
                                    [tweet.user.id, tweet.user.screen_name, tweet.created_at,
                                     tweet.text.encode('utf-8'), expanded_urls])
                    except IndexError:
                        urls_of_audio.add('')
            except tweepy.TweepError as e:
                print(e.reason)
                time.sleep(60)

            with open(filename_path1 + '/urls_of_audio_of_' + hashtag + '.txt', 'w', encoding='utf-8') as txt:
                for i in urls_of_audio:
                    txt.write(i + '\n')


hashtag = input("Enter a hashtag - ")
files = createFiles(hashtag)
api = Auth()
getTweets(api, hashtag, files[0], files[1], files[2])
