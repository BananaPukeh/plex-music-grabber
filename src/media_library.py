import os
from folder import Folder
from media_folder import MediaFolder

class MediaLibrary(Folder):
    def update_theme_songs(self, force = False):
        total = 0
        downloaded = 0

        for name in os.listdir(self.path):
            path = os.path.join(self.path, name)
            if os.path.isdir(path):
                media_folder = MediaFolder(path)
                total += 1
                if media_folder.update_theme_song(force): 
                    downloaded += 1
        return (self.get_name(), total, downloaded)
