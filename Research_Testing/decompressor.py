from text_decompression import Text_Decompressor
from os import getcwd

class WrongFileFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Decompressor(object):
    def __init__(self) -> None:
        self.input_folder = getcwd()
        self.output_folder = self.input_folder
        self.decompressed_data = []
        self.txt_decompressor = Text_Decompressor()

    def run(self, input_file:str):
        with open(f"{self.input_folder}/{input_file}", "r") as f:
            self.get_look_ahead(f)
            data = "\n".join(f.readlines())
        with open(f"{self.output_folder}/{input_file.replace('.lor', '.txt')}", "w") as f:
            self.txt_decompressor.decompress(data)
            f.writelines(self.txt_decompressor.get_decompressed_data())

    def get_look_ahead(self, f):
        char = f.read(1)
        if char != "[":
            raise(WrongFileFormatError("File does not contain look ahead!"))
        look_ahead = ""
        char = f.read(1)
        while char != "]":
            look_ahead += char
            char = f.read(1)
        self.look_ahead = int(look_ahead)

    def fill_decompressed_data(self, f):
        while len(self.decompressed_data) < self.look_ahead:
            self.read_one_word(f)

    def read_one_word(self, f):
        char = f.read(1)
        word = ""
        while(char != ' ' and char != ''):
            word += char
            char = f.read(1)
        self.decompressed_data.append(word)

    def get_decompressed_data(self):
        return " ".join(self.decompressed_data)
