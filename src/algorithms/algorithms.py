from src.algorithms.text_compression.text_compressor import Text_Compressor
from src.algorithms.text_compression.text_decompressor import Text_Decompressor

from src.algorithms.pattern_compression.pattern_compressor import Pattern_Compressor
from src.algorithms.pattern_compression.pattern_decompressor import Pattern_Decompressor

ALGORITHMS = {
    "Text Compression" : [
        ".lort",],
    "Pattern Compression" : [
        ".lorp",]
}

ALGORITHMS_OBJECTS = {
    "Text Compression" : [Text_Compressor(), Text_Decompressor()],
    "Pattern Compression" : [Pattern_Compressor(), Pattern_Decompressor()]
}