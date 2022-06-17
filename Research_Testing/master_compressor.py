from text_compressor import Text_Compressor
from pattern_compression import Pattern_Compressor

class Master_Compressor(object):
    def __init__(self) -> None:
        self.text_compr = Text_Compressor()
        self.patter_compr = Pattern_Compressor()

    def run(self, in_file:str, out_file=None):
        choice = self.some_decision_logic()
        if choice == 1:
            compress_success = self.text_compr.run(in_file, out_file)
        elif choice == 2:
            compress_success = self.patter_compr.run(in_file, out_file)
        else:
            compress_success = False
        return compress_success

    def some_decision_logic(self):
        pass