from unittest import TestCase, mock
from sys import path
path.append("..")
from src.master_compressor import Master_Compressor


TXT_FOLDER = "tests/compressor_text_files"
INPUT_FOLDER = f"{TXT_FOLDER}/test_files"
REF_FOLDER = f"{TXT_FOLDER}/reference_files"
OUTPUT_FOLDER = f"{TXT_FOLDER}/dump_files"

class TestMaster_Compressor(TestCase):
    def setUp(self) -> None:
        self.MCompressor = Master_Compressor()
        for algorithm in self.MCompressor.compressor_objects:
            self.MCompressor.compressor_objects[algorithm][0].run = mock.MagicMock()
            self.MCompressor.compressor_objects[algorithm][1].run = mock.MagicMock()
        return super().setUp()

    def test_Can_Call_Compress_folder(self):
        self.MCompressor.compress_folder(INPUT_FOLDER, OUTPUT_FOLDER)

    
