import urllib.request
import re
import json
from bs4 import BeautifulSoup

response = urllib.request.urlopen(
    'https://soundcloud.com/mengnanlan-peng/wav10s-00002?utm_source=soundcloud&utm_campaign=share&utm_medium=twitter')
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, features="html.parser")
tags = soup.find_all(name='meta', property="twitter:app:url:googleplay")
tag = re.findall('\d+', re.findall(r'"([^"]*)"', str(tags[0]))[0])
track_id = tag[0]
print(track_id)

client_id = 'NmW1FlPaiL94ueEu7oziOWjYEzZzQDcK'
url = urllib.request.urlopen(
    'https://api.soundcloud.com/i1/tracks/{}/streams?client_id={}'.format(track_id, client_id))
html1 = url.read().decode('utf-8')
j = json.loads(html1)
print(j['http_mp3_128_url'])