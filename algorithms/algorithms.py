from algorithms.text_compression.text_compressor import Text_Compressor
from algorithms.text_compression.text_decompressor import Text_Decompressor

from algorithms.pattern_compression.pattern_compressor import Pattern_Compressor
from algorithms.pattern_compression.pattern_decompressor import Pattern_Decompressor

ALGORITHMS = {
    "Text Compression" : [
        ".lort",
        ["algorithms.text_compression.text_compressor", "Text_Compressor"],
        ["algorithms.text_compression.text_decompressor", "Text_Decompressor"]],
    "Pattern Compression" : [
        ".lorp", 
        ["algorithms.pattern_compression.pattern_compressor", "Pattern_Compressor"], 
        ["algorithms.pattern_compression.pattern_decompressor", "Pattern_Decompressor"]
    ]
}

ALGORITHMS_OBJECTS = {
    "Text Compression" : [Text_Compressor(), Text_Decompressor()],
    "Pattern Compression" : [Pattern_Compressor(), Pattern_Decompressor()]
}
# ALGORITHMS = {
#     "Text Compression" : [
#         ".lort",
#         ["text_compressor", "Text_Compressor"],
#         ["text_decompressor", "Text_Decompressor"]],
#     "Pattern Compression" : [
#         ".lorp", 
#         ["pattern_compressor", "Pattern_Compressor"], 
#         ["pattern_decompressor", "Pattern_Decompressor"]
#     ]
# }