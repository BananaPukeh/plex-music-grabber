import os
from pytube import YouTube
import urllib.request
import urllib.parse
import re
from pathlib import Path
import time
import shutil
import requests

libraryPath = os.getenv('library_path')
themeFileName = "theme.mp3"
themeIgnoreFile = ".themeignore"
folder = "downloads"
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
                grabMusic(name)

# Checks whether given series dir has a theme song


def checkThemeSong(path):
    contains = False
    for f in os.listdir(path):
        if f == themeFileName or f == themeIgnoreFile:
            contains = True
            break
    return contains


def grabMusic(name):
    
    query = urllib.parse.urlencode(
        {"search_query": name + " theme song -had-theme-songs"})

    searchUrl = "http://www.youtube.com/results?" + query + "&sp=EgIQAQ%253D%253D"
    content = urllib.request.urlopen(
        searchUrl)
    results = re.findall(
        r'\/watch\?v=(.{11})', content.read().decode())
    url = ("http://www.youtube.com/watch?v=" + results[0])

    print(url)
    notify("Theme music grabbed\n" + name)

    # Download it
    yt = YouTube(url)
    yt.register_on_complete_callback(downloadReady)

    hiStream = yt.streams.get_audio_only("mp4")

    # Start downloading
    hiStream.download(output_path=("{}".format(folder) + '/' + name),
                      filename="{}".format("theme"))
# Callbacks


def downloadReady(stream, path):
    print("Music downloaded for " + path)
    processMusic(path)


def processMusic(path):
    parentDir = Path(path).parents[0]
    name = parentDir.name

    try:
        # Move to library and rename mp3
        seriesPath = libraryPath + "/" + name + "/theme.mp3"
        shutil.move(path, seriesPath)
        shutil.rmtree(parentDir)
    except:
        print("Failed to Move " + path)


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
