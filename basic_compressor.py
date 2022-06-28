from os import getcwd

class Basic_Compressor(object):
    def __init__(self, file_ext, org_file_ext) -> None:
        self.input_folder = getcwd()
        self.output_folder = self.input_folder
        self.compressed_file_extension = file_ext
        self.org_file_extension = org_file_ext

    def run(self, in_file:str, out_file=None) -> bool:
        """All Compressors should take in a in_file with an optional out_file. 
            They should return True if they successfully compressed the file.
            They should return Falsi if they failed to compress the file."""
        if out_file is None:
            out_file = in_file.replace(self.org_file_type, self.compressed_file_extension)
        return out_file == in_file
