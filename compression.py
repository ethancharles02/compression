

class compressor(object):
    def __init__(self):
        pass

    def compress(self, filepath):
        newFilepath = filepath.replace("txt", "lor")
        with open(newFilepath, 'w') as f:
            f.write("")