###
### Group 21
###

############################################
#this file will be imported in main.py
###########################################


## modules
import pandas as pd
from cdifflib import CSequenceMatcher
import difflib as diff
diff.SequenceMatcher = CSequenceMatcher
import re

def rule1(list1, list2):
    score = 0
    vol1 = list1['volume']
    pag1 = list1['pages']
    iss1 = list1['issn']
    vol2 = list2['volume']
    pag2 = list2['pages']
    iss2 = list2['issn']
    if vol1!=None and vol2!=None and vol1 == vol2:
        score += 1
        if pag1 == pag2:
            score += 2
            if iss1!=None and iss2!=None and iss1 == iss2:
                score += 3
    else:
        if pag1 == pag2:
            score += 1
            if iss1!=None and iss2!=None and iss1 == iss2:
                score += 1
        elif iss1!=None and iss2!=None and iss1 == iss2:
            score += 1
    return score

def rule2(list1, list2, threshold):
    score = 0
    aut1 = list1['authors']
    tit1 = list1['title']
    aut2 = list2['authors']
    tit2 = list2['title']
    if  type(tit1) == str and type(tit2) == str and diff.SequenceMatcher(None,tit1.lower(), tit2.lower()).quick_ratio() >= threshold:
        score += 3
        if type(aut1) == str and type(aut2) == str and diff.SequenceMatcher(None,aut1.lower(), aut2.lower()).quick_ratio() >= threshold:
            score += 2
        else:
            score -= 1
    elif type(aut1) == str and type(aut2) == str and diff.SequenceMatcher(None,aut1.lower(), aut2.lower()).quick_ratio() >= threshold:
        score += 1
    return score

def rule3(list1, list2, threshold):
    score = 0
    total1 = ''
    for x in list1:
        total1 += ' ' + str(x)
    total2 = ''
    for x in list2:
        total2 += ' ' + str(x)
    num1 = re.sub("[a-zA-Z]","", total1)
    num2 = re.sub("[a-zA-Z]","", total2)
    if diff.SequenceMatcher(num1,num2).quick_ratio() >= threshold:
        score += 2
    return score

def rule4(list1, list2):
    score = 0
    ISSN1 = list1['issn']
    ISBN1 = list1['isbn']
    XP1 = list1['xp']
    DOI1 = list1['doi']
    ISSN2 = list2['issn']
    ISBN2 = list2['isbn']
    XP2 = list2['xp']
    DOI2 = list2['doi']
    if ISSN1!=None and ISSN2!=None and ISSN1 == ISSN2:
        score += 2
    if ISBN1!=None and ISBN2!=None and ISBN1 == ISBN2:
        score += 2
    if XP1!=None and XP2!=None and XP1 == XP2:
        score += 2
    if DOI1!=None and DOI2!=None and DOI1 == DOI2:
        score += 1
    return score

def rule5(list1, list2, threshold):
    score = 0
    year1 = list1['publication_year']
    month1 = list1['publication_month']
    tit1 = list1['title']
    year2 = list2['publication_year']
    month2 = list2['publication_month']
    tit2 = list2['title']
    if year1!=None and year2!=None and year1 == year2:
        score += 2
        if month1!=None and month2!=None and month1 == month2:
            score += 2
            if type(tit1) == str and type(tit2) == str and diff.SequenceMatcher(None,tit1.lower(), tit2.lower()).quick_ratio() >= threshold:
                score += 3
        else:
            if type(tit1) == str and type(tit2) == str and diff.SequenceMatcher(None,tit1.lower(), tit2.lower()).quick_ratio() >= threshold:
                score += 2
    else:
        if month1!=None and month2!=None and month1 == month2:
            score += 1
            if type(tit1) == str and type(tit2) == str and diff.SequenceMatcher(None,tit1.lower(), tit2.lower()).quick_ratio() >= threshold:
                score += 2
    return score

def rule6(list1, list2,threshold):
    aut1 = list1['authors']
    vol1 = list1['volume']
    jor1 = list1['journal']
    year1 = list1['publication_year']
    aut2 = list2['authors']
    vol2 = list2['volume']
    jor2 = list2['journal']
    year2 = list2['publication_year']

    score = 0
    if type(aut1) == str and type(aut2) == str and diff.SequenceMatcher(None,aut1.lower(), aut2.lower()).quick_ratio() >= threshold:
        score += 1
        if type(jor1) == str and type(jor2) == str and diff.SequenceMatcher(None,jor1.lower(),jor2.lower()).quick_ratio() >= threshold:
            score += 2
            if vol1!=None and vol2!=None and vol1 == vol2:
                score += 2
                if year1!=None and year2!=None and year1 == year2:
                    score += 2
            elif year1!=None and year2!=None and year1 == year2:
                score += 2
        elif vol1!=None and vol2!=None and vol1 == vol2:
            score += 1
            if  year1!=None and year2!=None and year1 == year2:
                score += 2
        elif  year1!=None and year2!=None and year1 == year2:
            score += 1
    elif type(jor1) == str and type(jor2) == str and diff.SequenceMatcher(None,jor1.lower(),jor2.lower()).quick_ratio() >= threshold:
        score += 1
        if vol1!=None and vol2!=None and vol1 == vol2:
            score += 2
            if  year1!=None and year2!=None and year1 == year2:
                score += 2
        elif  year1!=None and year2!=None and year1 == year2:
            score += 1
    elif vol1!=None and vol2!=None and vol1 == vol2:
        score += 1
        if  year1!=None and year2!=None and year1 == year2:
            score += 2
    elif  year1!=None and year2!=None and year1 == year2:
        score += 1

    return score

def rule7(list1, list2, threshold):
    tit1 = list1['title']
    pag1 = list1['pages']
    tit2 = list2['title']
    pag2 = list2['pages']
    score = 0
    if type(tit1) == str and type(tit2) == str and diff.SequenceMatcher(None,tit1.lower(), tit2.lower()).quick_ratio() >= threshold:
        score += 2
        if pag1 == pag2:
            score += 3
    elif pag1 == pag2:
        score += 2
    return score
