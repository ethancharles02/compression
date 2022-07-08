from io import FileIO
from os import path
from src.basic_compressor import Basic_Compressor, WrongFileFormatError


class Text_Decompressor(Basic_Compressor):
    def __init__(self, file_extension=".lort") -> None:
        super().__init__(file_extension)
        self._decompressed_data = []

    def run(self, input_filepath:str, out_folder=None):
        """
        Input:  path to file that will be decompressed:string,
                destination of decompressed file:string
        Output: None
        Description:
        Opens the input file and output file. Reads in words from
        the input file, and writes the decompressed versions to the 
        output file.
        """
        input_file = path.basename(input_filepath)

        if not self._file_has_correct_file_extension(input_file):
            return False

        if out_folder is not None:
            self.output_folder = out_folder
        elif self.output_folder is None:
            self.output_folder = path.dirname(input_filepath)
        out_file = self.output_folder + '/' + self._remove_file_extension(input_file)
        with open(input_filepath, "r") as in_f:
            self._update_look_ahead_from_file(in_f)
            with open(out_file, "w") as out_f:
                while self.read_one_word_to_data(in_f):
                    if len(self._decompressed_data) > self.look_ahead:
                        self._write_word_to(out_f)
                if self._decompressed_data and self._decompressed_data[-1] == '\n':
                    self._decompressed_data.append('') 
                self._write_data_to_output_file(out_f)
        
        return True

    def _update_look_ahead_from_file(self, f:FileIO):
        """
        Gets the look ahead value from a properly formated lort file by
        reading in the look ahead value from the file.
        """
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
        """
        Reads one word from the file until the decompressed
        data is the same length as the look_ahead. This ensures
        that any reference read in will be able to be referenced.
        """
        while len(self._decompressed_data) < self.look_ahead:
            self.read_one_word_to_data(f)

    def read_one_word_to_data(self, f:FileIO):
        """
        Input:  open input file
        Output: Success:Boolean
        Reads one character from the input file until 
        a space or newline is reached, adding the character
        to a word variable. updates the decompressed data 
        with the word variable.
        """
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
        """
        If the word is a reference, decompresses the word.
        Adds the word to decompressed data.
        """
        if word is not None:
            if self.is_reference(word):
                word = self._decompress(word)
            self._decompressed_data.append(word)

    def is_reference(self, word):
        """
        Checks to make sure that the reference character '<' is in
        the word and that the escape character '~' is not in the word,
        Meaning the word is a reference.
        """
        return "<" in word and "~" not in word

    def get_decompressed_data(self):
        """
        Checks for bad values in the decompressed data and removes them.
        Combines the rest of the decompressed data into a single string.
        Returns the string.
        """
        bad_values = []
        for i in range(len(self._decompressed_data)):
            if not isinstance(self._decompressed_data[i], str):
                bad_values.insert(0,i)
        for bad_value in bad_values:
            self._decompressed_data.pop(bad_value)
        if self._decompressed_data and  self._decompressed_data[0] == '\n':
            self._decompressed_data.insert(0, '')
        return " ".join(self._decompressed_data)

    def _decompress(self, reference:str):
        """
        Gets the reference distance from the reference passed in.
        If the reference distance is less than the length of the 
        decompressed data, returns the word that was referenced.
        """
        words_away = int(reference.split('<')[-1])
        if words_away <= len(self._decompressed_data):
            result = self._decompressed_data[-1 * words_away]
            return result

    def _write_word_to(self, f:FileIO):
        """
        Get one word from the decompressed data. Add a space at the end
        of it, if it is not a newline, and the next word isn't a newline.
        Write the word to the file passed in.
        """
        word = self._decompressed_data.pop(0)
        if isinstance(word, str):
            if self._decompressed_data[0] != '\n' and word != '\n':
                word += ' '
            f.write(word)

    def _write_data_to_output_file(self, f:FileIO):
        """
        Formats the decompressed data, then writes it to the
        file that is passed in. 
        """
        f.write(self.get_decompressed_data().replace(" \n ", "\n"))  
