# [List-of String] -> String
# Parses through the string and forms sentences
def concatString(los):
    r = ""
    for s in los: 
        if(len(s) > 0): 
            if(s[0] != ' '):
                s = ' ' + s
            if(s[len(s) - 1] != '.'):
                s = s + '.'
        r = r + s
    return r

