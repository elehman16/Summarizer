import unittest.mock
import numpy as np
from ParseString import parseString
from Summary import SmartUrl
from Summary import rankImportance
from Summary import filterOutlier
import inflect
p = inflect.engine()
from nltk.corpus import wordnet as wn
from FindSentence import findSentence
import warnings
from ConcatString import concatString

filterWords = ['i', 'he', 'her', 'his', 'him', 'she', 'as', 'are', 'in', 'like', 'much',
               'can', 'so', 'if', 'its', 'may', 'use', 'come', 
               'or', 'a', 'at', 'it', 'be', 'no', 'has']

file = open('C://Users//Eric//Documents//BiologySample.txt', "r").read()
file1 = open('C://Users//Eric//Documents//SampleCivilWar.txt', "r").read()

# UserInput(file, "Cell Biology", True)
# UserInput(file1, "Battle of Antietam", True)
# Represents the user inputted string
class UserInput: 
    
    # text represents the actual passage
    # key represents the title or main topic
    # the los produced is a [List-of [List-of String]]
    # Flag represents whether or not we want to use wiki
    # for extra accuracy
    # with each inner list representing a sentence.
    def __init__(self, txt, key, flag):
        self.key = key
        self.txt = txt.replace(u'\xa0', u' ')
        self.los = parseString(txt.replace(u'\xa0', u' '))
        self.flag = flag
        
    # Generates Important sentences given user text
    # UserInput, Boolean -> [List-of String]
    def genImportantSentence(self):
        warnings.filterwarnings("ignore")
        if(self.flag):
            cc = self.combineCount()
        else: 
            cc = filterPlural(self.countSimplify())
        ss = self.splitSentences()
        rank = self.rank(cc)
        comb = []
        for i in range(0, len(rank)):
            tmp = []
            tmp.append(ss[i])
            tmp.append(rank[i])
            comb.append(tmp)
        rank = np.sort(rank)
        minVal = rank[np.floor(len(rank) * .8)]
        r = list(filter(lambda x: x[1] >= minVal, comb))
        
        tmp = []
        for innList in r:
            tmp.append(innList[0])
        s = concatString(tmp)
        return s
    
    # Generates the important words for the given text
    def genImportantWords(self):
        if(self.flag):
            cc = self.combineCount()
        else: 
            cc = self.countSimplify()       
        r = list(map(lambda x: x[1], cc))
        r = np.sort(r)
        minVal = r[int(np.floor(len(r) * .8))]
        low = list(filter(lambda x: x[1] >= minVal, cc))
        low = list(map(lambda x: x[0], low))
        return low
        
    
    # Rank each sentence, takes in a [List-of [List String Number]]
    # Returns a List of numbers, which each corresponding to a rank
    def rank(self, lowr):
        i = len(self.splitSentences())
        l = np.zeros(i)
        j = 0
        while(j < i):
            importance = 0
            g = 0
            while(g < len(self.los[j])):
                t = find(self.los[j][g], lowr)
                if(t >= 0):
                    importance = importance + lowr[t][1]
                g = g + 1
            l[j] = importance
            j = j + 1
        return l
    
    # Generate a list of strings, split up by sentences, so that we can
    # easily take out the important sentences and join them
    # UserInput -> List-of String
    def splitSentences(self):
        r = []
        txt = self.txt
        while(len(txt) > 0):
            i = findSentence(txt)
            if(i > 0 and not(i == len(txt) - 1)):
                r.append(txt[0:(i + 1)])
                txt = txt[(i + 1):len(txt)]
            else: 
                r.append(txt)
                return r
        return r
               
    # Simplifiy the list of words and filter out certain filler words
    # Returns a list of string (not a list-of-list-of-strings)
    def simplify(self):
        low = []
        for innList in self.los:
            for word in innList:
                word = word.lower()           
                r = wn.synsets(word)
                if(len(r) > 0 and r[0].pos() == 'n' and not(word in filterWords)):
                    low.append(word)
        return low
        
    # Create a count for the simplified words
    # Returns a [List-of [List String Number]]
    def countSimplify(self):
        return filterOutlier(rankImportance(self.simplify()))
        
    # combine the count of the wiki and the summary
    # Returns [List-of [List String Number]]
    def combineCount(self):
        losSum = self.countSimplify()
        losWiki = SmartUrl(self.key).findImportantWords()
        for inList in losWiki:
            sTemp = inList[0].lower()
            idx = find(sTemp, losSum)
                       
            if (idx >= 0):
                losSum[idx] = [sTemp, losSum[idx][1] + inList[1]]
        return filterOutlier(filterPlural(losSum))

# Test the split function       
class TestSplitSentences(unittest.TestCase):
    def test(self):
        ui = UserInput("Hi. Bye. See ya.", "Greetings", True)
        ui1 = UserInput("", "Greetings", True)
        ui2 = UserInput("Hi.", "", True)
        self.assertEquals(ui.splitSentences(), ["Hi.", " Bye.", " See ya."])
        self.assertEquals(ui1.splitSentences(), [])
        self.assertEquals(ui2.splitSentences(), ["Hi."])
        
# String, [List-of [List String Number]] -> Integer
# Finds the index of the String in the other list
# Returns negative 1 if it is not in the list. Returns 
# the index of the first occurance.
def find(s, losn):
    s = s.lower()
    sPlural = genPlural(s)        
    i = 0
    for inner in losn: 
        if(inner[0].lower() == s.lower() or inner[0].lower() == sPlural.lower()):
            return i
        i = i + 1
    return -1
    
# Test the functions in SmartFind
class TestFind(unittest.TestCase):
    def test(self):
        l = []
        l1 = [["a", 2]]
        l2 = [["A", 2]]
        l3 = [["ab", 5], ["b", 2]]
        l4 = [["a", 1], ["b", 2], ["c", 3], ["D", 4]]
        self.assertEquals(find("A", l), -1)
        self.assertEquals(find("b", l1), -1)
        self.assertEquals(find("a", l1), 0)
        self.assertEquals(find("a", l2), 0)
        self.assertEquals(find("b", l3), 1)
        self.assertEquals(find("cd", l3), -1)
        self.assertEquals(find("d", l4), 3)

# generate the plural version of the given word or
# unplural it if need be
# String -> String
def genPlural(s):
    # is not plural
    if(type(p.singular_noun(s)) == str): 
        return p.singular_noun(s)
    elif(type(p.plural(s)) == str):
        return p.plural(s)
    else:
        return ""
        
class TestGenPlural(unittest.TestCase):
    def test(self):
        self.assertEquals(genPlural("book"), "books")
        self.assertEquals(genPlural("books"), "book")
        self.assertEquals(genPlural("city"), "cities")
        self.assertEquals(genPlural("cities"), "city")
    
# combine the plural words into 1 single count 
# [List-of [List String Number]] -> [List-of [List String Number]]
def filterPlural(lown):
    r = []
    while(len(lown) > 0):
        s = lown[0][0]
        n = lown[0][1]
        idx = find(s, r)
        if(idx == -1):
            r.append(lown[0])
        else: 
            r[idx] = [r[idx][0], r[idx][1] + n]
        lown = lown[1:]
    return r
         
    
class TestFilterPlural(unittest.TestCase):
    def test(self):
        self.assertEquals(filterPlural([]), [])
        self.assertEquals(filterPlural([["a", 2], ["bar", 3], ["car", 4]]), [["a", 2], ["bar", 3], ["car", 4]])
        self.assertEquals(filterPlural([["a", 2], ["a", 3], ["car", 4]]), [["a", 5], ["car", 4]])
        self.assertEquals(filterPlural([["car", 2], ["a", 3], ["cars", 4]]), [["car", 6], ["a", 3]])
        
 

        