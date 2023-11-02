import requests
import modules.env as env

# KuttのAPIを叩いて短縮URLを取得
def kutt(url):
    try:
        r = requests.post("https://" + env.KUTT_HOST + "/api/v2/links", data={"target": url}, headers={'X-API-KEY': env.KUTT_API_KEY}).json()
        return r['link'].replace(env.KUTT_HOST,env.KUTT_DOMAIN)
    except Exception as e:
        print("Kuttでの短縮URL取得に失敗しました。")
        return False