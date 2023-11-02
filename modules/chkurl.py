import json
from urllib.parse import urlparse

l=json.loads(open("whitelist.json").read())["url"]

# URLのチェック
def chkurl(url):
    try:
        url = ('.'.join(urlparse(url).netloc.split('.')[-2:]))
        if url in l:
            return True
        else:
            return False
    except Exception as e:
        print("chkurlでエラーが発生しました。")
        return False