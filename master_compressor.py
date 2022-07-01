# TODO
# Move get file extension function from here and pattern compressor to helper function file

# from os import path
# from json import load

class WrongFileType(Exception):
    pass

class Master_Compressor(object):
    def __init__(self, algorithms) -> None:
        # from algorithms.text_compression.text_compressor import Text_Compressor
        # from algorithms.text_compression.text_decompressor import Text_Decompressor

        # from algorithms.pattern_compression.pattern_compressor import Pattern_Compressor
        # from algorithms.pattern_compression.pattern_decompressor import Pattern_Decompressor

        self.algorithms = algorithms
        self.file_extensions = {}
        for key in self.algorithms:
            self.file_extensions[self.algorithms[key][0]] = key

        self.algorithms_list = self.algorithms.keys()
        self.algorithm_objects = {}
        for algorithm in self.algorithms:
            exec(f"from {self.algorithms[algorithm][1][0]} import {self.algorithms[algorithm][1][1]}")
            exec(f"from {self.algorithms[algorithm][2][0]} import {self.algorithms[algorithm][2][1]}")
            self.algorithm_objects[algorithm] = [eval(f"{self.algorithms[algorithm][1][1]}()"), eval(f"{self.algorithms[algorithm][2][1]}()")]

        # self.text_compr = Text_Compressor()
        # self.text_decompr = Text_Decompressor()
        # self.patter_compr = Pattern_Compressor()
        # self.patter_decompr = Pattern_Decompressor()

    def _get_file_extension(self, string:str):
        index = string.rfind(".")
        if index != -1:
            return string[index:]
        else:
            raise ValueError(f"File extension did not exist on the given file: {string}")

    def compress(self, in_file:str, out_folder=None, algorithm=None):
        if algorithm is None:
            algorithm = self.algorithms_list[0]
        compress_success = self.algorithm_objects[algorithm][0].run(in_file, out_folder)
        # choice = self.some_decision_logic()
        # if choice == 1:
        #     if ".txt" not in in_file:
        #         raise WrongFileType()
        #     compress_success = self.text_compr.run(in_file, out_folder)
        # elif choice == 2:
        #     compress_success = self.patter_compr.run(in_file, out_folder)
        # else:
        #     compress_success = False
        return compress_success

    def decompress(self, in_file:str, out_folder=None):
        algorithm = self._get_algorithm_for_file_extension(self._get_file_extension(in_file))
        decompress_success = self.algorithm_objects[algorithm][1].run(in_file, out_folder)
        # choice = self.some_decision_logic()
        # if choice == 1:
        #     if ".lor" not in in_file:
        #         raise WrongFileType()
        #     compress_success = self.text_decompr.run(in_file, out_folder)
        # elif choice == 2:
        #     compress_success = self.patter_decompr.run(in_file, out_folder)
        # else:
        #     compress_success = False
        return decompress_success

    def _get_algorithm_for_file_extension(self, file_extension):
        if file_extension not in self.file_extensions:
            raise ValueError(f"No file extension found for decompressing {file_extension} files")

        return self.file_extensions[file_extension]

    def some_decision_logic(self):
        return 1