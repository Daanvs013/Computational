## modules
import re

## functions
def removeSpaces(input):
    output = input
    pos = re.search('\s\s',input)
    while pos != None:
        output = re.sub('\s\s',' ',output)
        pos = re.search('\s\s',output)
    return output