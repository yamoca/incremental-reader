import re
import time
from thefuzz import fuzz
# from typing import List


print("Welcome to Incremental Reader")

with open("english.txt") as f:
    english = f.read()

with open("latin.txt") as g:
    latin = g.read()


class Passage:
    def __init__(self, paragraphs, title):
        self.paragraphs = paragraphs 
        self.title = title 

class Paragraph:
    def __init__(self, clauses): # include position in passage?
        self.clauses = clauses 

class Clause:
    def __init__(self, latin, english):
        self.latin = latin
        self.english = english
        self._avgAccuracy = 0 #use a "hidden variable" so the settr doesnt recursively call itself
        self.attempts = 0
        self.level = "New" 
    
    @property
    def avgAccuracy(self):
        return self._avgAccuracy

    @avgAccuracy.setter
    def avgAccuracy(self, value):
        self._avgAccuracy = value
        self.updateLevel()
    
    def updateLevel(self):
        if self.avgAccuracy < 30:
            self.level = "New"
        elif self.avgAccuracy < 50:
            self.level = "Fresh"
        elif self.avgAccuracy < 70:
            self.level = "Learning" 
        elif self.avgAccuracy < 90:
            self.level = "Good" 
        else:
            self.level = "Mastered"




'''
0 - 30 new
30 - 50 fresh
50 - 70 learning
70 - 90 good
90+ master
'''

# example hardcoded passage
testPassage = Passage(
    title="test",
    paragraphs=[
        Paragraph(clauses=[
            Clause(
                latin="lorem ipsum dolor sit amet",
                english="the quick brown fox"
            ),
            Clause(
                latin="consectetur adipiscing elit",
                english="jumps over the lazy dog"
            )
        ])
    ]
)
def LearnPassage(passage):
    while True:
        for paragraph in passage.paragraphs:
            for clause in paragraph.clauses:
                print(f"{clause.latin}")
                # only capture learning data metrics on first input (assume if they keep getting it wrong its typos etc)
                # startTime = time.time()
                userInput = input("> ")
                # endTime = time.time()
                # completionTime = endTime - startTime
                # print(completionTime)
                accuracy = fuzz.ratio(userInput, clause.english)
                print(accuracy)
                clause.avgAccuracy = (clause.avgAccuracy * clause.attempts + accuracy) / (clause.attempts + 1)
                clause.attempts += 1
                print(clause.avgAccuracy)
                print(clause.level)
                if userInput.lower() != clause.english:
                    print(f"{clause.english}")
                    while True:
                        userInput = input("> ")
                        if userInput.lower() == clause.english:
                            break
                        print(f"{clause.english}")





# chunk together mastered clauses

def checkMastered(clauses):
    for clause in clauses:
        if clause.level != "Mastered":
            return False

    return True



def chunkClauses(clauses):
    length = len(clauses)
    chunklist = []
    currentChunk = []

    for i in range(length):
        print("iteration: ", i)
        print("currentChunk: ", currentChunk)
        print("chunklist: ", chunklist)
        print(clauses[i].level)
        if clauses[i].level == "New":
            currentChunk.append(i)
        else:
            chunklist.append(currentChunk)
            currentChunk = []
            chunklist.append(i)

    return chunklist

print(chunkClauses(testPassage.paragraphs[0].clauses))

# # fixed size for now
# def chunkClauses(clauses, windowSize):
#     length = len(clauses)

#     if length <= windowSize:
#         print("invalid, length of input has to be greater than window size")
#         return -1

#     # masteredGroup = checkMastered(clauses[:windowSize])
#     # maxsum equivalent is gonna be chunked latin and chunked english
#     window_sum_eng = " ".join([c.english for c in clauses[:windowSize]])
#     window_sum_lat = " ".join([c.latin for c in clauses[:windowSize]])

#     max_lat = window_sum_lat
#     mnax_eng = window_sum_eng

#     for i in range(length - windowSize):
#         if checkMastered(clauses[i:(i+windowSize)]):
#             window_sum_eng = " ".join([c.english for c in clauses[i:(i+windowSize)]])
#             window_sum_lat = " ".join([c.latin for c in clauses[i:(i+windowSize)]])


# must figure out what to do with chunked clauses e.g how to mark them as chunked, how to view chunks, how to handle chunks 
# probably have chunkClauses return placeholder english and latin
# so refactor main function to work with generic, then inside loop, run chunk function initially, then use result to print latin and check english
# then have to dechunk english input to maintain individual chunk scores 


def fuzzyMatch(userInput, expectedInput):
    positionInInput = 0
    while True:
        if userInput[positionInInput] != expectedInput[positionInInput]:
            pass
'''
test expected input
test the expected input

should return high accuracy

test epxected input
te st expected inp uit
testex pected input

remove spaces?, just look at how many of each letter? 
best way to get rid of typos hmm

# old method gives 26 accuracy for removing a single space, should give like 95
userInput = "testexpected input"
expectedInput = "test expected input"


def oldMethod(userInput, expectedInput):
    accuracy = 0
    errors = 0
    userInput = userInput.replace(" ")
    for i in range(len(userInput)):
        if userInput[i] != expectedInput[i]:
            errors += 1
    accuracy = (len(expectedInput) - errors)/len(expectedInput) * 100
    print(accuracy)

oldMethod(userInput, expectedInput)



def calculateMetrics():
    pass
'''
'''
# how this should run
fuzzy match so its not bad like anki
kinda reinvtengint the wheel could just import a fuzzy matcher but thats boring

think might have to implement custom fuzz or do library fuzz AND split into words and check letter by letter per word to find common mistake words)
could give clues e.g if get wrong (but should know it due to # times etc) then reveal first letter of next word or smth

work through every clause in a Paragraph
go back to top, start chunking clauses together based on how well you know them
how to calc how well you know a clause: accuracy and time
accuracy: have adjustable intervals e.g new, difficult, medium, good, easy with certain percentages accuracy
start chunking when avg accuracy > good
'''



LearnPassage(testPassage)
# text = "cum sis pietatis exemplum, fratremque optimum et amantissimum tui pari caritate dilexeris, filiamque eius ut tuam diligas, nec tantum amitae eiaffectum verum etiam patris amissi repraesentes, non dubito maximo tibi guadio fore cum cognoveris dignam patre dignam te dignam avo evadere."
# translation = ""


# translation = 
# chunks = text.split(",")
# print(chunks)

# split with regex

# for i in ch
