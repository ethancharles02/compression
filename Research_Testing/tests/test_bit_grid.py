import unittest
from sys import path
path.append("..")

from bit_grid import bit_grid

class Test_Bit_Grid(unittest.TestCase):
    def setUp(self) -> None:
        self.fiveByFive = bit_grid(5, 5)
        self.base_grid = [[None for _ in range(5)] for _ in range(5)]
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def test_creates_grid_of_correct_height(self):
        self.assertEqual(self.fiveByFive.grid_height, len(self.fiveByFive.grid))

    def test_creates_grid_of_correct_width(self):
        self.assertEqual(self.fiveByFive.grid_width, len(self.fiveByFive.grid[0]))

    def test_each_row_in_basic_grid_is_same_length(self):
        row_length = self.fiveByFive.grid_width
        for row in self.fiveByFive.grid:
            self.assertEqual(row_length, len(row))

    def test_fill_grid_with_empty_string(self):
        self.fiveByFive.fill_grid_with("")
        self.assertEqual(self.fiveByFive.grid, self.base_grid)

    def test_fill_grid_with_single_char(self):
        _char = "0"
        self.base_grid[0][0] = _char
        self.fiveByFive.fill_grid_with(_char)
        self.assertEqual(self.fiveByFive.grid, self.base_grid)

    def test_fill_row_1_col_1_with_0(self):
        _char = "0"
        self.base_grid[0][0] = _char
        self.fiveByFive.fill_index_with(1,1,_char)
        self.assertEqual(self.fiveByFive.grid, self.base_grid)

    def test_fill_index_1_5_with_0(self):
        _char = "0"
        self.base_grid[4][0] = _char
        self.fiveByFive.fill_index_with(1,5,_char)
        self.assertEqual(self.fiveByFive.grid, self.base_grid)

    def test_fill_grid_with_five_chars(self):
        data = "00000"
        self.base_grid[0] = [_char for _char in data]
        self.fiveByFive.fill_grid_with(data)
        self.assertEqual(self.fiveByFive.grid, self.base_grid)

    def test_fill_grid_with_25_chars(self):
        data = "0"*25
        single_char_grid = [["0" for _ in range(5)] for _ in range(5)]
        self.fiveByFive.fill_grid_with(data)
        self.assertEqual(self.fiveByFive.grid, single_char_grid)

    def test_fill_5_by_5_with_27_chars(self):
        data = "0"*27
        self.assertEqual(self.fiveByFive.fill_grid_with(data), "00")

    def test_get_row(self):
        self.fiveByFive.fill_grid_with("0"*25)
        self.assertEqual(self.fiveByFive.get_row(5), self.fiveByFive.grid[4])

    def test_get_col(self):
        self.fiveByFive.fill_grid_with(("0"*10)+("1"*15))
        self.assertEqual(self.fiveByFive.get_col(5), (["0"]*2)+(['1']*3))


