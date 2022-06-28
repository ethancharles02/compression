# Since 0 will never be an occurrence of a pattern, 0 in binary can be 1
PATTERN_BIT_OFFSET = 1
# How many bits the algorithm looks ahead for patterns
MAX_LOOK_AHEAD = 15
# The basic delimiter, the actual delimiter has a bit added to the end
RAW_DELIMITER = "01011"
PATTERN_COUNT_NUM_BITS = 4
OUT_FILE_EXTENSION = ".lor"