from os import mkdir, path, listdir
from shutil import copyfile
from src.basic_compressor import WrongFileFormatError
from src.algorithms.algorithms import ALGORITHMS, ALGORITHMS_OBJECTS

class WrongFileType(Exception):
    pass

class Master_Compressor(object):
    def __init__(self) -> None:
        self.algorithms = ALGORITHMS
        self.file_extensions = {}
        for key in self.algorithms:
            self.file_extensions[self.algorithms[key][0]] = key

        self.algorithms_list = list(self.algorithms.keys())
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
        if not algorithm:
            return False
        decompress_success = self.compressor_objects[algorithm][1].run(in_file, out_folder)
        return decompress_success

    def _get_algorithm_for_file_extension(self, file_extension, optional:bool = False):
        if file_extension not in self.file_extensions:
            if optional:
                return False
            else:
                raise ValueError(f"No file extension found for decompressing {file_extension} files")

        return self.file_extensions[file_extension]

    def _remove_file_extension(self, string:str, file_extension:str, optional:bool = False):
        index = string.rfind(file_extension)
        if index != -1:
            return string[:index]
        else:
            if optional:
                return string
            else:
                raise WrongFileFormatError(f"No file extension of {file_extension} found for {string}")

    def compress_folder(self, in_folder:str, out_folder=None, algorithm=None):
        compressed_folder = path.join(out_folder, path.basename(path.normpath(in_folder)) + ".lor")
        if path.exists(compressed_folder):
            raise Exception("Folder already exists")
        mkdir(compressed_folder)
        results = self.run_function_on_files_in_folder(self.compress, in_folder, [compressed_folder, algorithm])
        return any(results)  

    def decompress_folder(self, in_folder:str, out_folder=None):
        decompressed_folder = path.join(out_folder, path.basename(path.normpath(self._remove_file_extension(in_folder, ".lor", True))))
        if path.exists(decompressed_folder):
            raise Exception("Folder already exists")
        mkdir(decompressed_folder)
        results = self.run_function_on_files_in_folder(self.decompress, in_folder, [decompressed_folder])
        return any(results) 

    def run_function_on_files_in_folder(self, func, folder:str, args:list):
        results = []
        for f in listdir(folder):
            result = func(path.join(folder, f), *args)
            if not result:
                copyfile(path.join(folder, f), args[0])
            results.append(result)
        return results