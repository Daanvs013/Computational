# [author, title, journal, volume, issue, pagina, jaar, month, ISSN, XP, DOI]
import pandas as pd
from difflib import SequenceMatcher as sm
import regex as re
import math

def rule1(list1, list2):
    score = 0
    vol1 = list1[3]
    pag1 = list1[5]
    iss1 = list1[4]
    vol2 = list2[3]
    pag2 = list2[5]
    iss2 = list2[4]
    if math.isnan(vol1) == False and math.isnan(vol2) == False == False and vol1 == vol2:
        score += 1
        if pag1 == pag2:
            score += 2
            if math.isnan(iss1) == False and math.isnan(iss2) == False and iss1 == iss2:
                score += 3
    else:
        if pag1 == pag2:
            score += 1
            if math.isnan(iss1) == False and math.isnan(iss2) == False and iss1 == iss2:
                score += 1
        elif math.isnan(iss1) == False and math.isnan(iss2) == False and iss1 == iss2:
            score += 1
    return score

def rule2(list1, list2, threshold):
    score = 0
    aut1 = list1[0]
    tit1 = list1[1]
    aut2 = list2[0]
    tit2 = list2[1]
    test = type(tit1) == str and type(tit2) == str and sm(None,tit1.lower(), tit2.lower()).ratio() >= threshold
    test2 = sm(tit1.lower(), tit2.lower()).ratio()
    if  test:
        score += 3
        if type(aut1) == str and type(aut2) == str and sm(None,aut1.lower(), aut2.lower()).ratio() >= threshold:
            score += 2
        else:
            score -= 1
    elif type(aut1) == str and type(aut2) == str and sm(None,aut1.lower(), aut2.lower()).ratio() >= threshold:
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
    if sm(num1,num2).ratio() >= threshold:
        score += 2
    return score

def rule4(list1, list2):
    score = 0
    ISSN1 = list1[8]
    XP1 = list1[9]
    DOI1 = list1[10]
    ISSN2 = list2[8]
    XP2 = list2[9]
    DOI2 = list2[10]
    if math.isnan(ISSN1) == False and math.isnan(ISSN2) == False and ISSN1 == ISSN2:
        score += 2
    if math.isnan(XP1) == False and math.isnan(XP2) == False and XP1 == XP2:
        score += 2
    if math.isnan(DOI1) == False and math.isnan(DOI2) == False and DOI1 == DOI2:
        score += 1
    return score

def rule5(list1, list2, threshold):
    score = 0
    year1 = list1[6]
    month1 = list1[7]
    tit1 = list1[1]
    year2 = list2[6]
    month2 = list2[7]
    tit2 = list2[1]
    if math.isnan(year1) == False and math.isnan(year2) == False and year1 == year2:
        score += 2
        if math.isnan(month1) == False and math.isnan(month2) == False and month1 == month2:
            score += 2
            if type(tit1) == str and type(tit2) == str and sm(None,tit1.lower(), tit2.lower()).ratio() >= threshold:
                score += 3
        else:
            if type(tit1) == str and type(tit2) == str and sm(None,tit1.lower(), tit2.lower()).ratio() >= threshold:
                score += 2
    else:
        if math.isnan(month1) == False and math.isnan(month2) == False and month1 == month2:
            score += 1
            if type(tit1) == str and type(tit2) == str and sm(None,tit1.lower(), tit2.lower()).ratio() >= threshold:
                score += 2
    return score

def rule6(list1, list2,threshold):
    aut1 = list1[0]
    vol1 = list1[3]
    jor1 = list1[2]
    year1 = list1[6]
    aut2 = list2[0]
    vol2 = list2[3]
    jor2 = list2[2]
    year2 = list2[6]

    score = 0
    if type(aut1) == str and type(aut2) == str and sm(None,aut1.lower(), aut2.lower()).ratio() >= threshold:
        score += 1
        if type(jor1) == str and type(jor2) == str and sm(None,jor1.lower(),jor2.lower()).ratio() >= threshold:
            score += 2
            if math.isnan(vol1) == False and math.isnan(vol2) == False and vol1 == vol2:
                score += 2
                if math.isnan(year1) == False and math.isnan(year2) == False and year1 == year2:
                    score += 2
            elif math.isnan(year1) == False and math.isnan(year2) == False and year1 == year2:
                score += 2
        elif math.isnan(vol1) == False and math.isnan(vol2) == False and vol1 == vol2:
            score += 1
            if  math.isnan(year1) == False and math.isnan(year2) == False and year1 == year2:
                score += 2
        elif  math.isnan(year1) == False and math.isnan(year2) == False and year1 == year2:
            score += 1
    elif type(jor1) == str and type(jor2) == str and sm(None,jor1.lower(),jor2.lower()).ratio() >= threshold:
        score += 1
        if math.isnan(vol1) == False and math.isnan(vol2) == False and vol1 == vol2:
            score += 2
            if  math.isnan(year1) == False and math.isnan(year2) == False and year1 == year2:
                score += 2
        elif  math.isnan(year1) == False and math.isnan(year2) == False and year1 == year2:
            score += 1
    elif math.isnan(vol1) == False and math.isnan(vol2) == False and vol1 == vol2:
        score += 1
        if  math.isnan(year1) == False and math.isnan(year2) == False and year1 == year2:
            score += 2
    elif  math.isnan(year1) == False and math.isnan(year2) == False and year1 == year2:
        score += 1

    return score

def rule7(list1, list2, threshold):
    tit1 = list1[1]
    pag1 = list1[5]
    tit2 = list2[1]
    pag2 = list2[5]
    score = 0
    if type(tit1) == str and type(tit2) == str and sm(None,tit1.lower(), tit2.lower()).ratio() >= threshold:
        score += 2
        if pag1 == pag2:
            score += 3
    elif pag1 == pag2:
        score += 2
    return score
