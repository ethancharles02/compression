import os.path
from bit_grid import bit_grid

class compressor(object):
    def __init__(self, row_length:int=16, col_height:int=64):
        self.row_length = row_length
        self.col_height = col_height
        self.chunk_size = self.col_height * self.row_length

    def compress(self):
        grid = bit_grid(self.chunk_sizechunk_data, self.row_length, self.col_height)
        compressed_chunk = grid.compress()
        self.compressed_chunk = compressed_chunk

    def write_chunk(self, f):
        # TODO  add delimiters and other necessary info for 
        #       
        f.write(self.compressed_chunk)
    
    def run(self, filepath:str):
        if not os.path.exists(filepath):
            raise(FileNotFoundError())
            
        newFilepath = filepath.replace("txt", "lor")

        if os.path.exists(filepath):
            raise(FileNotFoundError())
            # with open(filepath, 'rb') as f:  # for reading actual bits

        with open(filepath, 'r') as f:
            self.chunk_data = f.read(self.chunk_size)
        self.compress()

        with open(newFilepath, 'a') as new_f:
            self.write_chunk(new_f)
            

if __name__ == "__main__":
    file_compressor = compressor()
    file_compressor.run("Research_Testing/random_string_files/random_bit_strings_1.txt")