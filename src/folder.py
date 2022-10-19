import os.path;

class Folder:
    def __init__(self, path):
        assert isinstance(path, str), "Path must be a string"
        assert os.path.isdir(path), "Path must be a directory"

        self.path = path

    def get_name(self):
        return os.path.basename(self.path)