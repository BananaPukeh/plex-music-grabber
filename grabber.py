import os
import pytube
from pytube import YouTube
import urllib.request
import urllib.parse
import re
import sys
from pathlib import Path
import time

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
    music_query_string = urllib.parse.urlencode(
        {"search_query": name + " theme song"})
    music_html_content = urllib.request.urlopen(
        "http://www.youtube.com/results?" + music_query_string + "&sp=EgIQAQ%253D%253D")
    music_search_results = re.findall(
        r'\/watch\?v=(.{11})', music_html_content.read().decode())
    music_url = ("http://www.youtube.com/watch?v=" + music_search_results[0])

    print(music_url)

    # Download it
    
    yt = YouTube(music_url)        
    yt.register_on_complete_callback(downloadReady)

    hiStream = yt.streams.get_audio_only("mp4")

    # Start downloading
    hiStream.download(output_path=("{}".format(folder)),
                      filename="{}".format(name))


# Callbacks

def downloadReady(stream, path):
    print("Music downloaded for " + path)
    processMusic(path)


def processMusic(path):
    name = Path(path).stem

    # Move to library and rename mp3
    seriesPath = libraryPath + "/" + name + "/theme.mp3"

    os.rename(path, seriesPath)

#  Start

print("Start monitoring for missing theme songs")
print("Interval %d seconds"%interval)

while True:
    scanLibrary()
    time.sleep(interval)
