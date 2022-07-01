from random import randint

def generate_string(length):
    return "".join([str(randint(0, 1)) for _ in range(length)])

if __name__ == "__main__":
    print(generate_string(25))
