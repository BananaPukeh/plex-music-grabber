import os
import urllib.request
import urllib.parse
import re
import yt_dlp

from folder import Folder
from notify import Notify

class MediaFolder(Folder):

    def update_theme_song(self, force = False):
        if (not self.has_theme_song() or force) and not self.is_ignored():
            return self.__grab_theme_song()
        else:
           return False

    def has_theme_song(self): 
        return os.path.isfile(os.path.join(self.path, "theme.mp3"))

    def is_ignored(self):
        return os.path.isfile(os.path.join(self.path, ".themeignore"))

    def __grab_theme_song(self):

        try:
            self.__clean_unfinished_downloads()
            url = self.__search_theme_song()
            self.__download_theme_song(url)
            Notify.notify("Downloaded theme song for '%s'\n\n'%s'" % (self.get_name(), url))
            return True
        except Exception as e:
            Notify.notify("Failed to download theme song for '%s'\n\n'%s'" % (self.get_name(), e))
            return False

    def __search_theme_song(self):
        query = urllib.parse.urlencode(
            {"search_query": self.get_name() + " OST"}
        )

        # TODO: Search using yt_dlp library
        searchUrl = "http://www.youtube.com/results?" + query + "&sp=EgQQARgB"
        content = urllib.request.urlopen(
            searchUrl)
        results = re.findall(
            r'\/watch\?v=(.{11})', content.read().decode())
        url = ("http://www.youtube.com/watch?v=" + results[0])

        return url

    def __download_theme_song(self, url):
        print("Downloading theme song from", url)
        options = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'outtmpl': self.path + '/theme.%(ext)s',
            'noprogress': True,
        }

        with yt_dlp.YoutubeDL(options) as ydl:
            error_code = ydl.download([url])


    def __clean_unfinished_downloads(self):
        for f in os.listdir(self.path):
            if f.startswith("theme."):
                path = os.path.join(self.path, f)
                print("Removing unfinished download: ", path)
                os.remove(path)

