from PIL import Image
import pytesseract
import builtins
from ParseString import parseString
from ConcatString import concatString
from autocorrect import spell

"""
Update 1/22/18 - Adding in comments to clarify functions, and clean up code.
"""
class ImageText:
    
    """
    Represents a picture and a way to summarize it.
    
    @param imgloc represents the location of the image
    """
    def __init__(self, imgloc):
        self.img = Image.open(imgloc)
        self.txt = self.ImageToText(self.img)
    
    """
    Gets the text from the image.
    """
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
            
    """
    Added to this class 1/22/18 (it was just a helper outside this class 
    before).
    
    Converts the image into text.
    
    @param img represents the image to parse into text
    @returns the text read from the document
    
    """
    def __image_to_text__(self, img):
            try:
                  builtins.open = self.bin_open
                  bts = pytesseract.image_to_string(img)
            finally:
                  builtins.open = open
            return (str(bts, 'cp1252', 'ignore'))
            
    """
    Added to this class 1/22/18 (it was just a helper outside this class 
    before).
    
    Helper to open the file.
    
    @param filename is location of the file.
    @param mode is the type of opening.
    """
    def bin_open(self, filename, mode='rb'):       
        return open(filename, mode)

                  



