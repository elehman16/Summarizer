from nltk.corpus import wordnet as wn

# Get a definition of all the words in the list
# [List-of String] -> [List-of [List String [List-of String]]]
# First string in the return value is the word,
# and the second part is the definition
def flashCard(los):
    r = []
    for s in los:
        r.append([s, genDef(s)])
    return r
        

# Generate the dictionary definition for 1 string 
# String -> [List-of String]
def genDef(s):
    r = []
    for syns in wn.synsets(s, pos='n'):
       r.append(syns.definition())
    return r