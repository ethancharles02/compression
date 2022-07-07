from src.algorithms.pattern_compression.pattern_constants import PATTERN_BIT_OFFSET

class Pattern_Algorithm_D(object):
    """ The pattern decompressor is used to facilitate decompressing of binary strings
    
    Attributes:

        _data (list): List of compressed strings

        _pattern_count_num_bits (int): Number of bits used for storing the amount of patterns in a compressed string
        _pattern_bit_offset (int): Offset for using bits for counting
        _is_pattern_count_limited (bool): Is there a set length for the bits of a compressed string

        raw_delimiter (str): The delimiter before any changes are made for functionality
        _delimiter (str): Main delimiter
        _delimiter_character (str): The character used at the end of the raw delimiter to denote a delimiter
        _delimiter_replace_string (str): Replacement delimiter for existing delimiter occurrences before compression
        _delimiter_length (int): Length of delimiter
        _replace_delimiter_character (str): Character used for strings that show up in the string that aren't actually delimiters

    Constructor Args:
        raw_delimiter (str): The intended delimiter for separating values. This will not actually be the
            used delimiter since existing occurrences of this in the string will need to be replaced. The actual delimiter is longer

        pattern_count_num_bits (int): The number of bits allocated to saving the length of a pattern
            This defaults to None which will use a dynamic amount of bits to store the pattern count

        pattern_bit_offset (int): The offset from which counting is based on. Since a 0 number of patterns
            will never happen, it is safe to say that 0 in binary is actually 1 in decimal
    
    Class Methods:
        __init__(): Initializes the parent class, assigns attributes

        decompress() -> None: Main function for decompressing data
        get_decompressed_data -> str: Returns all decompressed data as a binary string
        _update_data -> None: Decompresses one instance of data. The 0th index is the main string while everything after is some separated string and pattern count
        _get_num_patterns() -> int: Returns the number of patterns from a binary string representing a number 
        _update_delimiter_characters() -> None: Checks the front of the raw delimiter to figure out what the delimiter characters are, updating them
        _update_pattern_count_limited() -> None: Updates the attribute for if the pattern count is limited or not
        _set_pattern_count_num_bits() -> None: Setter for the attribute
        _get_pattern_count_num_bits() -> int: Getter for the attribute
        _set_raw_delimiter() -> None: Setter for the attribute
        _get_raw_delimiter() -> str: Getter for the attribute
    """
    def __init__(self, raw_delimiter:str = "1111", pattern_count_num_bits:int = None, pattern_bit_offset:int = None):
        """
        Constructor Args:
            raw_delimiter (str): The intended delimiter for separating values. This will not actually be the
                used delimiter since existing occurrences of this in the string will need to be replaced. The actual delimiter is longer

            pattern_count_num_bits (int): The number of bits allocated to saving the length of a pattern
                This defaults to None which will use a dynamic amount of bits to store the pattern count

            pattern_bit_offset (int): The offset from which counting is based on. Since a 0 number of patterns
                will never happen, it is safe to say that 0 in binary is actually 1 in decimal
        """
        self._data = []

        # Store the raw delimiter along with the version for normal delimiting and for replacing existing raw delimiters
        self._raw_delimiter = raw_delimiter
        self._delimiter_character = None
        self._replace_delimiter_character = None

        self._update_delimiter_characters()

        self._delimiter = self._raw_delimiter + self._delimiter_character
        self._delimiter_replace_string = self._raw_delimiter + self._replace_delimiter_character
        self._delimiter_length = len(self._delimiter)

        # If a count for patterns is set, there will only need to be two delimiters instead of three for each pattern
        self._pattern_count_num_bits = pattern_count_num_bits

        # Offset for the bits, ie. 1 means that 0 in binary represents a 1 in decimal
        if pattern_bit_offset is None:
            self._pattern_bit_offset = PATTERN_BIT_OFFSET
        else:
            self._pattern_bit_offset = pattern_bit_offset

        self._is_pattern_count_limited = None
        self._update_pattern_count_limited()

    def decompress(self, compressed_data:str):
        """ Decompresses a string using the pattern decompression algorithm

        Arguments:
            compressed_data (str): The string to be compressed
        """
        data = compressed_data.replace(self._delimiter_replace_string, "b").replace(self._delimiter, "a").replace("b", self._raw_delimiter).split("a")
        
        while len(data) > 1:
            self._update_data(data)
        
        if data:
            self._data.append(data[0])


    def get_decompressed_data(self) -> str:
        """ Returns all decompressed data as a binary string
        """
        output = "".join(self._data)
        self._data.clear()
        return output

    def _update_data(self, data:list):
        """ Decompresses one instance of data. The 0th index is the main string while everything after is some separated string and pattern count

        Arguments:
            data (list): Data in the format of [working string, pattern_string1, pattern_count1, ... , pattern_string_n, pattern_count_n, filler_zeroes (optional)]
        """
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
    
    def _get_num_patterns(self, binary_string:str) -> int:
        """ Returns the number of patterns from a binary string representing a number

        Arguments:
            binary_string (str): Binary string representing a number
        """
        return int(binary_string, 2) + self._pattern_bit_offset

    def _update_delimiter_characters(self):
        """ Checks the front of the raw delimiter to figure out what the delimiter characters are, updating them
        """
        if self._raw_delimiter[0] == "0":
            self._delimiter_character = "1"
            self._replace_delimiter_character = "0"
        elif self._raw_delimiter[0] == "1":
            self._delimiter_character = "0"
            self._replace_delimiter_character = "1"

    def _update_pattern_count_limited(self):
        """ Updates the attribute for if the pattern count is limited or not
        """
        if self._pattern_count_num_bits is not None:
            self._is_pattern_count_limited = True
        else:
            self._is_pattern_count_limited = False

    # Pattern Count Bits property setters and getters
    def _set_pattern_count_num_bits(self, value:int):
        """ Setter for the attribute

        Arguments:
            value (int): Value to update the pattern_count_num_bits with
        """
        self._pattern_count_num_bits = value
        self._update_pattern_count_limited()

    def _get_pattern_count_num_bits(self):
        """ Getter for the attribute
        """
        return self._pattern_count_num_bits

    pattern_count_num_bits = property(
        fset=_set_pattern_count_num_bits,
        fget=_get_pattern_count_num_bits,
        doc="Pattern Count property in number of bits"
    )

    # Delimiter property setters and getters
    def _set_raw_delimiter(self, value:str):
        """ Setter for the attribute

        Arguments:
            value (str): Value to update the raw delimiter with
        """
        self._raw_delimiter = value

        self._update_delimiter_characters()

        self._delimiter = value + self._delimiter_character
        self._delimiter_replace_string = value + self._replace_delimiter_character
        self._delimiter_length = len(self._delimiter)

    def _get_raw_delimiter(self):
        """ Getter for the attribute
        """
        return self._raw_delimiter

    raw_delimiter = property(
        fset=_set_raw_delimiter,
        fget=_get_raw_delimiter,
        doc="Raw delimiter as a string"
    )