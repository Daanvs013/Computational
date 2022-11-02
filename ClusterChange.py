import pandas as pd
import numpy as np
d = {"npl_publ_id":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], "cluster_id":[2,3,5,5,7,9,10,3,3,4,11,12,2,8,8]}
f = {"npl_publ_id":[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15], "cluster_id":[22,23,25,25,27,29,30,23,23,24,31,32,22,28,28]}

df1 = pd.DataFrame(d)
df2 = pd.DataFrame(f)
df3 = pd.DataFrame({"npl_publ_id":[],"cluster_id":[]})

def PredictedToGolden(df1, df2):
    df3 = pd.DataFrame({"npl_publ_id":[],"cluster_id":[]})
    i = 0 
    while len(df1)>0:
        cluster = df1.iloc[i,1]                                                             # Take the first row of our predicted clusters
        options = np.array(df1.loc[df1["cluster_id"] == cluster,"npl_publ_id"])             # Find all ID's which share the clusterID
        ClusterOptions = df2[df2.npl_publ_id.isin(options)]                                 # Find the corresponding clusterID's of these ID's in the golden set
        grouped = ClusterOptions.groupby(["cluster_id"]).count()                            # Get the clusterID which corresponds most often
        maxclus = grouped[grouped.npl_publ_id == grouped["npl_publ_id"].max()].index[0]     

        # Append all ID's which now have a corresponding clusterID from the golden set
        # Drop these ID's from our predicted set
        for j in options:
            df4 = pd.DataFrame({"npl_publ_id":[j],"cluster_id":[maxclus]})
            df3 = pd.concat([df3, df4], ignore_index=True)
            drop = df1.index[df1["npl_publ_id"] == j][0]
            df1 = df1.drop(drop)


    return df3.sort_values("npl_publ_id")

print(PredictedToGolden(df1,df2))