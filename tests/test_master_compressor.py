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
        self.MCompressor = Master_Compressor()
        self.MCompressor.compressor_objects["Pattern Compression"][0].run = \
            mock.MagicMock(name="run", return_value=True)
        self.MCompressor.compressor_objects["Pattern Compression"][1].run = \
            mock.MagicMock(name="run", return_value=True)
        self.MCompressor.compressor_objects["Text Compression"][0].run = \
            mock.MagicMock(name="run", return_value=True)
        self.MCompressor.compressor_objects["Text Compression"][1].run = \
            mock.MagicMock(name="run",return_value=True)
    
        self.MCompressor.file_extensions[".lor"] = "Text Compression"
        self.MCompressor.compressor_objects["Text Compression"][0].compressed_file_extension = ".lor"
        self.MCompressor.compressor_objects["Text Compression"][1].compressed_file_extension = ".lor"

    def tearDown(self) -> None:
        for f in os.listdir(OUTPUT_FOLDER):
            folder_path = os.path.join(OUTPUT_FOLDER, f)
            if os.path.isdir(folder_path):
                os.rmdir(folder_path)
            
    # def test_Can_Call_Compress_folder(self):
    #     self.MCompressor.compress_folder(INPUT_FOLDER, OUTPUT_FOLDER)

    # def test_can_call_decompress_folder(self):
    #     self.MCompressor.decompress_folder(REF_FOLDER, OUTPUT_FOLDER)
    
    def test_compress_folder_calls_compressor_run(self):
        self.MCompressor.compress_folder(INPUT_FOLDER, OUTPUT_FOLDER)
        compressed_folder = os.path.join(OUTPUT_FOLDER, os.path.basename(os.path.normpath(INPUT_FOLDER + ".lor")))
        calls = [mock.call(INPUT_FOLDER + '\\' + "text_generic.txt",compressed_folder),
                 mock.call(INPUT_FOLDER + '\\' + "text_three_chunks.txt",compressed_folder),
                 mock.call(INPUT_FOLDER + '\\' + "text_with_newlines.txt",compressed_folder)]
        self.MCompressor.compressor_objects["Text Compression"][0].run.assert_has_calls(calls, any_order=False)

    def test_compress_folder_returns_true_when_compresses_some_file(self):
        self.assertEqual(self.MCompressor.compress_folder(INPUT_FOLDER, OUTPUT_FOLDER), True)
       
    def test_decompress_folder_calls_decompressor_run(self):
        self.MCompressor.decompress_folder(REF_FOLDER, OUTPUT_FOLDER)
        decompressed_folder = os.path.join(OUTPUT_FOLDER, os.path.basename(os.path.normpath(self.MCompressor._remove_file_extension(REF_FOLDER, ".lor", True))))
        calls = [mock.call(REF_FOLDER + '\\' + "text_generic.txt.lor",decompressed_folder),
                 mock.call(REF_FOLDER + '\\' + "text_three_chunks.txt.lor",decompressed_folder),
                 mock.call(REF_FOLDER + '\\' + "text_with_newlines.txt.lor",decompressed_folder)]
        self.MCompressor.compressor_objects["Text Compression"][1].run.assert_has_calls(calls, any_order=False)

    def test_decompress_folder_returns_true_when_compresses_some_file(self):
        self.assertEqual(self.MCompressor.decompress_folder(REF_FOLDER, OUTPUT_FOLDER), True)

    # TODO add a test for incorrect file extension
