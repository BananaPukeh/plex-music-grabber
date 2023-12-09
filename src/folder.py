import os.path;
import re;

class Folder:
    def __init__(self, path):
        assert isinstance(path, str), "Path must be a string"
        assert os.path.isdir(path), "Path must be a directory"

        self.path = path

    def get_name(self):
        name = os.path.basename(self.path)
        # Strip off imdb/tmdb/tvdb id
        # https://support.plex.tv/articles/naming-and-organizing-your-movie-media-files/
        # https://support.plex.tv/articles/naming-and-organizing-your-tv-show-files/
        name = re.sub(r'\{(imdb|tmdb|tvdb)-(tt)?[0-9]*\}', '', name)
        
        return name;