import pyodbc as db
import matplotlib.pyplot as plt
conn = None
conn = db.connect('Driver={SQL Server};'
                'Server=uvtsql.database.windows.net;'
                'Database=db3;' #change to your own database
                'uid=user95;' #change to your username
                'pwd=CompEco1234;')

import pandas as pd
import numpy as np

validation_set = pd.read_sql("select * from Patstat_golden_set",conn)
to_validate = pd.read_sql("select * from group21_cluster_table",conn)

def PredictedToGolden(df1, df2):
    df1 = df1.drop('index', axis = 1)                                                       # Index dropped for easier navigating of dataframe
    df3 = pd.DataFrame({"npl_publn_id":[],"cluster_id":[]})                                 # Create a new dataframe to store our clusters with clusterID's corresponding to golden_set
    i = 0 
    while len(df1)>0:
        cluster = df1.iloc[i,1]                                                             # Take the first row of our predicted clusters
        options = np.array(df1.loc[df1["cluster_id"] == cluster,"npl_publn_id"])             # Find all ID's which share the clusterID
        ClusterOptions = df2[df2.npl_publn_id.isin(options)]                                 # Find the corresponding clusterID's of these ID's in the golden set
        grouped = ClusterOptions.groupby(["cluster_id"]).count()                            # Get the clusterID which corresponds most often
        maxclus = grouped[grouped.npl_publn_id == grouped["npl_publn_id"].max()].index[0]     

        # Append all ID's which now have a corresponding clusterID from the golden set
        # Drop these ID's from our predicted set
        for j in options:
            df4 = pd.DataFrame({"npl_publn_id":[j],"cluster_id":[maxclus]})
            df3 = pd.concat([df3, df4], ignore_index=True)
            drop = df1.index[df1["npl_publn_id"] == j][0]
            df1 = df1.drop(drop)


    return df3.sort_values("npl_publn_id")

to_validate = PredictedToGolden(to_validate,validation_set)

print(to_validate)

df5 = to_validate
df6 = validation_set
h = {"cluster_id":[], "precision": [], "recall": [], "f1_measure": []}                      
score_cluster = pd.DataFrame(h)                                                             # Create dataframe to house clusterID's with corresponding scores

i = 1
total_true_positive = 0                                                                     # variables to keep count of these terms
total_false_negative = 0
total_false_positive = 0
while i <= df5['cluster_id'].max():                                                         # loop for all clusters
    a = df5[df5['cluster_id'] == i]

    b = df6[df6['cluster_id'] == i]
    predicted_id = a.npl_publn_id.values.tolist()
    golden_id = b.npl_publn_id.values.tolist()
    false_negative = 0
    false_positive = 0
    true_positive = 0
    for j in golden_id:                                                                     # in this loop, npl_publn_ids in golden_set are compared to those in our set for each cluster
        if j in predicted_id:                                                               # to find true positives (npl_publn_id in both sets' cluster) and false negatives (npl_publn_id in golden_set's cluster but not in ours)
            true_positive += 1
        elif j not in predicted_id:
            false_negative += 1
    for k in predicted_id:                                                                  # find false positives (npl_publn_id in our set's cluster, but not in golden_set's cluster)
        if k not in golden_id:
            false_positive += 1                                                             
        precision = true_positive/(true_positive+false_positive)                            # compute scores
        recall = true_positive/(true_positive+false_negative)
        f1_measure = 2*precision*recall/(precision+recall)
        x = pd.DataFrame({"cluster_id":[int(i)], "precision": [precision], "recall": [recall], "f1_measure": [f1_measure]})
        score_cluster = pd.concat([score_cluster, x], ignore_index=True)                    # store scores in dataframe
    total_true_positive += true_positive
    total_false_negative += false_negative
    total_false_positive += false_positive
    i += 1

# print results for 'third end product'
print(score_cluster)
print(score_cluster['f1_measure'].max())
print(list(score_cluster.loc[score_cluster['f1_measure'] == score_cluster['f1_measure'].max()]['cluster_id'])[0])
print(score_cluster['f1_measure'].min())
print(list(score_cluster.loc[score_cluster['f1_measure'] == score_cluster['f1_measure'].min()]['cluster_id'])[0]) 
print(total_true_positive, total_false_negative, total_false_positive, '\n',
score_cluster['precision'].mean(), score_cluster['recall'].mean(), score_cluster['f1_measure'].mean())

plt.plot(score_cluster["cluster_id"], score_cluster["f1_measure"])                          # create plots
plt.ylabel('f1_score')
plt.xlabel('integer cluster_id')
plt.show()

plt.plot(score_cluster["cluster_id"], score_cluster["precision"])
plt.ylabel('precision score')
plt.xlabel('integer cluster_id')
plt.show()

plt.plot(score_cluster["cluster_id"], score_cluster["recall"])
plt.ylabel('recall score')
plt.xlabel('integer cluster_id')
plt.show()
