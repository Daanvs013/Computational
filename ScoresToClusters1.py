import rule_functions as rf
import pandas as pd
import numpy as np
import get_scores as gs 

column = range(0, len(gs.df.index)) 
clusters = pd.DataFrame(data = 0, index=column, columns=['ID', 'Cluster','Max Score'])
scores = gs.scores
print(scores)
print(clusters)
k = 0
c = 0
while k < len(scores.index):
    clusters.iloc[k,0] = k
    if clusters.iloc[k,1] == 0:
        c += 1
        clusters.iloc[k,1] = c
    m = k + 1
    while m <  len(scores.index):
        if scores.iloc[m,k] > 10: # threshold kan worden veranderd
            if clusters.iloc[m,2] < scores.iloc[m,k]:
                clusters.iloc[m,1] = c
                clusters.iloc[m,2] = scores.iloc[m,k]
        m += 1
    k += 1

print(clusters)


