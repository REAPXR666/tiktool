import time
import requests
import json
import os

# get from https://2captcha.com/
TWO_CAPTCHA_KEY = "Your-2cap-key"

#FORMAT: http://username:password@ip:port
PROXY = "your-proxy-here"


TURNSTILE_SITEKEY = "0x4AAAAAAB_0chVZyYLtMbNL"
TURNSTILE_PAGE_URL = "https://tiktool.pro"
API_ENDPOINT = "https://tiktool.pro/api/send-views"
PROXIES = {"http": PROXY, "https": PROXY}


def solve_turnstile(site_key, url):
    print("[+] Sending Turnstile challenge to 2Captcha...")

    create_task = requests.post("http://2captcha.com/in.php",
                                data={
                                    "key": TWO_CAPTCHA_KEY,
                                    "method": "turnstile",
                                    "sitekey": site_key,
                                    "pageurl": url,
                                    "json": 1
                                }).json()

    if create_task["status"] != 1:
        raise Exception("2Captcha failed to create captcha task:", create_task)

    request_id = create_task["request"]
    print("[+] Task ID:", request_id)

    while True:
        time.sleep(5)
        res = requests.get("http://2captcha.com/res.php",
                           params={
                               "key": TWO_CAPTCHA_KEY,
                               "action": "get",
                               "id": request_id,
                               "json": 1
                           }).json()

        if res["status"] == 1:
            print("[+] Captcha solved!")
            return res["request"]

        print("[...] Waiting for solution...")


def send_views(video_url, captcha_token):
    print("[+] Sending to API...")
    raw_json = json.dumps({
        "video_id": video_url,
        "captchaToken": captcha_token
    })
    payload = {"video_id": video_url, "captchaToken": captcha_token}

    response = requests.post(
        API_ENDPOINT,
        proxies=PROXIES,
        data=raw_json,
        headers={
            "Host":
            "tiktool.pro",
            "Accept":
            "*/*",
            "Accept-Encoding":
            "gzip, deflate, br, zstd",
            "Accept-Language":
            "en-GB,en-US;q=0.9,en;q=0.8,bs;q=0.7,fr;q=0.6",
            "Content-Type":
            "application/json",
            "Cookie":
            ("cf_clearance=aS67G6NOXZaB5OUQ3rZFDcrIh8Cv_X7NQDwMb8qPvfM-1763300126-1.2.1.1-"
             "XU4MidGh.E1qmj6HiOWV6jBN.fkHNecssm9zsiReAtYK5bdqMREl1lDQHXavAvoSu87nS_0oFZVI"
             "kXPfjGlUdbkwfeRS9GNVbFwbBIPrpvDhJEcCQy61zolHTv7TEkqjU0F9e574gRzWozeB9YmxTRO3y"
             "YK0D8u_Li6MHMyxPG5p9PKSgpTO_zjD3wpm8.APVgYXv436YYr3GR0utffp1ObM7azH0sGnTk880_"
             "ig_SqNa7QTEpACLYuQi07i2aY4"),
            "Origin":
            "https://tiktool.pro",
            "Priority":
            "u=1, i",
            "Referer":
            "https://tiktool.pro/",
            "Sec-CH-UA":
            '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
            "Sec-CH-UA-Arch":
            '"x86"',
            "Sec-CH-UA-Bitness":
            '"64"',
            "Sec-CH-UA-Full-Version":
            '"142.0.7444.163"',
            "Sec-CH-UA-Full-Version-List":
            '"Chromium";v="142.0.7444.163", '
            '"Google Chrome";v="142.0.7444.163", '
            '"Not_A Brand";v="99.0.0.0"',
            "Sec-CH-UA-Mobile":
            "?0",
            "Sec-CH-UA-Model":
            '""',
            "Sec-CH-UA-Platform":
            '"Windows"',
            "Sec-CH-UA-Platform-Version":
            '"19.0.0"',
            "Sec-Fetch-Dest":
            "empty",
            "Sec-Fetch-Mode":
            "cors",
            "Sec-Fetch-Site":
            "same-origin",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/142.0.0.0 Safari/537.36",
        })
    # FOR SUM REASON RESPONSE CAN CORRUPT ITSELF, IDFK
    print("[+] Response:", response.text)
    return response.text


if __name__ == "__main__":
    video = input("Your tiktok Video URL: ")

    token = solve_turnstile(TURNSTILE_SITEKEY, TURNSTILE_PAGE_URL)
    print(token)
    send_views(video, token)
