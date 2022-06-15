from io import FileIO
from os import getcwd

class WrongFileFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Decompressor(object):
    def __init__(self) -> None:
        self.input_folder = getcwd()
        self.output_folder = self.input_folder
        self._decompressed_data = []
        self._last_word_written = None
        self._has_written_from_overflow = False

    def run(self, input_file:str):
        with open(f"{self.input_folder}/{input_file}", "r") as in_f:
            self._get_look_ahead(in_f)
            with open(f"{self.output_folder}/{input_file.replace('.lor', '.txt')}", "w") as out_f:
                while self.read_one_word(in_f):
                    self._write_overflow_to_output_file(out_f)
                if self._has_written_from_overflow:
                    out_f.write(' ')
                self._write_data_to_output_file(out_f)

    def _get_look_ahead(self, f):
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
        while len(self._decompressed_data) < self.look_ahead:
            self.read_one_word(f)

    def read_one_word(self, f):
        char = f.read(1)
        if char:
            word = ""
            while(char != ' ' and char != '' and char != '\n'):
                word += char
                char = f.read(1)
            self._decompressed_data.append(self._decompress(word))
            if char == '\n':
                self._decompressed_data.append('\n')
            return True
        else:
            return False

    def get_decompressed_data(self):
        return " ".join(self._decompressed_data)

    def _decompress(self, reference):
        if "<" in reference and "~" not in reference:
            words_away = int(reference.split('<')[-1])
            if words_away <= len(self._decompressed_data):
                result = self._decompressed_data[-1 * words_away]
                if reference[0] == '\n':
                    result = '\n' + result
                if reference[-1] == '\n':
                    result = result + '\n'
                return result
        return reference

    def _write_overflow_to_output_file(self, f:FileIO):
        if len(self._decompressed_data) > self.look_ahead:
            word = self._decompressed_data.pop(0)
            if self._last_word_written is not None:
                if word != '\n' and self._last_word_written != '\n':
                    word = ' ' + word
                self._last_word_written = word
            else:
                self._last_word_written = word
            f.write(word)
            self._has_written_from_overflow = True

    def _write_data_to_output_file(self, f:FileIO):
        f.write(self.get_decompressed_data().replace(" \n ", "\n"))  
