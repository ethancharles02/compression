
def special_replace(string:str, old:str, new:str="", num_replaces_per_ignore:int=None, num_ignore_characters:int=None) -> str:
    old_string_length = len(old)
    # new_string_length = len(new)
    string_length = len(string)

    new_string_list = []
    last_replace = 0
    
    if num_replaces_per_ignore is not None:
        num_replaces = 0
        num_characters_ignored = 0
        for i in range(len(string) - (old_string_length - 1)):
            if num_replaces == num_replaces_per_ignore:
                num_characters_ignored += 1
                if num_characters_ignored == num_ignore_characters:
                    num_characters_ignored = 0
                    num_replaces = 0

            elif string[i:i+old_string_length] == old:
                new_string_list.append(string[last_replace:i] + new)

                last_replace = i + old_string_length

                num_replaces += 1
    else:
        for i in range(len(string) - (old_string_length - 1)):
            if string[i:i+old_string_length] == old:
                new_string_list.append(string[last_replace:i] + new)

                last_replace = i + old_string_length
    
    new_string_list.append(string[last_replace:string_length])
    
    return "".join(new_string_list)

def special_replace2(string:str, replace_dict:dict) -> str:
    # Gets a list of the replacement strings for checking if a particular part of the string needs to be replaced
    replace_key_list = replace_dict.keys()
    # Gets the length of the longest replacement string
    max_length = max([len(key) for key in replace_key_list])
    string_length = len(string)

    # Creates the empty list for the end string
    new_string_list = []
    last_replace = 0
    ignore_characters = 0

    for i in range(len(string) - (max_length - 1)):
        if ignore_characters > 0:
            ignore_characters -= 1
        else:
            # Creates the string for checking against replacement values
            substring = string[i : i + max_length]
            # Checks the string with each replacement string to see if a replacement can happen
            for key in replace_key_list:
                if substring[:len(key)] == key:
                    if replace_dict[key][1] > 0:
                        count = 0
                        pattern_string = key[replace_dict[key][1]:]
                        pattern_string_length = len(pattern_string)

                        position = i + len(key)
                        while string[position : position + pattern_string_length] == pattern_string:
                            count += 1
                            position += pattern_string_length
                        
                        new_string = replace_dict[key][0] + replace_dict[key][0][replace_dict[key][1]:] * count
                        new_string_list.append(string[last_replace:i] + new_string)
                        last_replace = i + len(key) + len(pattern_string) * count
                        ignore_characters = len(key) + len(pattern_string) * count - 1
                        break
                        
                    else:
                        new_string_list.append(string[last_replace:i] + replace_dict[key][0])
                        last_replace = i + len(key)
                        ignore_characters = len(key)
                        break
    
    new_string_list.append(string[last_replace:string_length])
    
    return "".join(new_string_list)

if __name__ == "__main__":
    # from time import monotonic
    
    # num_duplications = 100000
    # test_string = "10001100 " * num_duplications

    # old_time = monotonic()
    # new_string = special_replace(test_string, "1100", "0110")
    # print(new_string == "10000110 " * num_duplications)
    # print(monotonic() - old_time)

    # old_time = monotonic()
    # new_string = special_replace2(test_string, {"1100" : ["0110", 0, 0]})
    # print(new_string == "10000110 " * num_duplications)
    # print(monotonic() - old_time)

    # old_time = monotonic()
    # new_string = test_string.replace("1100", "0110")
    # print(new_string == "10000110 " * num_duplications)
    # print(monotonic() - old_time)

    # test_string = "10101010"
    # print(special_replace(test_string, "1", "0", 2, 2))
    
    # test_string = "10a10a10a10"
    # replace_dict = {
    #     "10" : ["00", 0, 0],
    #     "a" : ["11", 0, 0]
    # }
    # print(special_replace2(test_string, replace_dict))

    # test_string = "01111"
    # replace_dict = {
    #     "01" : ["232", 1]
    # }
    # new_string = special_replace2(test_string, replace_dict)
    # print(new_string)
    # replace_dict = {
    #     "232" : ["01", 1]
    # }
    # print(special_replace2(new_string, replace_dict))
    replace_dict = {
        "01011" : ["010110", 1]
    }
    print(special_replace2("01110000110001000010101110111011", replace_dict))