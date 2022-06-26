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
        # Add escape characters
        string = string.replace("<","~<").replace("\n", " \n ")
        # Split the string into a list
        self.new_data = string.split(" ")
        self.num_old_data = len(self.data)
        # Prepend the new list of strings onto the old list
        self.data += self.new_data
        # Update the reference dictionary indexes to account for the length of the new list
        # self._update_dict_ref_indexes(len(self.new_data))
        
        # Set the index for moving backwards through the new data
        data_index = len(self.data) - 1
        for new_data_index in range(len(self.new_data)):
            self.compress_word(self.num_old_data + new_data_index)
            self._clean_potential_refs(data_index)
            data_index -= 1
        if self.data[-1] == '' and self.data[0] != '':
            self.data.pop()

    def compress_word(self, data_index):
        if self._item_is_big_enough_to_be_referenced(self.data[data_index]):
                # If there is a current word in the dictionary, replace old word with a reference
            if self.data[data_index] in self.potential_ref_dict.keys():
                (ref_loc, org_value) = self.potential_ref_dict[self.data[data_index]]
                ref_dist = data_index - ref_loc
                if ref_dist <= self._look_ahead:
                    self._update_data_piece_to_reference_at(data_index, ref_dist)
                self._add_item_to_potential_refs(data_index, org_value)
            else:
                self._add_item_to_potential_refs(data_index, self.data[data_index])

    def _item_is_reference(self, item):
        return "<" in item and "~" not in item

    def _update_min_ref_length(self):
        self._min_reference_length = len(str(self._look_ahead)) + 1

    def _clean_potential_refs(self, curr_index):
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
        return len(item) > self._min_reference_length

    def _update_data_piece_to_reference_at(self, index:int, ref_dist):
        self.data[index] = f"<{ref_dist}" 

    def _update_dict_ref_indexes(self, num:int):
        for item in self.potential_ref_dict.keys():
            self.potential_ref_dict[item] += num
    
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
        if self.data[-1] == '\n':
            self.data.append('')
        output = (" ".join(self.data)).replace(" \n ", "\n")
        self.data.clear()
        self.potential_ref_dict.clear()
        return output
        
# if __name__ == "__main__":
#     compressor = Text_Compressor()
#     compressor.compress(" ")
#     print(compressor.get_compressed_data())