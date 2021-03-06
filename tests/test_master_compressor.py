import os
from unittest import TestCase, mock
from sys import path
path.append("..")
from src.master_compressor import Master_Compressor


TXT_FOLDER = "tests/master_compressor_files"
INPUT_FOLDER = f"{TXT_FOLDER}/test_files"
REF_FOLDER = f"{TXT_FOLDER}/reference_files"
OUTPUT_FOLDER = f"{TXT_FOLDER}/dump_files"


class TestMaster_Compressor(TestCase):
    def setUp(self) -> None:
        self.wipe_folder_contents(OUTPUT_FOLDER)
        
        self.MCompressor = Master_Compressor()
        self.MCompressor.compressor_objects["Pattern Compression"][0].run = \
            mock.MagicMock(name="run", return_value=True)
        self.MCompressor.compressor_objects["Pattern Compression"][1].run = \
            mock.MagicMock(name="run", return_value=True)
        self.MCompressor.compressor_objects["Text Compression"][0].run = \
            mock.MagicMock(name="run", return_value=True)
        self.MCompressor.compressor_objects["Text Compression"][1].run = \
            mock.MagicMock(name="run",return_value=True)
        
        self.mock_pool = mock.sentinel
        self.mock_pool.close = mock.MagicMock()
        self.mock_pool.join = mock.MagicMock()
        def side_effect(func, args, callback):
            result = func(*args)
            callback(result)
        self.mock_pool.apply_async = mock.MagicMock(side_effect=side_effect)
        self.MCompressor.create_pool = mock.MagicMock(name="create_pool", return_value=self.mock_pool)

        self.MCompressor.file_extensions[".lor"] = "Text Compression"
        self.MCompressor.compressor_objects["Text Compression"][0].compressed_file_extension = ".lor"
        self.MCompressor.compressor_objects["Text Compression"][1].compressed_file_extension = ".lor"

    def wipe_folder_contents(self, folder):
        for f in os.listdir(folder):
            folder_path = os.path.join(folder, f)
            if os.path.isfile(folder_path):
                os.remove(folder_path)
            elif os.path.isdir(folder_path):
                os.rmdir(folder_path)
                
    def tearDown(self) -> None:
        self.wipe_folder_contents(OUTPUT_FOLDER)
    
    def test_compress_folder_calls_compressor_run(self):
        self.MCompressor.compress_folder(INPUT_FOLDER, OUTPUT_FOLDER, "Text Compression")
        compressed_folder = os.path.join(OUTPUT_FOLDER, os.path.basename(os.path.normpath(INPUT_FOLDER + ".lor")))
        calls = [mock.call(INPUT_FOLDER + '\\' + "text_generic.txt",compressed_folder),
                 mock.call(INPUT_FOLDER + '\\' + "text_three_chunks.txt",compressed_folder),
                 mock.call(INPUT_FOLDER + '\\' + "text_with_newlines.txt",compressed_folder)]
        self.MCompressor.compressor_objects["Text Compression"][0].run.assert_has_calls(calls, any_order=False)

    def test_compress_folder_returns_true_when_compresses_some_file(self):
        self.assertEqual(self.MCompressor.compress_folder(INPUT_FOLDER, OUTPUT_FOLDER, "Text Compression"), True)

    def test_compress_folder_returns_false_when_no_file_is_compressed(self):
        self.MCompressor.copy_over = mock.MagicMock(return_value=True, name="copy_over")
        self.MCompressor.compressor_objects["Text Compression"][0].run = \
            mock.MagicMock(name="run", return_value=False)
        self.MCompressor.compressor_objects["Text Compression"][1].run = \
            mock.MagicMock(name="run",return_value=False)
        self.assertEqual(self.MCompressor.compress_folder(INPUT_FOLDER, OUTPUT_FOLDER, "Text Compression"), False)
        self.MCompressor.copy_over.assert_has_calls([])
       
    def test_decompress_folder_calls_decompressor_run(self):
        self.MCompressor.decompress_folder(REF_FOLDER, OUTPUT_FOLDER)
        decompressed_folder = os.path.join(OUTPUT_FOLDER, os.path.basename(os.path.normpath(self.MCompressor._remove_file_extension(REF_FOLDER, ".lor", True))))
        calls = [mock.call(REF_FOLDER + '\\' + "text_generic.txt.lor",decompressed_folder),
                 mock.call(REF_FOLDER + '\\' + "text_three_chunks.txt.lor",decompressed_folder),
                 mock.call(REF_FOLDER + '\\' + "text_with_newlines.txt.lor",decompressed_folder)]
        self.MCompressor.compressor_objects["Text Compression"][1].run.assert_has_calls(calls, any_order=False)

    def test_decompress_folder_returns_true_when_decompresses_some_file(self):
        self.assertEqual(self.MCompressor.decompress_folder(REF_FOLDER, OUTPUT_FOLDER), True)

    def test_decompress_folder_returns_false_when_no_file_decompresses(self):
        self.MCompressor.copy_over = mock.MagicMock(return_value=True, name="copy_over")
        self.assertEqual(self.MCompressor.decompress_folder(INPUT_FOLDER, OUTPUT_FOLDER), False)
        self.MCompressor.copy_over.assert_has_calls([])

    def test_copy_over(self):
        in_file = INPUT_FOLDER + "/text_generic.txt"
        self.MCompressor.copy_over(in_file, OUTPUT_FOLDER)

    def test_decompress_folder_only_decompresses_one_file(self):
        self.MCompressor.copy_over = mock.MagicMock(return_value=True, name="copy_over")
        in_folder = f"{TXT_FOLDER}/one_compressed_file.lor"
        self.MCompressor.decompress_folder(in_folder, OUTPUT_FOLDER)
        decompressed_folder = os.path.join(OUTPUT_FOLDER, os.path.basename(os.path.normpath(self.MCompressor._remove_file_extension(in_folder, ".lor", True))))
        calls = [mock.call(in_folder + '\\' + "text_generic.txt.lor",decompressed_folder)]
        self.MCompressor.compressor_objects["Text Compression"][1].run.assert_has_calls(calls, any_order=False)
        calls = [mock.call(in_folder + '\\' + "text_three_chunks.txt",decompressed_folder),
                 mock.call(in_folder + '\\' + "text_with_newlines.txt",decompressed_folder)]
        self.MCompressor.copy_over.assert_has_calls(calls, any_order=False)

    def test_parallel_folder_compression(self):
        self.MCompressor.compress_folder(INPUT_FOLDER, OUTPUT_FOLDER, "Text Compression")
        compressed_folder = os.path.join(OUTPUT_FOLDER, os.path.basename(os.path.normpath(INPUT_FOLDER + ".lor")))
        empty_call = [mock.call()]
        calls = [mock.call(self.MCompressor.compress,
                            args=(INPUT_FOLDER+'\\'+"text_generic.txt", compressed_folder, "Text Compression"), 
                            callback=self.MCompressor.callback_result),
                 mock.call(self.MCompressor.compress,
                            args=(INPUT_FOLDER+'\\'+"text_three_chunks.txt", compressed_folder, "Text Compression"), 
                            callback=self.MCompressor.callback_result),
                 mock.call(self.MCompressor.compress,
                            args=(INPUT_FOLDER+'\\'+"text_with_newlines.txt", compressed_folder, "Text Compression"), 
                            callback=self.MCompressor.callback_result)]
        
        self.MCompressor.create_pool.assert_has_calls(empty_call)
        self.mock_pool.apply_async.assert_has_calls(calls)
        self.mock_pool.join.assert_has_calls(empty_call)
        self.mock_pool.close.assert_has_calls(empty_call)