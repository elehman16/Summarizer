import unittest.mock
from FindSentence import findSentence

# String -> [List-of [List-of String]]
# Parse the string into individual words and sentences
def parseString(s):
    al = []
    if(s.find('.') == -1):
        al.append(createSentence(s + " "))
        return al
    else:
        while(len(s) > 0):
            if(s[0:1] == " " or s[0:1] == '.'):
                s = s[1:]
            else: 
                space = findSentence(s)
                al.append(createSentence(s[:(space + 1)]))
                if (space == -1):
                    return al
                else:
                    s = s[space:]
    return al

class TestParseString(unittest.TestCase): 
    def test(self):
        self.assertEquals(parseString('Hello there. I am gen. Bob. Nice to meet you.'), 
                          [['Hello', 'there'], ['I', 'am', 'gen.', 'Bob'], ['Nice', 'to', 'meet', 'you']])
        self.assertEquals(parseString('a b c'), [['a', 'b', 'c']])
        self.assertEquals(parseString('I like cheese. Hi.'), [["I", "like", "cheese"], ["Hi"]])

#String -> [List-of String]
#produce a list of string that represents 1 sentence
def createSentence(s): 
    idx = findSentence(s)
    worklist = s[0: idx]
    al = []
    while(len(worklist) > 0):
        split = worklist.find("\n")
        if(split >= 0):
            worklist = worklist[:split] + " " + worklist[split + 1:]       
        space = worklist.find(" ")
        if(space == -1):
            al.append(worklist[0:len(worklist)])
            return al
        al.append(worklist[0:space])
        worklist = worklist[space + 1:]
    return al

class TestCreateSentence(unittest.TestCase): 
    def test(self):
        self.assertEquals(createSentence('Hello.'), ['Hello'])
        self.assertEquals(createSentence('a b c.'), ['a', 'b', 'c'])
        self.assertEquals(createSentence('I like cheese.'), ["I", "like", "cheese"])    
        self.assertEquals(createSentence("asdfa cde ."), ["asdfa", "cde"])
        self.assertEquals(createSentence("abcd."), ["abcd"])
        