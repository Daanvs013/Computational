###
### Group 21
###


## modules
import re
from types import MethodDescriptorType
from unittest import skip
import pandas as pd

## functions
def cleanString(input):
    output = input
    pos = re.search('\s\s',input) ## returns a match if double space is found, else returns None
    while pos != None: 
        output = re.sub('\s\s',' ',output)
        pos = re.search('\s\s',output)
    return output

def getPages(input):
    ## hoe verbeteren: pagina in anderet talen zoeken of afkorting van pages, meer cases toevoegen

    pos = re.search('(?i)pages|bladzijde|seite|page|pp.', input) ## returns tuple with start and end position of pages in the string 
    if (pos == None):
        return None
    else:
        pos = pos.span() 
        page_numbers = input[pos[1]+1:].strip()
        ## case 1: page numbers are divided by space from the next word. Example: 100-110 word
        pos = re.search("\s",page_numbers) ## returns tuple with start and end position of a single space in the string 
        if (pos != None):
            pos = pos.span()
            page_numbers = page_numbers[0:pos[0]-1].strip()
        else:
        ## case 2: page numbers are divided by a comma from the next word. Example: 100-110, word
            pos = re.search(",",page_numbers) ## returns tuple with start and end position of a comma in the string 
            if (pos != None):
                page_numbers = page_numbers[0:pos[0]-1].strip()
            else:
                page_numbers = None
        return page_numbers

def getXP(input):
    ## hoe verbeteren: kijken of de output wel 9 cijfers is
    ## cijfercheck toegevoegd

    pos = re.search('(?i)xp',input) 
    if (pos == None):
        return None
    else:
        pos = pos.span() ## returns tuple with start and end position of XP in the string
        output = input[pos[0]:].strip()
        ## XP-number might have an - or space or other interpunction between XP and number
        pos = re.search('\d', output) ##check where the first digit in the string is
        if (pos == None):
            return None
        else:
            pos = pos.span()
            output = output[pos[0]:pos[0] + 9] ## xp number is 9 digits
            
        output_splitted = re.split("(1|2|3|4|5|6|7|8|9|0)", output)
        output_splitted = [x for x in output_splitted if x != '']  
        for i in range(len(output_splitted)):
            number = output_splitted[i]
            if number.isnumeric():
                continue
            else:
                return None  
        return output


def getISSN(input):
    ## hoe verbeteren: issn kan andere vormen aannemen dat alleen maar 8 getallen of er kunnen interpuncties in zitten

    pos = re.search('(?i)issn|ISSN',input)
    if (pos == None):
        return None
    else:
        pos = pos.span() ## returns tuple with start and end position of ISSN in the string
        output = input[pos[0]:].strip()
        ## ISSN might have an - or space or other interpunction between ISSN and the number
        pos = re.search('\d', output) ##check where the first digit in the string is
        if (pos == None):
            return None
        else:
            pos = pos.span()
            output = output[pos[0]:pos[0] + 8] ## ISSN number is 8 characters
            return output


def getISBN(input): ##is deze nodig??
    ## hoe verbeteren: isbn kan andere vormen aannemen dat alleen maar 8 getallen of er kunnen interpuncties in zitten

    pos = re.search('(?i)isbn',input) ## returns tuple with start and end position of ISBN in the string
    if (pos == None):
        return None
    else:
        pos = pos.span()
        output = input[pos[0]:].strip()
        ## ISBN-number might have an - or space or other interpunction between XP and number
        pos = re.search('\d', output) ##check where the first digit in the string is
        if (pos == None):
            return None
        else:
            pos = pos.span()
            output = output[pos[0]:pos[0] + 13] ## isbn number is 13 characters
            return output

def getVol(input):

    pos = re.search('(?i)vol|deel',input)
    if (pos != None):
        pos = pos.span()
        output = input[pos[1]:].strip()

        ## check where first digit in string is
        pos = re.search('\d',output)
        if (pos != None):
            output = output[pos.span()[0]:]

            ## case 1, look for single space as end of volume number
            ## case 2, look for comma as end of volume number

            ##first check which case is applicable
            poswhitespace = re.search('\s',output)
            poscomma = re.search(',',output)
            if (poswhitespace != None and poscomma != None):
                poscomma = poscomma.span()
                poswhitespace = poswhitespace.span()
                if (poswhitespace[0] > poscomma[0]):
                    output = output[0:poscomma[0]]
                else:
                    output = output[0:poswhitespace[0]]
            elif (poswhitespace != None and poscomma == None):
                poswhitespace = poswhitespace.span()
                output = output[0:poswhitespace[0]]
            elif (poswhitespace == None and poscomma != None):
                poscomma = poscomma.span()
                output = output[0:poscomma[0]]
            else:
                output = None
    else:
        output = None
    return output
            

def getIssue(input):
    # extra 'functie' toegevoegd om te kijken naar getallen tussen haakjes
    pos = re.search('(?i)no.',input)
    if (pos != None):
        pos = pos.span()
        output = input[pos[1]:].strip()

        ## check where first digit in string is
        pos = re.search('\d',output)
        if (pos == None):
            output = None
        else:
            pos = pos.span()
            output = output[pos[0]:]

            ## case 1, look for single space as end of volume number
            ## case 2, look for comma as end of volume number

            ##first check which case is applicable
            poswhitespace = re.search('\s',output)
            poscomma = re.search(',',output)
            if (poswhitespace != None and poscomma != None):
                poscomma = poscomma.span()
                poswhitespace = poswhitespace.span()
                if (poswhitespace[0] > poscomma[0]):
                    output = output[0:poscomma[0]]
                else:
                    output = output[0:poswhitespace[0]]
            elif (poswhitespace != None and poscomma == None):
                poswhitespace = poswhitespace.span()
                output = output[0:poswhitespace[0]]
            elif (poswhitespace == None and poscomma != None):
                poscomma = poscomma.span()
                output = output[0:poscomma[0]]
            else:
                output = None
    check = input[input.find("(")+1:input.find(")")]
    if check != '':
        check_1 = int(input.index(")")-1)
        check_2 = int(input.index("(")+1)
        if check_1 - check_2 < 2 and check.isnumeric():
            output = check
        else:
            output = getIssue(input[check_1 + 2:])
        
        return output
    else:
        output = None
    return output

def getAuthor(input):
    ## author name is almost always in the front and ends with a : or with et al
    pos = re.search('(?i)et al|:',input)
    if (pos != None):
        output = input[0:pos.span()[0]].strip()
    else:
        output = None

    ##if the above code does not return any results (so no et al.), we start looking at capital letters in order to find a match
    pos_splitted = re.split("[,|.|' ']", input)
    pos_splitted = [x for x in pos_splitted if x != '']

    for i in pos_splitted: 
        # nog elif statements toevogegen voor volgende cases af te gaan
        further_splitted = re.split("([a-z]|[A-Z])", i)
        further_splitted = [x for x in further_splitted if x != '']
        if further_splitted[0].isalpha():
            if len(i) == 1:
                continue
            output = i
            break
        else:
            output = pos_splitted

    return output

def getTitle(input):
    ## authors section almost always ends in et al or :
    pos = re.search('(?i)et al|:',input)
    if (pos != None):
        output = input[pos.span()[1]+1:].strip()
        if (len(output) == 0):
            output = None
        else:
            ## check title section for 'title' or title,
            if (output[0]=="'"):
                pos = re.search("'",output[1:])
                output = output[1:pos.span()[1]]
            else:
                pos = re.search(',',output)
                if (pos != None):
                    output = output[0:pos.span()[1]-1]
                else:
                    output = None
    else:
        output = None
    return output

def getYear(input):
    pages = getPages(input)
    pos = re.search("\d\d\d\d",input) ## check for 4 digits directly after earch other
    if (pos != None):
        output = input[pos.span()[0]:pos.span()[1]]
        ## check for false positive, for example we took page numbers instead of year number
        if (pages != None):
            if (output in pages):
                pos = re.search(pages,input).span()
                output = input[pos[1]:]
                pos = re.search('\d\d\d\d',output)
                if (pos != None):
                    output = output[pos.span()[0]:pos.span()[1]]
                else:
                    output = None

    else:
        output = None
    return output

def getMonth(input):
    ## hoe verbeteren: zoek ook op maanden waar een type fout in staat

    pos = re.search("(?i)january|february|march|april|may|june|july|augustus|september|october|november|december|januari|februari|maart|mei|juni|juli|oktober",input)
    if (pos != None):
        output = input[pos.span()[0]:pos.span()[1]]
    else:
        output = None
    return output

def getScore(validator,to_match):
    score = 0
    threshold = 3
    ## increase score if validator metadata is the same as the to_match metadata
    for metadata in validator.iteritems():
        ## dont compare the cluster_id column
        if metadata[0] == 'cluster_id':
            continue
        ## dont compare metadata if one of the two is none
        elif metadata[1] != None:
            if to_match[metadata[0]] != None:
                ## if metadata is similar, increment score with 1
                if str(metadata[1]) in str(to_match[metadata[0]]):
                    score += 1
                else:
                    pass
            else:
                continue
        else:
            continue
    ## return matching score
    if score > threshold:
        return True
    else:
        return False

##print(getMonth("Daan van Turnhout et al, titel van dit boek is bla bla bal, May  .bladzijde: 1000-1100 asdfasdf 2022 asdf xp-123456789 adf ISSN:98475645 asdfasdf       ISBN:1234567891012 sdfsdf asdf vol  1011, sdfsd"))
