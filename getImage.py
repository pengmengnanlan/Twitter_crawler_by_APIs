import tweepy
from tweepy import OAuthHandler
import json
import wget
import urllib.request

with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_token = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
# api = tweepy.API(auth)
api = tweepy.API(auth, proxy="127.0.0.1:1080", wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = input("Enter twitter user_id - ")
# get tweets of one user, response in json
all_tweets = api.user_timeline(screen_name=user, count=200, include_rts=False, exclude_replies=True)
last_tweet_id = all_tweets[-1].id

while True:
    # get more tweets posted earlier than max_id
    more_tweets = api.user_timeline(screen_name=user, count=200, include_rts=False, exclude_replies=True,
                                    max_id=last_tweet_id - 1)
    # break if there is no more older tweets; otherwise keep searching until all the tweets of this user can be found
    if len(more_tweets) == 0:
        break
    else:
        last_tweet_id = more_tweets[-1].id - 1
        all_tweets = all_tweets + more_tweets

image_files = set()
sizes = []
'''with open('./tweets_of_user' + user + '.csv', 'a', encoding='utf-8') as the_file:
    writer = csv.writer(the_file)
    writer.writerow(['userId', "userName", 'created_at', 'message', "location", "media_list"])'''
for status in all_tweets:
    media = status.entities.get('media', [])
    if len(media) != 0:
        image_files.add(media[0]['media_url'])
        sizes.append(media[0]['sizes'])

print('Downloading ' + str(len(image_files)) + ' images.....')
print(image_files)
'''x = 0
for i in image_files:
    print(i)
    urllib.request.urlretrieve(i, '%s.jpg' % x)
    x += 1'''
for image_file in image_files:
    wget.download(image_file)

'''x = 0
for i in image_files:
    print(i)
    try:
        resp = urllib.request.urlopen(i)
        respHtml = resp.read()
        picFile = open('%s.jpg' % x, 'wb')
        picFile.write(respHtml)
        picFile.close()
        x += 1
    except urllib.error.URLError as e:
        print(e.reason)'''
