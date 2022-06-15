from constants import PATTERN_BIT_OFFSET

class Pattern_Decompressor(object):
    def __init__(self, raw_delimiter:str = "1111", pattern_count_num_bits:int = None, pattern_bit_offset:int = None):
        self._data = []
        self._working_string = ""
        # self._working_string_length = 0

        # Store the raw delimiter along with the version for normal delimiting and for replacing existing raw delimiters
        self._raw_delimiter = raw_delimiter
        self._delimiter = self._raw_delimiter + "1"
        self._delimiter_replace_string = self._raw_delimiter + "0"
        # self._delimiter_length = len(self._delimiter)

        # If a count for patterns is set, there will only need to be two delimiters instead of three for each pattern
        self._pattern_count_num_bits = pattern_count_num_bits

        # Offset for the bits, ie. 1 means that 0 in binary represents a 1 in decimal
        if pattern_bit_offset is None:
            self._pattern_bit_offset = PATTERN_BIT_OFFSET
        else:
            self._pattern_bit_offset = pattern_bit_offset

        self._is_pattern_count_limited = False
        self._max_pattern_count = None
        # self._delimiter_cost = self._delimiter_length * 3

        if self._pattern_count_num_bits is not None:
            self._is_pattern_count_limited = True
            # self._delimiter_cost = self._delimiter_length * 2
            self._max_pattern_count = 2 ** self._pattern_count_num_bits

    def decompress(self, compressed_data):
        data = compressed_data.replace(self._delimiter, "a").replace(self._delimiter_replace_string, self._raw_delimiter).split("a")

        while len(data) > 1:
            self._update_data(data)
        
        if data:
            self._data.append(data[0])


    def get_decompressed_data(self):
        output = "".join(self._data)
        self._data.clear()
        return output

    def _update_data(self, data:list):
        if data[1]:
            if self._is_pattern_count_limited:
                binary_num_patterns = self._get_num_patterns(data[2][:self.pattern_count_num_bits]) + 1
                data[0] = data[0] + data[1] * binary_num_patterns + data[2][self.pattern_count_num_bits:]
            else:
                binary_num_patterns = self._get_num_patterns(data[2]) + 1
                data[0] = data[0] + data[1] * binary_num_patterns
                
            data.pop(1)
            data.pop(1)
        else:
            data.pop(1)
    
    def _get_num_patterns(self, binary_string):
        return int(binary_string, 2) + self._pattern_bit_offset

    # Pattern Count Bits property setters and getters
    def _set_pattern_count_num_bits(self, value):
        self._pattern_count_num_bits = value
        if value is not None:
            self._is_pattern_count_limited = True
            self._max_pattern_count = 2 ** self._pattern_count_num_bits
        else:
            self._is_pattern_count_limited = False
            self._max_pattern_count = None
        # self._update_delimiter_cost()

    def _get_pattern_count_num_bits(self):
        return self._pattern_count_num_bits

    pattern_count_num_bits = property(
        fset=_set_pattern_count_num_bits,
        fget=_get_pattern_count_num_bits,
        doc="Pattern Count property in number of bits"
    )

    # Delimiter property setters and getters
    def _set_raw_delimiter(self, value):
        self._raw_delimiter = value
        self._delimiter = value + "1"
        self._delimiter_replace_string = value + "0"
        # self._delimiter_length = len(self._delimiter)
        # self._update_delimiter_cost()

    def _get_raw_delimiter(self):
        return self._raw_delimiter

    raw_delimiter = property(
        fset=_set_raw_delimiter,
        fget=_get_raw_delimiter,
        doc="Raw delimiter as a string"
    )