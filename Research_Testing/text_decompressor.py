from io import FileIO
from os import getcwd

class WrongFileFormatError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class Text_Decompressor(object):
    def __init__(self) -> None:
        self.input_folder = getcwd()
        self.output_folder = self.input_folder
        self._decompressed_data = []

    def run(self, input_file:str):
        with open(f"{self.input_folder}/{input_file}", "r") as in_f:
            self._update_look_ahead_from_file(in_f)
            with open(f"{self.output_folder}\\{input_file.replace('.lor', '.txt')}", "w") as out_f:
                while self.read_one_word_to_data(in_f):
                    if len(self._decompressed_data) > self.look_ahead:
                        self._write_word_to(out_f)
                self._write_data_to_output_file(out_f)

    def _update_look_ahead_from_file(self, f:FileIO):
        char = f.read(1)
        if char != "[":
            raise(WrongFileFormatError("File does not contain look ahead!"))
        look_ahead = ""
        char = f.read(1)
        while char != "]":
            look_ahead += char
            char = f.read(1)
        self.look_ahead = int(look_ahead)

    def fill_decompressed_data(self, f:FileIO):
        while len(self._decompressed_data) < self.look_ahead:
            self.read_one_word_to_data(f)

    def read_one_word_to_data(self, f:FileIO):
        char = f.read(1)
        if char:
            word = ""
            while(char.strip() != ''):
                word += char
                char = f.read(1)
            self._update_decompressed_data(word)
            if char == '\n':
                self._decompressed_data.append('\n')
            return True
        else:
            return False

    def _update_decompressed_data(self, word):
        assert word is not None
        if self.is_reference(word):
            self._decompressed_data.append(self._decompress(word))
        else:
            self._decompressed_data.append(word)

    def is_reference(self, word):
        return "<" in word and "~" not in word

    def get_decompressed_data(self):
        bad_values = []
        for i in range(len(self._decompressed_data)):
            if not isinstance(self._decompressed_data[i], str):
                bad_values.insert(0,i)
        for bad_value in bad_values:
            self._decompressed_data.pop(bad_value)
        return " ".join(self._decompressed_data)

    def _decompress(self, reference:str):
        words_away = int(reference.split('<')[-1])
        if words_away <= len(self._decompressed_data):
            result = self._decompressed_data[-1 * words_away]
            # with open("decompress.log", "a") as f:
            #     f.write(result)
            #     f.write(",: ")
            #     f.write(",".join(self._decompressed_data))
            #     f.write('\n')
            assert result is not None
            return result

    def _write_word_to(self, f:FileIO):
        word = self._decompressed_data.pop(0)
        if isinstance(word, str):
            if self._decompressed_data[0] != '\n' and word != '\n':
                word += ' '
            f.write(word)

    def _write_data_to_output_file(self, f:FileIO):
        f.write(self.get_decompressed_data().replace(" \n ", "\n"))  
