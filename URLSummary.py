import urllib
import unittest.mock
from bs4 import BeautifulSoup
import re
from ConcatString import concatString

# http://www.digitalhistory.uh.edu/disp_textbook.cfm?smtID=2&psid=3072
def sumUrl(url):
   html = urllib.request.urlopen(url).read()
   soup = BeautifulSoup(html, 'html.parser')
   texts = soup.findAll(text=True)
   visible_text = filter(visible, texts)
   visible_text = list(filter(lambda x: x != '\n' and x != '\xa0', visible_text))
   visible_text = list(map(filterString, visible_text))
   s = concatString(visible_text)
   return s
   
def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element)):
        return False
    return True

# String -> String
# Take out any parts of the string that make it unreadable
def filterString(s):
    r = ""
    l = ['\r', "\t", '\n', '\xa0']
    while(len(s) > 0):
        if(s[:1] in l or s[:4] in l):
            s = s[2:]
        else: 
            r = r + s[0]
            s = s[1:]
    return r
    
class TestFilterString(unittest.TestCase):
    def test(self):
        self.assertEquals(filterString('\r'), "")
        self.assertEquals(filterString('\n\t\t\n\n\t\t\t\xa0'), "")
        
   