import pandas as pd
import numpy as np
h = {"cluster_id":[], "precision": [], "recall": [], "f1_measure": []}
d = {"npl_publ_id":[1,2,3,4,5,6,7,8,9,10], "cluster_id":[1,1,2,3,2,3,3,4,5,5]}
f = {"npl_publ_id":[1,2,3,4,5,6,7,8,9,10], "cluster_id":[1,1,2,3,3,3,3,1,5,6]}


df1 = pd.DataFrame(d)
df2 = pd.DataFrame(f)
wrong_cluster = pd.DataFrame(h)

i = 1
while i < 7:
    a = df1[df1['cluster_id'] == i]
    b = df2[df2['cluster_id'] == i]
    predicted_id = a.npl_publ_id.values.tolist()
    golden_id = b.npl_publ_id.values.tolist()
    print('this is cluster {}'.format(i), '\n' , predicted_id, '\n',golden_id)
    false_negative = 0
    false_positive = 0
    true_positive=0
    for j in golden_id:
        if j in predicted_id:
            true_positive += 1
        elif j not in predicted_id:
            false_negative += 1
    for k in predicted_id:
        if k not in golden_id:
            false_positive += 1
    if true_positive>0:
        precision = true_positive/(true_positive+false_positive)
        recall = true_positive/(true_positive+false_negative)
        f1_measure = 2*precision*recall/(precision+recall)
        x = pd.DataFrame({"cluster_id":[i], "precision": [precision], "recall": [recall], "f1_measure": [f1_measure]})
        wrong_cluster = pd.concat([wrong_cluster, x], ignore_index=True)
    i += 1


print(wrong_cluster)

