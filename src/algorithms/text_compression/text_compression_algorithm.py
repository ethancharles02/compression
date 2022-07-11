# TODO
# Add docstrings

class Text_Compression_Algorithm(object):
    def __init__(self, look_ahead:int):
        self._look_ahead = look_ahead
        self._update_min_ref_length()
        self.data = []
        self.potential_ref_dict = {}
        self.potential_ref_list = []

    def compress(self, string:str):
        """
        Input:  String
        Output: None
        Description:
        Updates class variable "data" with the input string separated by 
        spaces. Attempts to compress each word in the new data gotten 
        from the input string. Updates the class variables 'potetial_ref_dict'
        and 'potential_ref_list'
        """
        # Add escape characters and separate endlines
        string = string.replace("<","~<").replace("\n", " \n ")
        # Split the string into a list
        self.new_data = string.split(" ")
        self.num_old_data = len(self.data)
        # Prepend the new list of strings onto the old list
        self.data += self.new_data
        # Set the index for moving backwards through the new data
        data_index = len(self.data) - 1
        for new_data_index in range(len(self.new_data)):
            self.compress_word(self.num_old_data + new_data_index)
            self._clean_potential_refs(data_index)
            data_index -= 1
        # Remove extra space at the end of data
        if len(self.data) > 1 and self.data[-1] == '' and self.data[-2] == '\n':
            self.data.pop()

    def compress_word(self, data_index):
        """
        Input:  index of item in class variable "data"
        Output: None
        Description:
        Check if the word could be a reference. Check if the 
        possible reference is close enough. If it passes the 
        checks, replace it with a reference. Update the 
        potential reference class variables.
        """
        word = self.data[data_index]
        if self._item_is_big_enough_to_be_referenced(word):
                # If there is a current word in the dictionary, replace old word with a reference
            if word in self.potential_ref_dict.keys():
                (ref_loc, org_value) = self.potential_ref_dict[word]
                ref_dist = data_index - ref_loc
                if ref_dist <= self._look_ahead:
                    self._update_data_piece_to_reference_at(data_index, ref_dist)
                self._add_item_to_potential_refs(data_index, org_value)
            else:
                self._add_item_to_potential_refs(data_index, word)

    def _item_is_reference(self, word:str):
        """
        Input:  String
        Output: Boolean
        Description:
        Check if the word has the '<' reference character in it
        and that it doesn't have the '~' escape character as well,
        meaning the word is reference.
        """
        return "<" in word and "~" not in word

    def _update_min_ref_length(self):
        """
        Description:
        Updates the min_refernce_length which is the smallest length a word
        could be for it to be worth referencing. The log of the look_ahead 
        plus one is this length.
        """
        self._min_reference_length = len(str(self._look_ahead)) + 1

    def _clean_potential_refs(self, curr_index):
        """
        Input:  Index:Integer
        Output: None
        Description:
        Checks to see if the difference between the index passed in
        and the index of the first item in the potential reference list
        is greater than the look_ahead value. If so, remove the first value
        from the potential reference dictionary and list.
        """
        if self.potential_ref_list:
            old_index, old_value = self.potential_ref_list[0]
            if old_index - curr_index >= self.look_ahead:
                if self.potential_ref_dict[old_value] == old_index:
                    self.potential_ref_dict.pop(old_value)
                self.potential_ref_list.pop(0)

    def _add_item_to_potential_refs(self, index, value):
        self.potential_ref_dict[value] = (index, value)
        self.potential_ref_list.append((index, value))

    def _item_is_big_enough_to_be_referenced(self, item):
        """
        Input:  item:str
        Output: Boolean
        Description:
        Is the length of the item longer than the minimum
        reference length? If so, then the item is big enough.
        If not, then the item is not big enough.
        """
        return len(item) > self._min_reference_length

    def _update_data_piece_to_reference_at(self, index:int, ref_dist):
        """
        input:  index:int, ref_dist
        output: None
        Description:
        Update the item in the class variable "data" at the index passed in
        to be a reference of the distance ref_dist.
        """
        self.data[index] = f"<{ref_dist}" 
    
    def _get_look_ahead(self):
        return self._look_ahead
        
    def _set_look_ahead(self, value):
        self._look_ahead = value
        self._update_min_ref_length()

    look_ahead = property(
        fget=_get_look_ahead,
        fset=_set_look_ahead,
        doc="Look Ahead Property"
    )

    def get_compressed_data(self):
        """
        input:  None
        output: output:str
        Description:
        prepare data to be combined. Combile all the items in data 
        into one string. Remove the extra spaces before and after
        newlines. Clear the class variables data, potential_ref_list and potential_ref_dict 
        """
        if self.data[-1] == '\n':
            self.data.append('')
        output = (" ".join(self.data)).replace(" \n ", "\n")
        self.data.clear()
        self.potential_ref_dict.clear()
        self.potential_ref_list.clear()
        return output
