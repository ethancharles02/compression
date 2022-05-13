import os.path

class compressor(object):
    def __init__(self, row_length=5, col_height=5) -> None:
        self.row_length = row_length
        self.col_height = col_height

    def compress(self, filepath):
        if not os.path.exists(filepath):
            raise(FileNotFoundError())
        # self.create_grid(filepath)
        newFilepath = filepath.replace("txt", "lor")
        with open(newFilepath, 'a') as f:
            f.write("")