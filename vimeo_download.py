from urllib.error import HTTPError
from bs4 import BeautifulSoup
import requests
import json
import urllib.request
import threading
import os
import sys
import time


true = True
false = False
null = None

cookies = {
    }

PARAMS = {
    }

url = ""


def make_request():
    r = requests.get(url=url, params=PARAMS, cookies=cookies)
    print(r.content)

    f = open("out.html", "w")
    f.write(r.content.decode())
    f.close()


def process_response():
    with open('response.html', 'r') as file:
        response = BeautifulSoup(file, "html.parser")

    script_content = ""

    for tag in response.find_all("script"):
        if "window.playerConfig = {" in tag.get_text():
            script_content = tag.get_text().replace("  ", "")  # reduce indent
            break

    # trim playerConfig section
    config_start_pos = script_content.find("window.playerConfig = ") + 22
    config_end_pos = script_content.rindex("}") + 1

    playerConfig = json.loads(script_content[config_start_pos:config_end_pos])

    return playerConfig


def sizeof_fmt(num, suffix='B'):
    for unit in ["", "K", "M", "G"]:
        if abs(num) < 1024.0:
            return f"{num:3.5f} {unit}{suffix}"
        num /= 1024.0
    return f"{num:1f}Ti{suffix}"


def process_playerConfig(playerConfig):

    # Get highest resolution
    playerConfig_progressive = playerConfig['request']['files']['progressive']

    highest_res = (0, 0)
    for ndx, value in enumerate(playerConfig_progressive):
        if value['height'] > highest_res[1]:
            highest_res = (ndx, value['height'])

    url = playerConfig_progressive[highest_res[0]]['url']
    extension = playerConfig_progressive[highest_res[0]]['mime'].split('/')[1]

    # File size
    try:
        site = urllib.request.urlopen(url)
        headers = dict(site.headers.items())
        filesize = int(headers["Content-Length"])
        print("File size:", sizeof_fmt(filesize))
        download_selection = input("Download video file? (y/n): ")

        if download_selection.lower().strip() in ["y", "yes"]:
            download(url, f'video.{extension}', filesize)
    except HTTPError:
        type, value, traceback = sys.exc_info()
        print(value)


def download(url, filename, filesize):
    download_thread = threading.Thread(target=urllib.request.urlretrieve, args=[url, filename])
    download_thread.start()

    while not os.path.exists(f"./{filename}"):
        pass

    bytes_downloaded = 0

    print('\33[?25l', end='')   # hide cursor
    while bytes_downloaded < filesize:
        time.sleep(0.5)
        bytes_downloaded = os.path.getsize(f"./{filename}")
        print("\rDownloaded: ", bytes_downloaded, "       ", end='')
    print('\33[?25h', end='')   # reveal cursor

    # empty 'response.html'
    open('response.html', 'w').close()


if __name__ == "__main__":
    pc = process_response()
    process_playerConfig(pc)
