import urllib
import unittest.mock
import numpy as np
from google import search
      
url = 'https://en.wikipedia.org/wiki/Cell_(biology)'
# Represents a URL with data to be extracted
class SmartUrl: 
    
    def __init__(self, keyword):
        self.url = SmartFind(keyword).genUrl()
            
    # URL -> [List-of [List String Number]] 
    # goes to the given URL and finds important tags
    def findImportantWords(self):  
        response = urllib.request.urlopen(self.url)
        webContent = response.read().decode("utf-8")
        return filterOutlier(rankImportance(parseData(webContent)))

# Test the findImportantWords function
class TestFindImportantWords(unittest.TestCase):
    def test(self):
        l = SmartUrl(url).findImportantWords()
        self.assertEquals(len(l) > 0, True)
        # every inner list is of length 2, and has a tag of more than 0
        for innerList in l: 
            self.assertEquals(len(innerList), 2)
            self.assertEquals(innerList[1] > 0, True)
            
# represents a lot of links with certain key words
class SmartFind:
    
    def __init__(self, key):
        self.key = key
        
    # generate a single URL 
    # Returns a url in String format
    def genUrl(self):
        loUrl = self.genLoUrl()
        return loUrl[0]
    
    # Generate url's with relevant topics 
    # Returns a list of URL in string format
    def genLoUrl(self):
        loUrl = []
        keyword = self.key
        for url in search("Wikipedia" + keyword, stop=5):
            loUrl.append(url)
        return loUrl
        
# Test the functions in SmartFind
class TestSmartFind(unittest.TestCase):
    def test(self):
        sf = SmartFind("Cell Biology")
        lol = sf.genLoUrl()
        self.assertTrue(lol[0] == url)
        self.assertTrue(sf.key == "Cell Biology")
        self.assertTrue(sf.genUrl() == url)
      

# [List-of [List String Number]] -> [List-of [List String Number]] 
# Filters out outliers based on standard deviation
def filterOutlier(l):
    mySum = 0
    mySumSq = 0
    # calc the sum of the list structure
    for innnerList in l: 
        mySum = mySum + innnerList[1]
        mySumSq = mySumSq + innnerList[1] * innnerList[1]
   
    # cut out values lower that are outliers in sample
    if(len(l) > 0):
        var = mySumSq / len(l) - (mySum / len(l)) * (mySum / len(l))
        std = np.sqrt(var)
        lower = mySum / len(l) - std
        return list(filter(lambda x: x[1] >= lower, l))
    else: 
        return l
    
# Test the filterOutlier function
class TestFilterOutlier(unittest.TestCase):
    def test(self):
        self.assertEqual(filterOutlier([]), [])
        self.assertEqual(filterOutlier([["a", 500], ["A", 250], ["b", 0]]), [["a", 500], ["A", 250]])
        self.assertEquals(filterOutlier([["A", 1000], ["a", 0]]), [["A", 1000], ["a", 0]])
        
        
# [List-of String] -> [List-of [List String Number]]
# Takes in a least of features, and creates a new list
# with the number of occurences in it
def rankImportance(l):
    r = []
    while(len(l) > 0): 
        string = l[0]
        temp = []
        temp.append(string)
        temp.append(l.count(string))
        r.append(temp)
        l = list(filter(lambda x: not(x == string), l))
    return r     
    
# Test the rankImportance function
class TestRankImportance(unittest.TestCase):
    def test(self):
        self.assertEqual(rankImportance([]), [])
        self.assertEqual(rankImportance(["a", "a", "b", "c"]), [["a", 2], ["b", 1], ["c", 1]])
        self.assertEqual(rankImportance(["a", "a", "a", "a"]), [["a", 4]])
        
#String -> [List-of String]
#Get a list of all the titles and keywords from a wiki article
def parseData(w):
    r = []
    # stop when string is shorter than title="
    while(len(w) >= 7): 
        s = w.find('title="')
        if (s != -1):
            temp = getTitle(w[s + 7:len(w)])
             # determine if it is worth keeping
            if (temp.isalpha()): 
                r.append(temp)
        w = w[s + 7: len(w)]
    return r
    
# Test the ParseData function
class TestParseData(unittest.TestCase):
    def test(self):
        self.assertEqual(parseData('title="asdfasdf"'), ["asdfasdf"])
        self.assertEqual(parseData('title="as"as"'), ['as'])
        self.assertEqual(parseData('a"s"s"'), [])
        
# String -> String
# Given a string, with a title tag, get the string in it
def getTitle(w):
    r = "" 
    continueParse = True
    while(continueParse and len(w) > 0):
        if (w[0:1] == '"'):
            continueParse = False
        else: 
            r = r + w[0:1]
        w = w[1:]
                 
    return r

# Test the getTitle function
class TestSuite(unittest.TestCase):
    def test(self):
        self.assertEqual(getTitle('asdfasdf"'), "asdfasdf")
        self.assertEqual(getTitle('as"as"'), 'as')
        self.assertEqual(getTitle('a"s"s"'), 'a')
        
        