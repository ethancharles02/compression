from os import mkdir, path, listdir, remove, rmdir
from shutil import copyfile
import multiprocessing as mp
# from time import monotonic

from src.basic_compressor import WrongFileFormatError
from src.algorithms.algorithms import ALGORITHMS, ALGORITHMS_OBJECTS

class WrongFileType(Exception):
    pass

class Master_Compressor(object):
    def __init__(self, run_in_parallel:bool = True) -> None:
        self.algorithms = ALGORITHMS
        self.file_extensions = {}
        for key in self.algorithms:
            self.file_extensions[self.algorithms[key][0]] = key

        self.algorithms_list = list(self.algorithms.keys())
        self.compressor_objects = ALGORITHMS_OBJECTS

        self.run_in_parallel = run_in_parallel
        if self.run_in_parallel:
            self.processor_count = mp.cpu_count()

        self.results = []

    def _get_file_extension(self, string:str):
        index = string.rfind(".")
        if index != -1:
            return string[index:]
        else:
            return None

    def _get_compressor(self, algorithm):
        if algorithm is None:
            compressor = self.compressor_objects[self.algorithms_list[0]][0]
        else:
            compressor = self.compressor_objects[algorithm][0]
        return compressor

    def compress(self, in_file:str, out_folder=None, algorithm=None):
        compressor = self._get_compressor(algorithm)
        compress_success = compressor.run(in_file, out_folder)

        if not compress_success:
            return (compress_success, in_file, out_folder)
        else:
            return (compress_success, None, None)

    def decompress(self, in_file:str, out_folder=None):
        file_extension = self._get_file_extension(in_file)
        if not file_extension:
            return (False, in_file, out_folder)
        algorithm = self._get_algorithm_for_file_extension(file_extension)
        if not algorithm:
            return (False, in_file, out_folder)
        decompress_success = self.compressor_objects[algorithm][1].run(in_file, out_folder)

        if not decompress_success:
            return (decompress_success, in_file, out_folder)
        else:
            return (decompress_success, None, None)

    def _get_algorithm_for_file_extension(self, file_extension):
        if file_extension not in self.file_extensions:
            return None
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
        result = self.run_function_on_files_in_folder(self.compress, in_folder, [compressed_folder, algorithm])
        return result

    def decompress_folder(self, in_folder:str, out_folder=None):
        decompressed_folder = path.join(out_folder, path.basename(path.normpath(self._remove_file_extension(in_folder, ".lor", True))))
        if path.exists(decompressed_folder):
            raise Exception("Folder already exists")
        mkdir(decompressed_folder)
        result = self.run_function_on_files_in_folder(self.decompress, in_folder, [decompressed_folder])
        return result

    def callback_result(self, result):
        self.results.append(result)

    def create_pool(self):
        return mp.Pool(self.processor_count)

    def run_function_on_files_in_folder(self, func, folder:str, args:list):
        # old_time = monotonic()
        if self.run_in_parallel:
            folder_pool = self.create_pool()
            for f in listdir(folder):
                folder_pool.apply_async(func, args=(path.join(folder, f), *args), callback=self.callback_result)

            folder_pool.close()
            folder_pool.join()
        else:
            for f in listdir(folder):
                result = func(path.join(folder, f), *args)
                self.results.append(result)

        # print(f"Time to completion{' with parallelism' if self.run_in_parallel else ''}: {monotonic() - old_time}")

        final_result = any([result[0] for result in self.results])
        if not final_result:
            self.remove_failed_folder(args[0])
        else:
            for result in self.results:
                if not result[0]:
                    self.copy_over(result[1], result[2])

        self.results.clear()
        return final_result

    def remove_failed_folder(self, folder):
        for f in listdir(folder):
            remove(path.join(folder, f))
        rmdir(folder)


    def copy_over(self, in_file, out_folder):
        out_file = out_folder + '/' + path.basename(in_file)
        copyfile(in_file, out_file)