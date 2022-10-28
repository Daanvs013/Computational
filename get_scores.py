import rule_functions as rf
import pandas as pd
import numpy as np

d = {'npl_id':[1,2,3,4], 'author':['jan','piet','bas',np.nan], 'title':['hocus','pocus','pas','hocus'],
'journal':['sci','science',np.nan,'science'], 'volume':[1,4,19,np.nan], 'issue':[4,np.nan,np.nan,4],
'pagina':['200','205','3','200'], 'jaar':[np.nan, 2019,1999,1999], 'month':[np.nan,2,np.nan,np.nan],
'ISSN':[2,4,7,2], 'ISBN':[np.nan,np.nan,np.nan,np.nan], 'XP':[np.nan, np.nan, 3, 8], 'DOI':[np.nan,np.nan,np.nan,np.nan]}
df = pd.DataFrame(data = d)
column = range(len(df.index))
scores = pd.DataFrame(data = 0, index=column, columns=column)

i = 0
while i < len(df.index):
    info1 = df.iloc[[i]].values.flatten().tolist()
    j = i + 1
    while j < len(df.index):
        info2 = df.iloc[[j]].values.flatten().tolist()
        score = 0
        score += rf.rule1(info1, info2)
        score += rf.rule2(info1, info2, 0.8)
        score += rf.rule3(info1, info2, 0.8)
        score += rf.rule4(info1, info2)
        score += rf.rule5(info1, info2, 0.8)
        score += rf.rule6(info1, info2, 0.8)
        score += rf.rule7(info1, info2, 0.8)
        scores.iloc[i,j] = score
        scores.iloc[j,i] = score
        #print(scores)
        j += 1
        
    i += 1


