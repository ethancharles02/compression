# TODO
# Count number of row b delimiters until it == num_rows then switch to columns
# Finish compressibility by inverting the rating (subtract the value from the max compressibility size) and multiple the two ratings together?
# Add tests for all functions
# Maybe add a mode that doesn't have symbol specifiers at the start of each column or row (default to 1). See if it changes much

from bit_string_generator import generate_string
from constants import *
from math import floor, ceil, log2
from bit_grid import bit_grid

# NUM_COLUMNS = 16
# NUM_ROWS = 64
NUM_COLUMNS = 5
NUM_ROWS = 5

class bit_grid_compressor:
    def __init__(self, bit_string:str, num_columns:int, num_rows:int):
        # bits = self.create_bit_string(bit_string)
        if num_columns > 0:
            self.num_columns = num_columns
        else:
            raise(ValueError("Row length must be greater than zero!"))
        
        if num_rows > 0:
            self.num_rows = num_rows
        else:
            raise(ValueError("Column height must be greater than zero!"))

        self.grid = bit_grid(self.num_rows, self.num_columns)

        if self.grid.grid_area > len(bit_string):
            raise(ValueError(f"Grid must not be larger than the number of bits. Bits given was {len(bit_string)} while the size of the grid was {self.grid.grid_area}"))

        # Initialize bit list
        # self.grid = self._create_grid(bit_string)
        leftover_bits = self.grid.fill_grid_with(bit_string)
        if leftover_bits != None:
            raise Exception("There were too many bits")

        # Create delimiters for rows and columns
        self._row_a_delimiter = "0" * self.get_num_bin_bits_for_dec(self.num_columns) + "10"
        self._row_b_delimiter = "0" * self.get_num_bin_bits_for_dec(self.num_columns) + "11"
        self._row_a_delimiter_length = len(self._row_a_delimiter)
        # self._row_b_delimiter_length = len(self._row_b_delimiter)

        self._column_a_delimiter = "0" * self.get_num_bin_bits_for_dec(self.num_rows) + "10"
        self._column_b_delimiter = "0" * self.get_num_bin_bits_for_dec(self.num_rows) + "11"
        self._column_a_delimiter_length = len(self._column_a_delimiter)
        

        # Find the maximum numbers of countable symbols in a row or column
        self._max_row_individual_bits = ceil(self.num_columns / 2)
        self._max_column_individual_bits = ceil(self.num_rows / 2)

        # Find the worst case scenario for compression in number of bits
        self._max_row_compression_size = self._max_row_individual_bits + (self._max_row_individual_bits - 1) * self._row_a_delimiter_length
        self._max_column_compression_size = self._max_column_individual_bits + (self._max_column_individual_bits - 1) * self._column_a_delimiter_length

    def convert_to_binary(self, num, offset=0) -> str:
        return str(bin(num - offset))[2:]

    def get_num_bin_bits_for_dec(self, num):
        return floor(log2(num)+1)

    def compress(self) -> str:
        """
        compress will use the grid attribute to return compressed bits
        """
        # Converting rows and columns to their condensed numbers in binary
        rows = []
        for y in range(self.num_rows):
            data, num_list = self._get_row_nums(y)
            rows.append((data, [self.convert_to_binary(number) for number in num_list]))

        columns = []
        for x in range(self.num_columns):
            data, num_list = self._get_column_nums(x)
            columns.append((data, [self.convert_to_binary(number) for number in num_list]))
        
        # Columns and rows with the delimited a's between numbers
        compressed_rows_list = [self._row_a_delimiter.join(row[1]) for row in rows]
        for i in range(len(compressed_rows_list)):
            compressed_rows_list[i] = rows[i][0] + compressed_rows_list[i]
            
        compressed_columns_list = [self._column_a_delimiter.join(column[1]) for column in columns]
        for i in range(len(compressed_columns_list)):
            compressed_columns_list[i] = columns[i][0] + compressed_columns_list[i]
        

        # Columns and rows with the delimited b's between columns/rows
        compressed_row_string = self._row_b_delimiter.join(compressed_rows_list)
        compressed_column_string = self._column_b_delimiter.join(compressed_columns_list)
        
        # Dedicates 16 bytes to indicate the number of columns and rows
        # Errors if there are too many rows or columns
        binary_length_string = str(bin(self.num_rows)[2:])
        if len(binary_length_string) > DEDICATED_ROW_SPACE:
            raise Exception("Too many rows in the grid")
        binary_length_string = "0"*(DEDICATED_ROW_SPACE - len(binary_length_string)) + binary_length_string

        binary_height_string = str(bin(self.num_columns)[2:])
        if len(binary_height_string) > DEDICATED_COLUMN_SPACE:
            raise Exception("Too many columns in the grid")
        binary_height_string = "0"*(DEDICATED_COLUMN_SPACE - len(binary_height_string)) + binary_height_string

        length_height_string = binary_length_string + binary_height_string

        # Adds the c between the column section and the row section
        bit_string = length_height_string + compressed_row_string + self._row_b_delimiter + compressed_column_string + self._column_b_delimiter

        return bit_string

    def _create_grid(self, bits:str) -> list:
        grid = []
        for y in range(self.num_rows):
            grid.append([])
            for x in range(self.num_columns):
                grid[y].append(bits[y * self.num_columns + x])
        return grid

    def _get_row_nums(self, row_num:int, symbol:str="1") -> tuple:
        return (symbol, self._get_symbol_counts(self.grid.get_row(row_num), symbol))

    def _get_column_nums(self, column_num, symbol="1") -> tuple:
        bit_list = self.grid.get_col(column_num)
        return (symbol, self._get_symbol_counts(bit_list, symbol))

    def _get_symbol_counts(self, iterable, symbol="1", type_conversion=str) -> list:
        num_list = []

        # Initialize variable for counting the number of bits found in a row
        consec_bit_count = 0
        for bit in iterable:
            if bit == symbol:
                consec_bit_count += 1
            elif consec_bit_count > 0:
                num_list.append(consec_bit_count)
                consec_bit_count = 0
        
        if consec_bit_count > 0:
            num_list.append(consec_bit_count)

        return num_list

    def _rate_decompressibility(self, row_or_column_nums:list, is_row:bool = True) -> int:
        part_1 = sum(row_or_column_nums) + len(row_or_column_nums) - 1
        part_2 = part_1 / (self.num_columns if is_row else self.num_rows)

        print(part_2)
        return part_2

    def _rate_compressibility(self, row_or_column_nums:list, is_row) -> int:
        part_1 = (self._row_a_delimiter_length if is_row else self._column_a_delimiter_length) * (len(row_or_column_nums) - 1)
        print(row_or_column_nums)
        part_2 = sum([self.get_num_bin_bits_for_dec(num) for num in row_or_column_nums])
        final_length = part_1 + part_2

        print(final_length)
        return final_length


    def _get_optimal_count_symbol(self, row_or_column:list, is_row:bool = True) -> str:
        one_symbol_counts = self._get_symbol_counts(row_or_column, "1", int)
        one_rating = self._rate_compressibility(one_symbol_counts, is_row) +\
                     self._rate_decompressibility(one_symbol_counts, is_row)

        zero_symbol_counts = self._get_symbol_counts(row_or_column, "0", int)
        zero_rating = self._rate_compressibility(zero_symbol_counts, is_row) +\
                      self._rate_decompressibility(zero_symbol_counts, is_row)

        # zero_rating = self._rate_compressibility(row_or_column)
        # one_rating = self._rate_compressibility(row_or_column)
        
        return "0" if zero_rating > one_rating else "1"

if __name__ == "__main__":
    # with open("Research_Testing/random_string_files/random_bit_strings_1.txt") as f:
    with open("random_string_files/random_bit_strings_1.txt") as f:
        bitlist = f.read(25)
    
    grid_compressor = bit_grid_compressor(bitlist, NUM_COLUMNS, NUM_ROWS)

    grid_compressor.grid.print_grid()
    print(grid_compressor.compress())
    print(grid_compressor._get_optimal_count_symbol(grid_compressor.grid.get_col(0), False))
    # grid._rate_compressibility()
    # grid._rate_decompressibility()