# TODO
# Add docstrings
from os import path, listdir
from text_compression import Text_Compressor

COMPRESSION_FOLDER = "random_textstring_files"

class compressor(object):
    def __init__(self, chunk_size=1000, look_ahead=5):
        self.chunk_size = chunk_size
        self.look_ahead = look_ahead
        self.chunk_data = None
        self.text_compressor = Text_Compressor(self.look_ahead)
        self.input_folder = None
        self.output_folder = None
        
    def run(self, in_file:str, out_file=None):
        in_file, out_file = self._check_and_update_io_files(in_file, out_file)

        with open(in_file, 'r') as f:
            # Get chunk data
            self.chunk_data = f.read(self.chunk_size)

            # Create initial compressed file
            with open(out_file, 'x'):
                pass
            
            # As long as there is more data to read:
            while self.chunk_data:
                # Append additional chunk data till it has a full word at the end
                self._update_chunk_data_to_end_of_word(f)

                # Compress the chunk 
                self.text_compressor.compress(self.chunk_data)
                # write the chunk to the output file
                with open(out_file, 'a') as new_f:
                    new_f.write(self.text_compressor.get_compressed_data())
                
                # Get new chunk data
                self.chunk_data = f.read(self.chunk_size)

    def _update_chunk_data_to_end_of_word(self, f):
        # Keeps reading in chunk data till the last character is a space
        while self.chunk_data[-1] != " ":
            new_character = f.read(1)
            # Updates the chunk data unless it hits the end of the file
            if new_character:
                self.chunk_data = self.chunk_data + new_character
            else:
                break

    def _check_and_update_io_files(self, in_file, out_file):
        # If an output file isn't specified, use the input with a replaced file extension
        if out_file is None:
            out_file = in_file.replace(".txt", ".lor")

        # If the input folder or output folders are specified, it updates the corresponding file with a path
        if self.input_folder is not None:
            in_file = f"{self.input_folder}/{in_file}"
        if self.output_folder is not None:
            out_file = f"{self.output_folder}/{out_file}"
        
        # If the input file doesn't exist, an error will be raised
        if not path.exists(in_file):
            raise(FileNotFoundError())

        return in_file, out_file

if __name__ == "__main__":
    file_compressor = compressor(20)
    
    # for file in listdir(COMPRESSION_FOLDER):
    #     if file.endswith(".txt"):
    #         file_compressor.run(f"{COMPRESSION_FOLDER}/{file}")
    # file_compressor.run(f"{COMPRESSION_FOLDER}/textstring_5words_10lines.txt")
    file_compressor.run(f"{COMPRESSION_FOLDER}/empty.txt")