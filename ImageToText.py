from PIL import Image
import pytesseract
import builtins
from ParseString import parseString
from ConcatString import concatString
from autocorrect import spell

# ImageText("CivilWar.png", "Battle of Antietem", True)

# Represents a picture and a way to summarize it
class ImageText:
    
    def __init__(self, imgloc, title, flag):
        self.img = Image.open(imgloc)
        self.txt = ImageToText(self.img)
        self.title = title
        self.flag = flag
        
    # Purpose: To re-adjust the image to text portion of this         
    # class, as the ocr does a pretty trash job of interpretation
    # This function will go through individual words and attempt to
    # parse them and use an autocorrector on them.
    # Only do this part if they have autocorrect flag as true
    def text(self):
        if(self.flag):
            lolos = parseString(self.txt)
            r = []
            for sentence in lolos:
                s = ''
                for word in sentence:                    
                    if(word.find(".") >= 0): 
                        s = s + " " + word
                    else:
                        s = s + " " + spell(word)                  
                r.append(s)
            return concatString(r)
        else: 
            return self.txt
                  
# Image -> String
# Converst image to text
def ImageToText(img):
        try:
              builtins.open = bin_open
              bts = pytesseract.image_to_string(img)
        finally:
              builtins.open = original_open
        return (str(bts, 'cp1252', 'ignore'))
        
        
# Helps out with image to text conversion        
# note, the default mode now opens in binary        
original_open = open
def bin_open(filename, mode='rb'):       
    return original_open(filename, mode)



