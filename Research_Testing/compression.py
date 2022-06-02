# import os.path
from os import path, listdir
# from bit_grid import bit_grid

COMPRESSION_FOLDER = "random_textstring_files"

class compressor(object):
    def __init__(self, chunk_size=1000):
        self.chunk_size = chunk_size
    # def __init__(self, row_length:int=16, col_height:int=64):
        # self.row_length = row_length
        # self.col_height = col_height
        # self.chunk_size = self.col_height * self.row_length

    def compress(self):
        # grid = bit_grid(self.chunk_sizechunk_data, self.row_length, self.col_height)
        # compressed_chunk = grid.compress()
        # self.compressed_chunk = compressed_chunk
        pass

    def write_chunk(self, f):
        # TODO  add delimiters and other necessary info for 
        # f.write(self.compressed_chunk)
        pass
    
    def run(self, filepath:str):
        if not path.exists(filepath):
            raise(FileNotFoundError())
            
        newFilepath = filepath.replace("txt", "lor")

        # if path.exists(filepath):
        #     raise(FileNotFoundError())
            # with open(filepath, 'rb') as f:  # for reading actual bits

        with open(filepath, 'r') as f:
            self.chunk_data = f.read(self.chunk_size)
            while self.chunk_data:
                while self.chunk_data[-1] != " ":
                    new_character = f.read(1)
                    if new_character:
                        self.chunk_data = self.chunk_data + new_character
                    else:
                        break

                self.chunk_data = f.read(self.chunk_size)

        # self.compress()

        # with open(newFilepath, 'a') as new_f:
        #     self.write_chunk(new_f)
    
    # def _

if __name__ == "__main__":
    file_compressor = compressor(20)
    
    # for file in listdir(COMPRESSION_FOLDER):
    #     if file.endswith(".txt"):
    #         file_compressor.run(f"{COMPRESSION_FOLDER}/{file}")
    # file_compressor.run(f"{COMPRESSION_FOLDER}/textstring_5words_10lines.txt")
    file_compressor.run(f"{COMPRESSION_FOLDER}/empty.txt")