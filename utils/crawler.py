import requests

def get_redgifs_token():
    try:
        res = requests.get("https://api.redgifs.com/v2/auth/temporary", timeout=10)
        res.raise_for_status()
        token = res.json().get('access_token')
        if token:
            return token
        else:
            print("[Redgifs Auth] No access_token in response.")
    except requests.RequestException as e:
        print(f"[Redgifs Auth] HTTP error: {e}")
    except Exception as e:
        print(f"[Redgifs Auth] Unexpected error: {e}")
    return None

def crawl(limit=30):
    token = get_redgifs_token()
    if not token:
        return []

    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(
            f"https://api.redgifs.com/v2/gifs/trending?count={limit}",
            headers=headers,
            timeout=10
        )
        res.raise_for_status()

        data = res.json()
        gifs = data.get('gifs', [])
        results = []

        for gif in gifs:
            urls = gif.get('urls', {})
            thumb = urls.get('poster')
            video = urls.get('hd')
            title = gif.get('title', 'Redgifs Clip').strip()

            if thumb and video:
                results.append({
                    "thumb": thumb,
                    "video": video,
                    "title": title
                })

        return results

    except requests.RequestException as e:
        print(f"[Redgifs Crawler] HTTP error: {e}")
    except Exception as e:
        print(f"[Redgifs Crawler] Unexpected error: {e}")
    return []
