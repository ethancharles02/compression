# TODO
# Finish docstrings, add types as necessary to methods
# Reduce look ahead in the main loop if it is near the end of the string

from math import log2, floor

from sys import path
path.append("Research_Testing")
from constants import PATTERN_BIT_OFFSET

class Pattern_Compressor(object):
    """
    The pattern compressor is used to facilitate compressing of binary strings.
    Once the compression happens, any raw delimiters that exist are replaced with the corresponding delimiter string that won't mess with the delimiter.
    Compression only happens if bits will be saved in the process, it will place a delimiter before the pattern and one after to indicate that it is the pattern.
    After that second delimiter, a number of bits will indicate how many times the pattern occurs. If the number of bits isn't set, a third delimiter will exist at the end of the number to indicate this

    Attributes:
        pattern_count_num_bits (int): Number of bits used for storing the amount of patterns in a compressed string
        raw_delimiter (str): The delimiter before any changes are made for functionality

        _data (list): List of compressed strings
        _working_string (str): Current string being compressed
        _working_string_length (int): Length of current string
        _max_look_ahead (int): Maximum value for looking ahead in the bit string
        _is_pattern_count_limited (bool): Is there a set length for the bits of a compressed string
        _delimiter_cost (int): Cost of compressing a value excluding the count of bits used for the pattern count
        _pattern_count_num_bits (int): Same as public
        _raw_delimiter (str): Same as public
        _pattern_bit_offset (int): Offset for using bits for counting
        _delimiter (str): Main delimiter
        _delimiter_replace_string (str): Replacement delimiter for existing delimiter occurrences before compression
        _delimiter_length (int): Length of delimiter

    Constructor Args:
        max_look_ahead (int): How far ahead the compressor will look for patterns
            ie. a string of "101101" will see the pattern of "101" with a minimum of 3 look_ahead

        raw_delimiter (str): The intended delimiter for separating values. This will not actually be the
            used delimiter since existing occurrences of this in the string will need to be replaced. The actual delimiter is longer

        pattern_count_num_bits (int): The number of bits allocated to saving the length of a pattern
            This defaults to None which will use a dynamic amount of bits to store the pattern count

        pattern_bit_offset (int): The offset from which counting is based on. Since a 0 number of patterns
            will never happen, it is safe to say that 0 in binary is actually 1 in decimal
    
    Class Methods:
        __init__(): Initializes the parent class, assigns attributes

        compress() -> None: Main function for compressing data

        get_compressed_data() -> str: Returns all compressed data as a binary string

        _get_compression_cost() -> int: Returns the cost for a compression based on a number of patterns

        _get_binary_length_of_dec_number() -> int: Returns the length of a decimal number in binary based on an offset

        _convert_to_binary() -> str: Returns a decimal number converted to binary

        _will_compression_compress() -> bool: Returns a boolean of whether or not a particular compression will actually save space

        _get_num_patterns() -> int: Returns the number of patterns excluding the initial pattern that occur sequentially 

        _get_pattern_binary_string() -> str: Returns the string for the portion of a compression that uses the count of patterns.
            This includes the delimiter at the end only if the pattern bit counts are dynamic

        _compress_string_patterns() -> None: Compress a portion of the working string attribute

        _update_delimiter_cost() -> None: Updates the delimiter cost attribute. Used for whenever the delimiter changes or
            when the pattern count type changes 

        _set_pattern_count_num_bits() -> None: Setter for the attribute

        _get_pattern_count_num_bits() -> int: Getter for the attribute

        _set_raw_delimiter() -> None: Setter for the attribute

        _get_raw_delimiter() -> str: Getter for the attribute

    """
    def __init__(self, max_look_ahead:int, raw_delimiter:str = "11111", pattern_count_num_bits:int = None, pattern_bit_offset:int = None):
        """
        Constructor Args:
            max_look_ahead (int): How far ahead the compressor will look for patterns
                ie. a string of "101101" will see the pattern of "101" with a minimum of 3 look_ahead

            raw_delimiter (str): The intended delimiter for separating values. This will not actually be the
                used delimiter since existing occurrences of this in the string will need to be replaced. The actual delimiter is longer

            pattern_count_num_bits (int): The number of bits allocated to saving the length of a pattern
                This defaults to None which will use a dynamic amount of bits to store the pattern count

            pattern_bit_offset (int): The offset from which counting is based on. Since a 0 number of patterns
                will never happen, it is safe to say that 0 in binary is actually 1 in decimal
        """
        self._data = []
        self._working_string = ""
        self._working_string_length = 0
        self._max_look_ahead = max_look_ahead

        # Store the raw delimiter along with the version for normal delimiting and for replacing existing raw delimiters
        self._raw_delimiter = raw_delimiter
        self._delimiter = self._raw_delimiter + "1"
        self._delimiter_replace_string = self._raw_delimiter + "0"
        self._delimiter_length = len(self._delimiter)

        # If a count for patterns is set, there will only need to be two delimiters instead of three for each pattern
        self._pattern_count_num_bits = pattern_count_num_bits

        # Offset for the bits, ie. 1 means that 0 in binary represents a 1 in decimal
        if pattern_bit_offset is None:
            self._pattern_bit_offset = PATTERN_BIT_OFFSET
        else:
            self._pattern_bit_offset = pattern_bit_offset

        self._is_pattern_count_limited = False
        self._delimiter_cost = self._delimiter_length * 3

        if self._pattern_count_num_bits is not None:
            self._is_pattern_count_limited = True
            self._delimiter_cost = self._delimiter_length * 2
            

    def compress(self, string:str):
        self._working_string = string.replace(self._raw_delimiter, self._delimiter_replace_string)

        # Update string length as necessary whenever it gets changed
        self._working_string_length = len(self._working_string)
        string_position = 0
        look_ahead = self._max_look_ahead
        while string_position < self._working_string_length:
            while look_ahead > 0:
                string_slice = self._working_string[string_position : string_position + look_ahead]
                number_of_patterns = self._get_num_patterns(string_position, string_slice)
                if number_of_patterns >= 1:
                    if self._will_compression_compress(string_slice, number_of_patterns):
                        self._compress_string_patterns(string_position, string_slice, number_of_patterns)
                look_ahead -= 1
            string_position += 1
            look_ahead = self._max_look_ahead

        self._data.append(self._working_string)

    def get_compressed_data(self):
        self.output = " ".join(self._data)
        self._data.clear()
        return self.output
    
    def _get_compression_cost(self, num_patterns):
        if self._is_pattern_count_limited:
            return self._delimiter_cost + self.pattern_count_num_bits
        else:
            return self._delimiter_cost + self._get_binary_length_of_dec_number(num_patterns)

    def _get_binary_length_of_dec_number(self, number):
        number -= self._pattern_bit_offset
        if number <= 0:
            return 1
        else:
            return floor(log2(number) + 1)

    def _convert_to_binary(self, num) -> str:
        return str(bin(num - self._pattern_bit_offset))[2:]

    def _will_compression_compress(self, pattern, num_patterns):
        pattern_length = len(pattern)
        return self._get_compression_cost(num_patterns) + pattern_length < pattern_length * (num_patterns + 1)

    # Ignores the first occurence of the pattern, assuming it is already there
    def _get_num_patterns(self, position, pattern_string):
        count = 0
        pattern_string_length = len(pattern_string)
        while self._working_string[position + pattern_string_length : position + pattern_string_length*2] == pattern_string:
            count += 1
            position += pattern_string_length
        
        return count
    
    def _get_pattern_binary_string(self, num_patterns:int) -> str:
        if self._is_pattern_count_limited:
            binary_string = self._convert_to_binary(num_patterns)
            return "0" * (self._pattern_count_num_bits - len(binary_string)) + binary_string
        else:
            return self._convert_to_binary(num_patterns) + self._delimiter

    def _compress_string_patterns(self, position, pattern_string, num_patterns):
        pattern_string_length = len(pattern_string)
        self._working_string =   self._working_string[:position] +\
                                self._delimiter + pattern_string + self._delimiter + self._get_pattern_binary_string(num_patterns)+\
                                self._working_string[position + pattern_string_length * (num_patterns + 1):]
        self._working_string_length = len(self._working_string)

    def _update_delimiter_cost(self):
        if self._is_pattern_count_limited:
            self._delimiter_cost = self._delimiter_length * 2
        else:
            self._delimiter_cost = self._delimiter_length * 3

    # Pattern Count Bits property setters and getters
    def _set_pattern_count_num_bits(self, value):
        self._pattern_count_num_bits = value
        if value is not None:
            self._is_pattern_count_limited = True
        else:
            self._is_pattern_count_limited = False
        self._update_delimiter_cost()

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
    compressor = Pattern_Compressor(max_look_ahead = 15, raw_delimiter = "111", pattern_count_num_bits = 3)
    # compressor.working_string = "00011111000"
    # compressor.compress("100110001001100110001001")
    # print(compressor.get_compressed_data())
    # print(compressor.get_compressed_data())
    # compressor._replace_string_patterns(3, "1", 4)
    # print(compressor.working_string)