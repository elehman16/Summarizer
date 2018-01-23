from PIL import Image
import pytesseract
import builtins

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
        self.txt = self.__image_to_text__()
    
    """
    Gets the text from the image.
    """
    def text(self):
        return self.txt;
            
    """
    Added to this class 1/22/18 (it was just a helper outside this class 
    before).
    
    Converts the image into text.
    
    @param img represents the image to parse into text
    @returns the text read from the document
    
    """
    def __image_to_text__(self):
        return image_text(self.img)


original_open = open
def bin_open(filename, mode='rb'):       # note, the default mode now opens in binary
    return original_open(filename, mode)


def image_text(img):    
    try:
        builtins.open = bin_open
        bts = pytesseract.image_to_string(img)
    finally:
        builtins.open = original_open
    
    return str(bts, 'cp1252', 'ignore')           



