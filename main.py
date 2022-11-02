###
### Group 21
###


## modules
import tqdm 
import pandas as pd
import rules as rf
import functions as f
from classes import metatable, scoretable
from timeit import default_timer as timer
from conn import conn
import concurrent.futures
import multiprocessing as mp
from itertools import repeat
import os

def metadataExtraction(id,row):
    doi = f.getDOI(row)
    if doi != None:
        row = row.replace(str(doi),'')
    xp = f.getXP(row)
    if xp!= None:
        row = row.replace(str(xp),'')
    issn = f.getISSN(row)
    if issn!= None:
        row = row.replace(str(issn),'')
    isbn = f.getISBN(row)
    if isbn!= None:
        row = row.replace(str(isbn),'')
    pages = f.getPages(row)
    if pages!= None:
        row = row.replace(str(pages),'')
    year = f.getYear(row)
    if year!= None:
        row = row.replace(str(year),'')
    month = f.getMonth(row)
    if month!= None:
        row = row.replace(str(month),'')
    volume = f.getVol(row)
    if volume!= None:
        row = row.replace(str(volume),'')
    issue = f.getIssue(row)
    if issue!= None:
        row = row.replace(str(issue),'')
    authors = f.getAuthor(row)
    if authors!=None:
        row = row.replace(str(authors),'')
    title = f.getTitle(row)
    if title!= None:
        row = row.replace(str(title),'')
    journal = None
    return {"id":id,"authors":authors,"title":title,"volume":volume,"issue":issue,"pages":pages,"publication_year":year,"publication_month":month,"issn":issn,"isbn":isbn,"xp":xp,"doi":doi,"journal":journal}

def getScore(table,info1):
    validator = {"authors":info1[1],"title":info1[2],"journal":info1[3],"volume":info1[4],"issue":info1[5],"pages":info1[6],"publication_year":info1[7],"publication_month":info1[8],"issn":info1[9],"isbn":info1[10],"xp":info1[11],"doi":info1[12],"index":info1[13]}
    scores = []
    for index,row in table.iterrows():
        score = 0
        score += rf.rule1(validator, row)
        #print(score)
        score += rf.rule2(validator, row, 0.8)
        #print(score)
        #score += rf.rule3(validator, row, 0.8)
        #print(score)
        score += rf.rule4(validator, row)
        #print(score)
        score += rf.rule5(validator, row, 0.8)
        #print(score)
        score += rf.rule6(validator, row, 0.8)
        #print(score)
        score += rf.rule7(validator, row, 0.8)
        #print(score)
        scores.append(score)
    return {"index":info1[13],"scores":scores}

def main(dataset):   
    num = len(dataset)

    """ Part I Extract Metadata"""
    ## create a class which functions as our metadata table
    metadata = metatable("metadata_table")
    print(f"---- Creating metadata:")
    ## we are using multiprocessing, normally python only runs on one of the cpu cores
    ## by using the module concurrent.futures, we can easily partition our dataset and run the partitions on individual subprocesses on each cpu core
    ## we are applying the fuction metadataExtraction simulatously to all chunks, hence reducing the runtime significantly
    with concurrent.futures.ProcessPoolExecutor(cores) as executor:
        ## tqdm is for a fancy progress bar
        ## executor.map handles all the partitioning and collection of the data from each subprocess
        results = list(tqdm.tqdm(executor.map(metadataExtraction,dataset["npl_publn_id"],dataset['npl_biblio'], chunksize=10)))
        for result in results:
            ## add the extracted metadata to the metadata dataframe
            metadata.addEntry(result["id"],result["authors"],result["title"],result["journal"],result["volume"],result["issue"],result["pages"],result["publication_year"],result["publication_month"],result["issn"],result["isbn"],result["xp"],result["doi"])

    """ Part II Matching scores"""
    ## We create a matrix in which the similarity of all entries are calculated based on scores given by the rules
    ## We get all these scores in a n*n matrix  

    scores = scoretable("score_table",num)
    metadata.df['index'] = metadata.df.index ## create helper column
    print(f"---- Creating scoretable:")
    ## we are again using multiprocessing
    with concurrent.futures.ProcessPoolExecutor(cores) as executor:
        results = list(tqdm.tqdm(executor.map(getScore,repeat(metadata.df),metadata.df.values,chunksize=10)))
        for result in results:
            ##print(result)
            scores.updateEntry(result["index"],result['scores']) 
    metadata.df = metadata.df.drop(['index'],axis=1) ## remove helper column


    """ Part III Clustering"""
    clusters = pd.DataFrame(data = 0, index=range(0,num), columns=['npl_publn_id', 'cluster_id',"npl_biblio",'Max Score'])
    threshold = 10
    k = 0
    c = 0
    print("---- Creating clusters:")
    for k in tqdm.tqdm( range(0,len(scores.df))):
        
        clusters.iloc[k,0] = metadata.df.loc[k,'npl_publn_id']
        clusters.iloc[k,3] = dataset.loc[k,"npl_biblio"]
        if clusters.iloc[k,1] == 0:
            c += 1
            clusters.iloc[k,1] = c
        m = k + 1
        while m <  len(scores.df):
            if scores.df.iloc[m,k] > threshold:
                if clusters.iloc[m,2] < scores.df.iloc[m,k]:
                    clusters.iloc[m,1] = c
                    clusters.iloc[m,2] = scores.df.iloc[m,k]
            m += 1
        k += 1
    ##print(clusters)

    """ Part IV Results"""
    #metadata.toCSV()
    metadata.insertIntoDB()
    #scores.toCSV()
    #scores.insertIntoDB()
    #clusters.to_csv("CSV\cluster_table.csv")
    clusters.to_sql("group21_cluster_table",con=conn,if_exists='replace')
    #print(f"---- Cluster table written to file {os.getcwd()}\CSV\cluster_table.csv")
    print(f"---- Cluster table inserted into the SQL DB with the name 'group21_cluster_table'")
    conn.close()

## only run main function if this script is directly executed by user, so importing this file does not trigger this function
if __name__ == '__main__':
    ## multiprocessing
    cores = mp.cpu_count()

    ## retrieve dataset from the databse
    data_set = 'Patstat'
    sql_query = f'select * from {data_set}'
    sample_size = pd.read_sql(f'select count(*) from {data_set}',conn).loc[0][0]
    n = input("How many samples should we run? insert 'all' for the entire dataset")
    if n != 'all':
        sample_size = int(n)
    df = pd.read_sql(sql_query,conn).head(sample_size)
    print(f'---- data set: {data_set}')
    print(f'---- Sample size: {sample_size}')
    ## start main function
    main(df)