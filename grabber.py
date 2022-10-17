import os
import urllib.request
import urllib.parse
import re
import time
import requests
import yt_dlp


libraryPath = os.getenv('library_path')
themeFileName = "theme.mp3"
themeIgnoreFile = ".themeignore"
interval = int(os.getenv('interval', "3600"))


def scanLibrary():
    if not libraryPath:
        raise Exception("No library path")

    # Go through all series folders
    for name in os.listdir(libraryPath):
        seriesPath = os.path.join(libraryPath, name)

        if os.path.isdir(seriesPath):
            if not checkThemeSong(seriesPath):
                print("%s doesn't have a theme song" % name)
                grabMusic(name, seriesPath)

# Checks whether given series dir has a theme song


def checkThemeSong(path):
    contains = False
    for f in os.listdir(path):
        if f == themeFileName or f == themeIgnoreFile:
            contains = True
            break
    return contains


def grabMusic(name, seriesPath):
    query = urllib.parse.urlencode(
        {"search_query": name + " theme song -had-theme-songs"})

    # TODO: Search using yt_dlp library
    searchUrl = "http://www.youtube.com/results?" + query + "&sp=EgIQAQ%253D%253D"
    content = urllib.request.urlopen(
        searchUrl)
    results = re.findall(
        r'\/watch\?v=(.{11})', content.read().decode())
    url = ("http://www.youtube.com/watch?v=" + results[0])

    print(url)
    notify("Theme music grabbed\n" + name)

    download(url, seriesPath)


def download(url, seriesPath):
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'outtmpl': seriesPath + '/theme.%(ext)s',
        'overwrites' : True,
    }

    with yt_dlp.YoutubeDL(options) as ydl:
        error_code = ydl.download([url])

# Callbacks


def notify(message):
    bot_token = os.getenv("telegram_token", "")
    bot_chatID = os.getenv("telegram_chat_id", "")

    if not bot_token == "" and not bot_chatID == "":
        send_text = 'https://api.telegram.org/bot' + bot_token + \
            '/sendMessage?disable_notification=true&chat_id=' + \
            bot_chatID + '&parse_mode=Markdown&text=' + message

        _ = requests.get(send_text)


#  Start
print("Start monitoring for missing theme songs")
print("Interval %d seconds" % interval)

while True:
    scanLibrary()
    time.sleep(interval)
