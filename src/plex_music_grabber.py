import time
from media_library import MediaLibrary
from notify import Notify

class PlexMusicGrabber:
    def __init__(self, library_paths, interval):
        assert isinstance(library_paths, list), "Library paths must be a list"
        assert isinstance(interval, int), "Interval must be an integer"
        assert interval > 0, "Interval must be greater than 0"

        self.library_paths = library_paths
        self.interval = interval

    def run(self):
        print("=== Plex Music Grabber ===")
        print("Start running with an interval of %d" % self.interval)

        try:
            while True:
                self.__scan()
                time.sleep(self.interval)
        except KeyboardInterrupt:
            print("Stopping Plex Music Grabber")

    def __scan(self):
        libraries = []
        for path in self.library_paths:
            library = MediaLibrary(path)
            libraries.append(library)

        Notify.notify("Start updating theme songs for %d libraries" % len(libraries))    

        results = []
        for library in libraries:
            results.append(library.update_theme_songs())

        msg = "Finished updating theme songs\n"
        for result in results:
            msg += "`%s` new: %d total: %d \n" % (result[0], result[2], result[1])
        
        Notify.notify(msg)

