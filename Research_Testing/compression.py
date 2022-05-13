import os.path

class compressor(object):
    def __init__(self, row_length=16, col_height=64) -> None:
        self.row_length = row_length
        self.col_height = col_height
        self.chunk_size = self.col_height * self.row_length

    def compress(self, filepath):
        if not os.path.exists(filepath):
            raise(FileNotFoundError())

        with open(filepath, 'r') as f:
            data = f.read(self.chunk_size)

        # with open(filepath, 'rb') as f:
        #     data = f.read(self.chunck_size)
        # self.create_grid(filepath)
        newFilepath = filepath.replace("txt", "lor")
        with open(newFilepath, 'a') as f:
            f.write("")