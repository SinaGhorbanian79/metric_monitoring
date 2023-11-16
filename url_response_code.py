import requests
import threading
import json

def get_urls():
    response = requests.get(
        "example.com"
    )
    data = response.json()
    urls = []
    for obj in data["data"]["result"]:
        if "urls" in obj:
            urls.append(obj["urls"])
    return urls


def update_urls():
    urls = get_urls()
    results = []
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "Accept-Language": "en-US",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Referer": "http://www.google.com",
    }
    threads = []
    for url in urls:
        https_url = url.replace("http://", "https://")
        thread = threading.Thread(
            target=lambda: results.append(get_status_code(https_url, headers))
        )
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    return json.dumps(results)


def get_status_code(url, headers):
    try:
        response = requests.get(
            url, headers=headers, allow_redirects=True, verify=False, timeout=30
        )
        if response.status_code != 200 :
            url = url.replace("https", "http")
            response = requests.get(
                url, headers=headers, allow_redirects=True, verify=False, timeout=30
            )
        return {"url": url, "status_code": response.status_code}
    except:
        try:
            url = url.replace("https", "http")
            response = requests.get(
                url, headers=headers, allow_redirects=True, verify=False, timeout=30
            )
            return {"url": url, "status_code": response.status_code}
        except:
            return {"url": url, "status_code": 0}


result = update_urls()
print(result)
