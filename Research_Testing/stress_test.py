from time import monotonic
from random import randint

if __name__ == "__main__":
    # test_list = [randint(0, 1000) for _ in range(1000000)]

    old_time = monotonic()
    print([1, 2, 3] + [4, 5, 6])
    # print(type(reversed(test_list)))
    print(monotonic() - old_time)