import unittest.mock
from nltk.corpus import wordnet as wn
abb = ['mr', 'ms', 'mrs', 'pres', 'gen']
# Find the end of the sentence, and return the index
# Will return -1 if there is no period 
# String -> Integer   
def findSentence(s): 
    r = 0
    while(len(s) > 0): 
        space = s.find(" ")
        period = s.find(".")
        if(period == -1):
            return -1
        if(space == -1):
            return r + period
        if(space > period):
            word = s[0:period]
            word = word.lower()           
            low = wn.synsets(word)
            if (len(low) > 0 and not (word in abb)): 
                return r + period
            else: 
                r = r + space + 1
                s = s[(space + 1):]
        else: 
            r = r + space + 1
            s = s[(space + 1):]
    return -1
        

class TestFindSentence(unittest.TestCase):
    def test(self): 
        self.assertEquals(findSentence("Hello there my good friend"), -1)
        self.assertEquals(findSentence(""), -1)
        self.assertEquals(findSentence("Hello."), 5)
        self.assertEquals(findSentence("Hello. Hi."), 5)
        self.assertEquals(findSentence("Hello Mr. Potato."), 16)
        self.assertEquals(findSentence("Hello Cpl. Potato."), 17)
        self.assertEquals(findSentence("Hello Gen. Potato."), 17)