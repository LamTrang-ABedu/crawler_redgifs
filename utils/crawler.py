import requests
from bs4 import BeautifulSoup

# Hàm lấy Access Token miễn phí từ Redgifs API
def get_access_token():
    try:
        response = requests.post("https://api.redgifs.com/v2/oauth2/token", json={"grant_type": "client_credentials"})
        response.raise_for_status()
        return response.json()['access_token']
    except Exception as e:
        print(f"[Error] Get access token failed: {e}")
        return None
              
def crawl(limit=30):
    token = get_access_token()
    if not token:
        return []
    
    headers = {"Authorization": f"Bearer {token}"}
    try:
        res = requests.get(f"https://api.redgifs.com/v2/gifs/search?search=popular&count={limit}", headers=headers)
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
