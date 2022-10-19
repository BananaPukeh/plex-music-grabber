import os
from plex_music_grabber import PlexMusicGrabber

library_path_env_key = 'library_path'
library_paths = os.getenv(library_path_env_key)
interval = int(os.getenv('interval', "3600"))

if library_paths:
    paths = library_paths.split(",")
else:
    raise Exception("No library paths. Please set the environment variable %s. Multiple libraries comma seperated." % library_path_env_key)

if len(paths) == 0:
    raise Exception("No library paths. Please set the environment variable %s. Multiple libraries comma seperated." % library_path_env_key)

PlexMusicGrabber(paths, interval).run()
