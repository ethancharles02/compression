# TODO
# Get sentence grammar from discrete math code
# Create a smaller list for each set of words

from random import *
from sys import *
from math import floor

TEXTSTRING_FOLDER_PATH = "../random_textstring_files"
FILE_PATTERN = "textstring_%1words_%2lines.txt"

lineNum = 0

punctuation = ['.', '?', '!']

noun = [line.rstrip('\n') for line in open('nouns.txt')]
adjective = [line.rstrip('\n') for line in open('adjective.txt')]
verb = [line.rstrip('\n') for line in open('verb.txt')]
verbSingular = [line.rstrip('\n') for line in open('verbSingular.txt')]
verbPresent = [line.rstrip('\n') for line in open('verbPresent.txt')]
verbPast = [line.rstrip('\n') for line in open('verbPast.txt')]
verbSimplePast = [line.rstrip('\n') for line in open('verbSimplePast.txt')]
ARTICLES = ["the", "a", "an"]

sentForm = [line.rstrip('\n') for line in open('sentenceFormats.txt')]

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
    create_textstring_file(5, 10, 0.5)
    # pool_size = 15
    # pool = []
    # for function in function_list:
    #     for _ in range(pool_size):
    #         pool.append(function())
    
    
    # pool = [randWordFuntion()() for _ in range(pool_size)] + ARTICLES

    # pool = pool + ARTICLES
    
    # pools = [[function() for _ in range(pool_size)] + ARTICLES for function in function_list]
    # print(pools)
    # print(pool)
    # sentence_length = 10
    # print(" ".join([choice(function_list)() for _ in range(sentence_length)]))
    
# if False:
#   for i in range(10):
#     stdout.write(noun[randint(0, len(noun) - 1)] + ' ')
    
# #for word in sentFormats:
#   #stdout.write
# for i in range(1):
#   chosenSentForm = sentFormDict[randint(0, len(sentFormDict) - 1)]
#   newSentence = []
  
#   #print(sentFormDict)
#   for word in chosenSentForm:
#     if 'noun' in word:
#       newSentence.append(randNoun())
      
#     elif 'verb' in word:
#       newSentence.append(randVerb())
        
#     elif 'verbSingular' in word:
#       newSentence.append(randVerbSingular())
      
#     elif 'verbPresent' in word:
#       newSentence.append(randVerbPresent())
      
#     elif 'verbPast' in word:
#       newSentence.append(randVerbPast())
      
#     elif 'verbSimplePast' in word:
#       newSentence.append(randVerbSimplePast())
      
#     elif 'adjective' in word:
#       newSentence.append(randAdjective())
      
#     else:
#       newSentence.append(word)
      
#   i = 0
  
#   for word in newSentence:
#     if i == 0:
#       newSentence[0] = newSentence[0].capitalize()
#     if i == len(newSentence) - 1:
#       newSentence[i] = newSentence[i] + punctuation[randint(0, len(punctuation) - 1)]
#     if word == 'a' or word == 'an':
#       if newSentence[i + 1][0] == 'a' or newSentence[i + 1][0] == 'e' or newSentence[i + 1][0] == 'i' or newSentence[i + 1][0] == 'o' or newSentence[i + 1][0] == 'u':
#         newSentence[i] = 'an'
#       else:
#         newSentence[i] = 'a'
#     if word == 'A' or word == 'An':
#       if newSentence[i + 1][0] == 'a' or newSentence[i + 1][0] == 'e' or newSentence[i + 1][0] == 'i' or newSentence[i + 1][0] == 'o' or newSentence[i + 1][0] == 'u':
#         newSentence[i] = 'An'
#       else:
#         newSentence[i] = 'A'
#     if word == 's':
#       if newSentence[i - 1][len(newSentence[i - 1]) - 1] == 'y':
#         newSentence[i - 1] = list(newSentence[i - 1])
#         newSentence[i - 1][len(newSentence[i - 1]) - 1] = 'ie'
#         newSentence[i - 1] = ''.join(newSentence[i - 1])
#         newSentence[i - 1] = newSentence[i - 1] + 's'
#       else:
#         newSentence[i - 1] = newSentence[i - 1] + 's'
#       del newSentence[i]
#     elif word == "'s":
#       if newSentence[i - 1][len(newSentence[i - 1]) - 1] == 'y':
#         newSentence[i - 1] = list(newSentence[i - 1])
#         newSentence[i - 1][len(newSentence[i - 1]) - 1] = 'ie'
#         newSentence[i - 1] = ''.join(newSentence[i - 1])
#         newSentence[i - 1] = newSentence[i - 1] + "'s"
#       else:
#         newSentence[i - 1] = newSentence[i - 1] + "'s"
#       del newSentence[i]
#     else:
#       i += 1
    
#   for word in newSentence:
#     stdout.write(word + ' ')