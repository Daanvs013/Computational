###
### Group 21
###

############################################
#this file will be imported in main.py
###########################################


## modules
import re
 
## functions
def cleanString(input):
    #funtion to remove double white spaces from input string
    #returns string with double white spaces replaced by single white space
    output = input
    pos = re.search('\s\s',input) ## returns a match if double space is found, else returns None
    while pos != None: 
        output = re.sub('\s\s',' ',output)
        pos = re.search('\s\s',output)
    return output

def getYear(input):
    #function to find the publication year in a string
    #returns first four digit number between 1900 and 2022 included
    pos = re.findall("\d\d\d\d",input) ## find all numbers that have 4 digits 
    output = None
    if pos!=None: ## for each number check if it is in the allowed range
        for match in pos:
            if int(match) in range(1900,2023):
                output = match
    else:
        output = None

    return output

def getMonth(input):
    #function to find the publication month in a string
    #returns the number of the month found
    pos = re.search("(?i)january|januari",input) #(?i) is used to treat capital and lowercase letters the same
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
    #function to find the XP number in a string
    #returns the found XP number
    pos = re.search('(?i)xp',input)
    output = None 
    while (pos != None): #we use a while loop, since 'xp' may also be present in for example the title
        pos = pos.span() ## returns tuple with start and end position of XP in the string
        output = input[pos[0]+2:].strip() #output is now everything after 'xp'
        output_copy = output #make a copy of output for later use
        ## XP-number might have an - or space or other interpunction between XP and number
        pos = re.search('\d', output) ##check where the first digit in the string is
        if (pos == None):
            output=None #there are no numbers in the string --> so there is no xp number
            continue
        else:
            pos = pos.span()
            output = output[pos[0]:pos[0] + 9] ## xp number is 9 digits

        output_splitted = re.split("(1|2|3|4|5|6|7|8|9|0)", output) #we are now going to check whether each element of the found string is a number
        output_splitted = [x for x in output_splitted if x != '']
        if len(output_splitted) >= 9: #otherwise it cannot be the xp number
            counter = 1
            for i in range(len(output_splitted)):
                number = output_splitted[i]
                if number.isnumeric():
                    counter += 1
                    if counter == 10:
                        return output
                    continue
                else:
                    pos = re.search('(?i)xp',output_copy)
                    input = output_copy
                    output = None
                    break
        else:
            pos = re.search('(?i)xp',output_copy) #we now look for the next instance of 'xp' in the string and repeat the whole process
            input = output_copy
            output = None

    return output

def getISSN(input):
    #function to find the ISSN number in the string
    #returns the ISSN number
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
            output = output[pos[0]:pos[0] + 9] ## ISSN number is 8 characters
            return output

def getISBN(input):
    #function to find ISBN number in a string
    #returns ISBN number
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
    #function that returns DOI of a string
    ## doi format 2 digits point 4 digits
    pos = re.search('(?i)\d\d\.\d\d\d\d',input)
    if (pos == None):
        return None
    else:
        pos = pos.span()
        output = input[pos[0]:pos[1]]
        return output


def getPages(input):
    #function that finds and returns the pagenumbers in a string
    pos = re.search('(?i)pages|bladzijde|seite|page|pp\.', input) ## returns tuple with start and end position of pages in the string 
    if (pos == None):
        return None
    else:
        pos = pos.span() 
        page_numbers = input[pos[1]+1:].strip()
        output = page_numbers
        pos = re.search('\s',input) ## returns a match if white space is found, else returns None (whitespaces are removed for later convenience
        while pos != None: 
            output = re.sub('\s','',output)
            pos = re.search('\s',output)
        ## split on comma for example: "pages: 100-110, word"
        pos = re.search(",",output) ## returns tuple with start and end position of a comma in the string 
        if (pos != None):
            pos = pos.span()
            page_numbers = output[0:pos[0]].strip()
        elif re.search('(?i)[a-z]|\(', page_numbers) != None: #if no comma is found, we look for the first letter or first bracket
            pos = re.search('(?i)[a-z]|\(', page_numbers).span()
            page_numbers = page_numbers[0:pos[0]].strip()
        else: ## pages numbers are the last characters in the string
            pass
        return page_numbers

def getVol(input):
    #function that finds and returns the volume found in the string
    ## first look if there is an 'vol' or 'deel' keyword in the string
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
    #function that finds and returns the issue in the string
    pos = re.search('(?i)no\.|nr\.',input) #first we look for the words no. and nr.
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
        return output
    #if the above search does not give any results, we look at numbers between brackets that could possibly indicate a volume
    first_bracket = input.find("(")+1
    second_bracket = input.find(")")
    if second_bracket < 0: #if no brackets are found, second_bracket takes value 0 and so there is no volume which we can reasonably find
        output = None
    else:
        check = input[input.find("(")+1:input.find(")")]
        if check != '':
            check_1 = int(input.index(")")-1)
            check_2 = int(input.index("(")+1)
            if check_1 - check_2 < 2 and check.isnumeric(): #issue is at most 2 characters long
                output = check
                return output
            else:
                output = getIssue(input[check_1 + 2:]) #look for the next pair of brackets in the string
        else:
            output = None
    return output

def getAuthor(input):
    #function that finds and returns the name of the author
    ## author name is almost always in the front and ends with a : ,  or with et al
    # we do not think it is reasonable to find the author when et al is not present in the string
    pos = re.search('(?i)et al',input)
    if (pos != None):
        output = input[0:pos.span()[1]].strip()
    else:
        pos = re.search('(?i),|:',input)
        if pos !=None:
            output = input[0:pos.span()[1]-1].strip()
        else:
            output = None
    return output

def getTitle(input):
    #function that finds and returns the (most likely) title of the string
    ## find the first letter in the string, because we look at title as last so we have removed all other metadata information
    pos = re.search('(?i)[a-z]',input)
    if pos!=None:
        input = input[pos.span()[0]:]
        ## find comma
        pos = re.search(',',input)
        if pos!=None:
            output = input[0:pos.span()[0]].strip()
        else:
            output=input.strip()
    else:
        output = None
    return output

def getJournal(input):
    #function that finds and returns the journal of a string
    #again, we do not think it is reasonable to find the journal when there is not expression like journal in the string
    pos = re.search('(?i)journal|science', input)
    if pos!=None:
        input = input[pos.span()[0]:]
        pos = re.search(',|\.',input)
        if pos != None:
            output = input[0:pos.span()[0]].strip()
        else:
            output = None
    else:
        output = None
    return output
