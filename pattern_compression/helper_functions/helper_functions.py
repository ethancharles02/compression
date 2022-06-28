
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

if __name__ == "__main__":
    from time import monotonic
    
    num_duplications = 100000
    test_string = "10001100 " * num_duplications

    old_time = monotonic()
    new_string = special_replace(test_string, "1100", "0110")
    print(new_string == "10000110 " * num_duplications)
    print(monotonic() - old_time)

    old_time = monotonic()
    new_string = test_string.replace("1100", "0110")
    print(new_string == "10000110 " * num_duplications)
    print(monotonic() - old_time)

    # test_string = "10101010"
    # print(special_replace(test_string, "1", "0", 2, 2))
