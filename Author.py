from difflib import SequenceMatcher as sm

test = ['Codd', 'et al', 'research', 'Codd et al']

def getBestOption(list):
    option = list[0]
    totals = []
    i = 0
    while i < len(list):
        stri = list[i].lower()
        total = []
        j = i + 1
        while j < len(list):
            strj = list[j].lower()
            match = sm(None, stri, strj).ratio()
            if match > 0.8:
                total.append(strj)
            j += 1
        totals.append(total)    
        i += 1
    a = []
    for k in totals:
        a.append(len(k))
    b = a.index(max(a))
    if max(a) > 0:
        option = list[b]
    return option

print(getBestOption(test))