# TODO
# Add docstrings

class Text_Compressor(object):
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
        new_data = string.split(" ")
        # Prepend the new list of strings onto the old list
        self.data = new_data + self.data
        # Update the reference dictionary indexes to account for the length of the new list
        self._update_dict_ref_indexes(len(new_data))
        
        # Set the index for moving backwards through the new data
        i = len(new_data) - 1
        for item in reversed(new_data):
            if self._item_should_be_referenced(item):
                # If there is a current word in the dictionary, replace old word with a reference
                if item in self.potential_ref_dict:
                    ref_loc = self.potential_ref_dict[item]
                    self._update_data_at(ref_loc, ref_loc - i)
                self._add_item_to_potential_refs(i, item)
            self._clean_potential_refs(i)
            i -= 1

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
        self.potential_ref_dict[value] = index
        self.potential_ref_list.append((index, value))

    def _item_should_be_referenced(self, item):
        return len(item) > self._min_reference_length

    def _update_data_at(self, index:int, ref_dist):
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
        self.output = (" ".join(self.data)).replace(" \n ", "\n")
        self.data.clear()
        self.potential_ref_dict.clear()
        return self.output
        
if __name__ == "__main__":
    compressor = Text_Compressor()
    compressor.compress(" ")
    print(compressor.get_compressed_data())