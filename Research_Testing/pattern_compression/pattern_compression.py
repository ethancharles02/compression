# TODO
# Add docstrings

# The behavior of the compressor is as follows:
# It is given a max_look_ahead value. This is how far it will look for patterns
# It is given a raw_delimiter value. This is the delimiter without accounting for fixing previously existing delimiters in the bitstring.
# It is given a pattern_count_num_bits values. This can be None to indicate that any number of patterns can exist. Otherwise, the number of patterns that can exist is 2^pattern_count_num_bits

# Once the compression happens, any raw delimiters that exist are replaced with the corresponding delimiter string that won't mess with the delimiter.
# Compression only happens if bits will be saved in the process, it will place a delimiter before the pattern and one after to indicate that it is the pattern.
# After that second delimiter, a number of bits will indicate how many times the pattern occurs. If the number of bits isn't set, a third delimiter will exist at the end of the number to indicate this
class Pattern_Compressor(object):
    def __init__(self, max_look_ahead:int, raw_delimiter:str = "11111", pattern_count_num_bits = None):
        self.data = []
        self.max_look_ahead = max_look_ahead

        self._raw_delimiter = raw_delimiter
        self._delimiter = self._raw_delimiter + "1"
        self._delimiter_replace_string = self._raw_delimiter + "0"
        self._delimiter_length = len(self._delimiter)

        # If a count for patterns is set, there will only need to be two delimiters instead of three for each pattern
        self._pattern_count_num_bits = pattern_count_num_bits
        self.is_pattern_count_limited = False
        self.delimiter_cost = self._delimiter_length * 3

        if self._pattern_count_num_bits is not None:
            self.is_pattern_count_limited = True
            self.delimiter_cost = self._delimiter_length * 2
            

    def compress(self, string:str):
        string = string.replace(self._raw_delimiter, self._delimiter_replace_string)

        string_length = len(string)
        string_position = 0
        look_ahead = 1
        while string_position < string_length:
            while look_ahead <= self.max_look_ahead:
                look_ahead += 1
            string_position += 1

        self.data.append(string)

    def get_compressed_data(self):
        self.output = " ".join(self.data)
        self.data.clear()
        return self.output
    
    def _get_compression_cost(self, num_patterns):
        pass

    def _will_compression_compress(self, pattern, num_patterns):
        pattern_length = len(pattern)
        return self._get_compression_cost(num_patterns) + pattern_length < pattern_length * num_patterns

    def _get_num_patterns(self, position, pattern_string):
        # num_patterns = 0
        # pattern_string_length = len(pattern_string)
        # if position + pattern_string_length:
        #     pass
        # self.data[position + len(pattern_string)]
        pass
    
    def _update_delimiter_cost(self):
        if self.is_pattern_count_limited:
            self.delimiter_cost = self._delimiter_length * 2
        else:
            self.delimiter_cost = self._delimiter_length * 3

    # Pattern Count Bits property setters and getters
    def _set_pattern_count_num_bits(self, value):
        self._pattern_count_num_bits = value
        if value is not None:
            self.is_pattern_count_limited = True
        else:
            self.is_pattern_count_limited = False
        self._update_delimiter_cost()

    def _get_pattern_count_num_bits(self):
        return self._pattern_count_num_bits

    pattern_count_bits = property(
        fset=_set_pattern_count_num_bits,
        fget=_get_pattern_count_num_bits,
        doc="Pattern Count property in number of bits"
    )

    # Delimiter property setters and getters
    def _set_raw_delimiter(self, value):
        self._raw_delimiter = value
        self._delimiter = value + "1"
        self._delimiter_replace_string = value + "0"
        self._delimiter_length = len(self._delimiter)
        self._update_delimiter_cost()

    def _get_raw_delimiter(self):
        return self._raw_delimiter

    raw_delimiter = property(
        fset=_set_raw_delimiter,
        fget=_get_raw_delimiter,
        doc="Raw delimiter as a string"
    )

if __name__ == "__main__":
    compressor = Pattern_Compressor()
    compressor.compress(" ")
    print(compressor.get_compressed_data())