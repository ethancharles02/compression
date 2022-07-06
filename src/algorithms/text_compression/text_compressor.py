# TODO
# Add docstrings
# Create decompressors for each algorithm
# Move/create constants for compressors
from os import path, fstat, remove as os_remove
from src.algorithms.text_compression.text_compression_algorithm import Text_Compression_Algorithm
from src.basic_compressor import Basic_Compressor
from time import monotonic

COMPRESSION_FOLDER = "Research_Testing/random_textstring_files"

class Text_Compressor(Basic_Compressor):
    def __init__(self, chunk_size=1024, look_ahead=5):
        super().__init__(".lort")
        self.chunk_size = chunk_size
        self.look_ahead = look_ahead
        self.text_compr_alg = Text_Compression_Algorithm(self.look_ahead)

        self._chunk_data = None
        self._bits_read = 0
        self._file_size = 0
        self._print_time = 5
        self._print_cur_time = 0
        
    def run(self, in_file:str, out_folder=None):
        """
        Input:  file to compress:str, destination of compressed file:str
        Output: Did the file compress successfully:Boolean
        Description:
        Creates and writes the look_ahead to the output file. Opens and 
        reads in chunks of data from the input file. Periodically,
        appends chunks of compressed data to the output file. 
        Updates a progress percentage.
        """
        if out_folder is not None:
            self.output_folder = out_folder
        if not path.exists(in_file):
            raise(FileNotFoundError())
        
        out_file = self._get_out_file(in_file)

        with open(out_file, 'w') as f:
            f.write(f"[{self.look_ahead}]")

        with open(in_file, 'r') as f:
            self._file_size = fstat(f.fileno()).st_size
            # Get chunk data
            # self.chunk_data = f.read(self.chunk_size)
            self._chunk_data = self._read_chunk_data(f, self.chunk_size)

            
            self._print_cur_time = monotonic()

            # As long as there is more data to read:
            while self._chunk_data:
                if monotonic() - self._print_cur_time >= self._print_time:
                    self._print_percentage_completion(2)
                    self._print_cur_time = monotonic()

                # Append additional chunk data till it has a full word at the end
                self._update_chunk_data_to_end_of_word(f)

                # Compress the chunk 
                self.text_compr_alg.compress(self._chunk_data)
                # write the chunk to the output file
                with open(out_file, 'a') as new_f:
                    new_f.write(self.text_compr_alg.get_compressed_data())
                
                # Get new chunk data
                # self.chunk_data = f.read(self.chunk_size)
                self._chunk_data = self._read_chunk_data(f, self.chunk_size)
            self._print_percentage_completion(2)
        
        if self._compressed_successfully(in_file, out_file):
            return True
        else:
            os_remove(out_file)
            return False

    def _compressed_successfully(self, input_filepath, output_filepath):
        """
        """
        with open(input_filepath, 'r') as f:
            input_size = fstat(f.fileno()).st_size

        with open(output_filepath, 'r') as f:
            output_size = fstat(f.fileno()).st_size
        
        return output_size < input_size

    def _print_percentage_completion(self, decimals):
        print(f"{round(self._get_percentage_completion() * 100, decimals)}%")

    def _get_percentage_completion(self):
        if self._file_size > 0:
            percent = self._bits_read / self._file_size
            return percent if percent < 1 else 1
        else:
            return 1

    def _read_chunk_data(self, file, chunk_size = 1):
        """
        Input:  open file, chunk size
        Output: data
        Description:
        Reads in a chunk of data from the file. Returns
        the data.
        """
        self._bits_read += chunk_size
        data = file.read(chunk_size)
        return data

    def _update_chunk_data_to_end_of_word(self, f):
        """
        Continue to read in one character of data, until you reach the end of a word.
        """
        # Keeps reading in chunk data till the last character is a space
        while self._chunk_data[-1] != " ":
            new_character = self._read_chunk_data(f, 1)
            # Updates the chunk data unless it hits the end of the file
            if new_character:
                self._chunk_data = self._chunk_data + new_character
            else:
                break

    def _get_out_file(self, in_file):
        """
        Input:  input file:string
        Output: output file:string
        Description:
        Creates the filepath to the output file based on the output folder,
        and input file.
        """
        # If an output folder isn't specified, the out file is 
        # the same as the in file except with the added file extension
        if self.output_folder is None:
            out_file =  in_file + self.compressed_file_extension
        # Otherwise add the file extension to the infile name and put that in the out folder
        else:
            out_file = self.output_folder + '/' + path.basename(in_file) + self.compressed_file_extension
        return out_file
