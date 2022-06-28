from text_compression.text_compressor import Text_Compressor
from text_compression.text_decompressor import Text_Decompressor

from pattern_compression.pattern_compressor import Pattern_Compressor
from pattern_compression.pattern_decompressor import Pattern_Decompressor


class Master_Compressor(object):
    def __init__(self) -> None:
        self.in_folder = None
        self.out_folder = None
        self.text_compr = Text_Compressor()
        self.text_decompr = Text_Decompressor()
        self.patter_compr = Pattern_Compressor()
        self.patter_decompr = Pattern_Decompressor()


    def compress(self, in_file:str, out_file=None):
        choice = self.some_decision_logic()
        if choice == 1:
            self.text_compr.input_folder = self.in_folder
            self.text_decompr.output_folder = self.out_folder
            compress_success = self.text_compr.run(in_file, out_file)
        elif choice == 2:
            self.patter_compr.input_folder = self.in_folder
            self.patter_decompr.output_folder = self.out_folder
            compress_success = self.patter_compr.run(in_file, out_file)
        else:
            compress_success = False
        return compress_success

    def decompress(self, in_file:str, out_file=None):
        choice = self.some_decision_logic()
        if choice == 1:
            assert ""
            self.text_compr.input_folder = self.in_folder
            self.text_decompr.output_folder = self.out_folder
            compress_success = self.text_decompr.run(in_file, out_file)
        elif choice == 2:
            self.patter_compr.input_folder = self.in_folder
            self.patter_decompr.output_folder = self.out_folder
            compress_success = self.patter_decompr.run(in_file, out_file)
        else:
            compress_success = False
        return compress_success

    def some_decision_logic(self):
        return 1