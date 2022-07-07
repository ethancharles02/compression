from random import randint

def generate_string(length:int) -> str:
    """ Generates a random bitstring of the specified length

    Arguments:
        length (int): How long the bitstring is
    """
    return "".join([str(randint(0, 1)) for _ in range(length)])

if __name__ == "__main__":
    print(generate_string(25))
