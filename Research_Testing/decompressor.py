from text_decompression import Text_Decompressor
from os import getcwd

class Decompressor(object):
    def __init__(self) -> None:
        self.input_folder = getcwd()
        self.output_folder = self.input_folder
        self.txt_decompressor = Text_Decompressor()

    def run(self, input_file:str):
        with open(f"{self.input_folder}/{input_file}", "r") as f:
            data = "\n".join(f.readlines())
        with open(f"{self.output_folder}/{input_file.replace('.lor', '.txt')}", "w") as f:
            self.txt_decompressor.decompress(data)
            f.writelines(self.txt_decompressor.get_decompressed_data())