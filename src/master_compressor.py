from os import mkdir
from src.algorithms.algorithms import ALGORITHMS, ALGORITHMS_OBJECTS

class WrongFileType(Exception):
    pass

class Master_Compressor(object):
    def __init__(self) -> None:
        self.algorithms = ALGORITHMS
        self.file_extensions = {}
        for key in self.algorithms:
            self.file_extensions[self.algorithms[key][0]] = key

        self.algorithms_list = self.algorithms.keys()
        self.compressor_objects = ALGORITHMS_OBJECTS

    def _get_file_extension(self, string:str):
        index = string.rfind(".")
        if index != -1:
            return string[index:]
        else:
            raise ValueError(f"File extension did not exist on the given file: {string}")

    def _get_compressor(self, algorithm):
        if algorithm is None:
            compressor = self.compressor_objects[self.algorithms_list[0]][0]
        else:
            compressor = self.compressor_objects[algorithm][0]
        return compressor

    def compress(self, in_file:str, out_folder=None, algorithm=None):
        compressor = self._get_compressor(algorithm)
        compress_success = compressor.run(in_file, out_folder)
        return compress_success

    def decompress(self, in_file:str, out_folder=None):
        algorithm = self._get_algorithm_for_file_extension(self._get_file_extension(in_file))
        decompress_success = self.compressor_objects[algorithm][1].run(in_file, out_folder)
        return decompress_success

    def _get_algorithm_for_file_extension(self, file_extension):
        if file_extension not in self.file_extensions:
            raise ValueError(f"No file extension found for decompressing {file_extension} files")

        return self.file_extensions[file_extension]

    def compress_folder(self, in_folder:str, out_folder=None, algorithm=None):
        compressor = self._get_compressor(algorithm)
        results = self.run_function_on_files_in_folder(in_folder, compressor.run)
        # TODO filter results. If all failed, delete the folder and files.
        return False  # This will change to if all the results failed or not.

    def decompress_folder(self, in_folder:str, out_folder=None):
        folder_files = []
        algorithms = []
        # TODO Get a list of files. 
        for file in folder_files:
            algorithms.append((self._get_algorithm_for_file_extension(self._get_file_extension(file)), file))
        results = []
        for algorithm in algorithms:
            results.append(self.compressor_objects[algorithms[0]][1].run(algorithms[1], out_folder))
        return results  # TODO This should really return if all of them failed or not.

    def run_function_on_files_in_folder(self, function, folder):
        folder_files = []
        # TODO grab all files in the folder
        results = []
        for file in folder_files:
            results.append(function(file))
        return results