###
### Group 21
###


## modules
import re

from sqlalchemy import false

## functions
def cleanString(input):
    output = input
    pos = re.search('\s\s',input) ## returns a match if double space is found, else returns None
    while pos != None: 
        output = re.sub('\s\s',' ',output)
        pos = re.search('\s\s',output)
    return output

def getYear(input):
    pos = re.search("\d\d\d\d",input) ## check for 4 digits directly after earch other
    counter = 0
    output = None
    while counter < len(input): 
        if pos != None:
            if counter == 0:
                output = input[pos.span()[0]:pos.span()[1]]
            else:
                output = new_part[pos.span()[0]:pos.span()[1]]

    
            if int(output) in range(1900,2022):
                output = output
                break
            else:
                new_index = re.search(f"{output}([\d\D]*)", input)
                new_part = new_index.group(1)
                pos = re.search("\d\d\d\d",new_part)
            counter += 1
        else:
            break

    return output

def getMonth(input):
    pos = re.search("(?i)january|januari",input)
    if (pos != None):
        output = 1
    else:
        pos = re.search("(?i)februari|febuary",input)
        if (pos != None):
            output = 2
        else:
            pos = re.search("(?i)march|maart",input)
            if (pos != None):
                output = 3
            else:
                pos = re.search("(?i)april",input)
                if (pos != None):
                    output = 4
                else:
                    pos = re.search("(?i)may|mei",input)
                    if (pos != None):
                        output = 5
                    else:
                        pos = re.search("(?i)june|juni",input)
                        if (pos != None):
                            output = 6
                        else:
                            pos = re.search("(?i)july",input)
                            if (pos != None):
                                output = 7
                            else:
                                pos = re.search("(?i)augustus",input)
                                if (pos != None):
                                    output = 8
                                else:
                                    pos = re.search("(?i)september",input)
                                    if (pos != None):
                                        output = 9
                                    else:
                                        pos = re.search("(?i)october|oktober",input)
                                        if (pos != None):
                                            output = 10
                                        else:
                                            pos = re.search("(?i)november",input)
                                            if (pos != None):
                                                output = 11
                                            else:
                                                pos = re.search("(?i)december",input)
                                                if (pos != None):
                                                    output = 12
                                                else:
                                                    output = None
    return output

def getXP(input):
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


def getISBN(input):  
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

def getDOI(input):
    ## doi format 2 digits point 4 digits
    pos = re.search('(?i)\d\d\.\d\d\d\d',input)
    if (pos == None):
        return None
    else:
        pos = pos.span()
        output = input[pos[0]:pos[1]]
        return output


def getPages(input):
    pos = re.search('(?i)pages|bladzijde|seite|page|pp\.', input) ## returns tuple with start and end position of pages in the string 
    if (pos == None):
        return None
    else:
        pos = pos.span() 
        page_numbers = input[pos[1]+1:].strip()
        ## split on white space or comma for example: "pages: 100-110 word" or "pages: 100-110, word"
        pos = re.search("\s|,",page_numbers) ## returns tuple with start and end position of a single space in the string 
        if (pos != None):
            pos = pos.span()
            page_numbers = page_numbers[0:pos[0]].strip()
        else: ## pages numbers are the last characters in the string
            pass
        return page_numbers

############################################################################ alles hierboven is al gecontroleerd
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
    else:
        output = None
    return output

def getAuthor(input):
    ## author name is almost always in the front and ends with a : or with et al
    pos = re.search('(?i)et al|:',input)
    if (pos != None):
        output = input[0:pos.span()[1]].strip()
    else:
        output = None
    return output

def getTitle(input):
    ## authors section almost always ends in et al or :
    output = None
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


input = "Altschul S. F. et al. Gapped BLAST and PSI-BLAST: A new generation of protein database search programs Nucleic Acids Research. 1997, vol. 25(17), pages 3389-3402"
print(getPages(input))
print(getXP(input))
print(getISSN(input))
print(getISBN(input))
print(getVol(input))
print(getIssue(input))
print(getAuthor(input))
#print(getTitle(input))
print(getYear(input))
print(getMonth(input))
