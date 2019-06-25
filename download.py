import os
import requests


def do_load_media(url, path):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.3.2.1000 Chrome/30.0.1599.101 Safari/537.36"}
        pre_content_length = 0
        while True:
            if os.path.exists(path):
                headers['Range'] = 'bytes=%d-' % os.path.getsize(path)
            res = requests.get(url, stream=True, headers=headers)

            content_length = int(res.headers['content-length'])
            if content_length < pre_content_length or (
                    os.path.exists(path) and os.path.getsize(path) == content_length):
                break
            pre_content_length = content_length

            with open(path, 'ab') as file:
                file.write(res.content)
                file.flush()
                print('receive data，file size : %d  total size:%d' % (os.path.getsize(path), content_length))
    except Exception as e:
        print(e)


def load_media():
    url = "https://cf-media.sndcdn.com/bA1dsXOxA0j5.128.mp3?Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiKjovL2NmLW1lZGlhLnNuZGNkbi5jb20vYkExZHNYT3hBMGo1LjEyOC5tcDMiLCJDb25kaXRpb24iOnsiRGF0ZUxlc3NUaGFuIjp7IkFXUzpFcG9jaFRpbWUiOjE1NjE0NTYzNTR9fX1dfQ__&Signature=RBzbQppVuOndaNdUvCm5mDgj7WtInMIVHyANURaIiMMxxfAe~BuZnGe2wmqdqEt~sSgOsqnhHD7wQNT2oUQv60B8Znb9YnZ8-0knutkGH2~e4Z2BbGdeKz1fDdLMvDRH5Qq7z7cOo39cjNXVppjEM-sQy8Ip-E6sjuXP10ssTnCpIcydNY1OdJFLY6pxlhTKjmML2hKaJxpyFnXchVYV71lg8us-QTySswmT4qS4nM~NSDj~rJZWRUm9nh9RVTyok~DIhC4maAij9i9zCMmTuQeFJGS6Yyd5eWE5CsPRfs2FBEolE0V7fH01r~MqMAr0hHw7anh-16LqCArEzWyCgA__&Key-Pair-Id=APKAI6TU7MMXM5DG6EPQ"
    path = 'D:\p\crawler\code.mp3'
    do_load_media(url, path)
    pass


def main():
    load_media()
    pass
