import requests
from bs4 import BeautifulSoup

# Hàm lấy Access Token miễn phí từ Redgifs API
def get_redgifs_token():
    try:
        res = requests.get("https://api.redgifs.com/v2/auth/temporary", timeout=10)
        if res.ok:
            token = res.json().get('access_token')
            return token
    except Exception as e:
        print(f"[Error] Get access token failed: {e}")
    return None
              
def crawl(limit=30):
    token = get_redgifs_token()
    if not token:
        return []
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(f"https://api.redgifs.com/v2/gifs/trending?count={limit}", headers=headers)
        res.raise_for_status()
        gifs = res.json().get('gifs', [])
        results = []
        for gif in gifs:
            results.append({
                "thumb": gif['urls'].get('poster'),
                "video": gif['urls'].get('hd'),
                "title": gif.get('title', 'Redgif Clip')
            })
        return results
    except Exception as e:
        print(f"[Error] Crawl redgifs failed: {e}")
        return []
