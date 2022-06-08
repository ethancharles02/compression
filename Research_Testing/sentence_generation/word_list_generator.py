# TODO
# Get sentence grammar from discrete math code
# Create a smaller list for each set of words

from random import *
from sys import *
from math import floor

TEXTSTRING_FOLDER_PATH = "Research_Testing/random_textstring_files"
WORD_DATA_PATH = "Research_Testing/sentence_generation"
FILE_PATTERN = "textstring_%1words_%2lines.txt"

lineNum = 0

punctuation = ['.', '?', '!']

noun = [line.rstrip('\n') for line in open(f'{WORD_DATA_PATH}/nouns.txt')]
adjective = [line.rstrip('\n') for line in open(f'{WORD_DATA_PATH}/adjective.txt')]
verb = [line.rstrip('\n') for line in open(f'{WORD_DATA_PATH}/verb.txt')]
verbSingular = [line.rstrip('\n') for line in open(f'{WORD_DATA_PATH}/verbSingular.txt')]
verbPresent = [line.rstrip('\n') for line in open(f'{WORD_DATA_PATH}/verbPresent.txt')]
verbPast = [line.rstrip('\n') for line in open(f'{WORD_DATA_PATH}/verbPast.txt')]
verbSimplePast = [line.rstrip('\n') for line in open(f'{WORD_DATA_PATH}/verbSimplePast.txt')]
ARTICLES = ["the", "a", "an"]

sentForm = [line.rstrip('\n') for line in open(f'{WORD_DATA_PATH}/sentenceFormats.txt')]

sentFormDict = {}
for line in sentForm:
    sentFormDict[lineNum] = line.split()
    lineNum += 1

def randNoun():
    randomNoun = noun[randint(0, len(noun) - 1)]
    return randomNoun
  
def randVerb():
    randomVerb = verb[randint(0, len(verb) - 1)]
    return randomVerb

def randVerbSingular():
    randomVerbSingular = verbSingular[randint(0, len(verbSingular) - 1)]
    return randomVerbSingular
  
def randVerbPresent():
    randomVerbPresent = verbPresent[randint(0, len(verbPresent) - 1)]
    return randomVerbPresent
  
def randVerbPast():
    randomVerbPast = verbPast[randint(0, len(verbPast) - 1)]
    return randomVerbPast
  
def randVerbSimplePast():
    randomVerbSimplePast = verbSimplePast[randint(0, len(verbSimplePast) - 1)]
    return randomVerbSimplePast
  
def randAdjective():
    randomAdjective = adjective[randint(0, len(adjective) - 1)]
    return randomAdjective

# def randArticle():
#     randomArticle = ARTICLES[randint(0, len(ARTICLES) - 1)]
#     return randomArticle
  
function_list = [randNoun, randVerb, randVerbSingular, randVerbPresent, randVerbPast, randVerbSimplePast, randAdjective]

def randWordFuntion():
    randomFuntion = function_list[randint(0, len(function_list) - 1)]
    return randomFuntion

def create_textstring_file(num_words_per_line, num_lines, percentage_duplicate = 0.5):
    pool_size = floor(num_words_per_line * (1 - percentage_duplicate)) + 1
    pool = [randWordFuntion()() for _ in range(pool_size)] + ARTICLES
    with open(f"{TEXTSTRING_FOLDER_PATH}/{FILE_PATTERN.replace('%1', str(num_words_per_line)).replace('%2', str(num_lines))}", "w") as file:
        for _ in range(num_lines):
            for _ in range(num_words_per_line):
                file.write(choice(pool) + " ")
            file.write("\n")

if __name__ == "__main__":
    create_textstring_file(500, 100000, 0.5)