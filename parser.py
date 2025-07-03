import requests
from bs4 import BeautifulSoup
import json
import socket
import random
import asyncio

SITES = [
    "https://v2rayssr.com",
    "https://freevpn.us/v2ray",
    "https://getvmess.net",
    "https://v2raytech.com",
    "https://v2raylist.net",
    "https://freekeyv2ray.xyz",
    "https://v2ray.cool/freev2",
    "https://free-ss.site/vmess",
    "https://proxystore.xyz/free-v2ray",
    "https://v2rayshare.com",
    "https://vpnjantit.com/free-v2ray",
]

STORAGE_FILE = "storage.json"


def fetch_links():
    links = set()
    for url in SITES:
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")
            for code in soup.find_all("code"):
                text = code.get_text(strip=True)
                if text.startswith(("vmess://", "vless://", "trojan://", "ss://")):
                    links.add(text)
        except Exception as e:
            print(f"[!] Ошибка при парсинге {url}: {e}")
    return list(links)


async def test_key(key: str) -> bool:
    try:
        if "@" in key:
            host = key.split("@")[1].split(":")[0]
        else:
            host = key.split("//")[1].split("@")[-1].split(":")[0]
        socket.gethostbyname(host)
        return True
    except:
        return False


async def save_valid_keys():
    raw_links = fetch_links()
    valid = []

    for link in raw_links:
        if await test_key(link):
            print(f"[+] OK: {link}")
            valid.append(link)
        else:
            print(f"[-] DEAD: {link}")

    with open(STORAGE_FILE, "w") as f:
        json.dump(valid, f, indent=2)


def get_random_key():
    try:
        with open(STORAGE_FILE, "r") as f:
            links = json.load(f)
            return random.choice(links) if links else None
    except:
        return None