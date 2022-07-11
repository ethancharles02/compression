class WrongFileFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Basic_Compressor(object):
    def __init__(self, file_ext) -> None:
        self.output_folder = None
        self.compressed_file_extension = file_ext

    def run(self, in_file:str, out_folder=None) -> bool:
        """All Compressors should take in a in_file with an optional out_folder. 
            They should return True if they successfully compressed the file.
            They should return False if they failed to compress the file."""
        if out_folder is None:
            out_file = in_file + self.compressed_file_extension
        return out_file == in_file
    
    def _remove_file_extension(self, string:str, optional:bool = False):
        index = string.rfind(self.compressed_file_extension)
        if index != -1:
            return string[:index]
        else:
            if optional:
                return string
            else:
                raise WrongFileFormatError(f"No file extension of {self.compressed_file_extension} found for {string}")
    
    def _get_file_extension(self, string:str, optional:bool = False):
        index = string.rfind(".")
        if index != -1:
            return string[index:]
        else:
            if optional:
                return False
            else:
                raise WrongFileFormatError(f"File extension did not exist on the given file: {string}")
    
    def _file_has_correct_file_extension(self, file:str):
        file_extension = self._get_file_extension(file, optional=True)
        return file_extension and file_extension == self.compressed_file_extension
