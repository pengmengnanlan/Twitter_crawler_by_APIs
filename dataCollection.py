import tweepy
import csv
import json
import time
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


def getTweets(api):
    hashtag = 'SoundCloud'
    user = input("Enter twitter user_name - ")
    urls_of_audio = []

    with open('./tweets_with_hashtag_' + hashtag + '.csv', 'a', encoding='utf-8') as the_file:
        writer = csv.writer(the_file)
        writer.writerow(['userId', "userName", 'created_at', 'message', 'urls_for_soundcloud'])

        try:
            for tweet in tweepy.Cursor(api.user_timeline, screen_name=user).items():
                hashtags = []
                for h in tweet.entities['hashtags']:
                    hashtags.append(h['text'])
                    # print(hashtags)
                if 'SoundCloud' in hashtags:
                    expanded_urls = []
                    try:
                        for u in tweet.entities['urls']:
                            expanded_urls.append(u['expanded_url'])
                            urls_of_audio.append(u['expanded_url'])
                    except IndexError:
                        expanded_urls.append('')
                        urls_of_audio.append('')
                    writer.writerow(
                        [tweet.user.id, tweet.user.screen_name, tweet.created_at, tweet.text.encode('utf-8'),
                         expanded_urls])
        except tweepy.TweepError as e:
            print(e.reason)
            time.sleep(60)
        print(urls_of_audio)

api = Auth()
getTweets(api)
