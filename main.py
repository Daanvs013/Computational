###
### Group 21
###


## modules
import tqdm 
import pandas as pd
import rules as rf
import functions as f
from classes import metatable, scoretable, clustertable
from conn import conn
import concurrent.futures
import multiprocessing as mp
from itertools import repeat

def metadataExtraction(id,row):
    ## function to extract metadata from a string, after each metadata is found, we remove it from the string and continue looking for new metadata
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
    issue = f.getIssue(row)
    if issue!= None:
        row = row.replace(str(issue),'')
        row = row.replace('()','')
    volume = f.getVol(row)
    if volume!= None:
        row = row.replace(str(volume),'')
        row = row.replace('vol','')
    authors = f.getAuthor(row)
    if authors!=None:
        row = row.replace(str(authors),'')
    journal = f.getJournal(row)
    if journal!= None:
        row = row.replace(str(journal),'')
    title = f.getTitle(row)
    if title!= None:
        row = row.replace(str(title),'')
    return {"id":id,"authors":authors,"title":title,"volume":volume,"issue":issue,"pages":pages,"publication_year":year,"publication_month":month,"issn":issn,"isbn":isbn,"xp":xp,"doi":doi,"journal":journal}

def getScore(table,info1):
    ## function to apply our matching rules and calculate a machting score between 2 rows in our metadata table
    validator = {"authors":info1[1],"title":info1[2],"journal":info1[3],"volume":info1[4],"issue":info1[5],"pages":info1[6],"publication_year":info1[7],"publication_month":info1[8],"issn":info1[9],"isbn":info1[10],"xp":info1[11],"doi":info1[12],"index":info1[13]}
    scores = []
    for index,row in table.iterrows():
        score = 0
        score += rf.rule1(validator, row)
        #print(score)
        score += rf.rule2(validator, row, 0.8)
        #print(score)
        score += rf.rule3(validator, row, 0.8)
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
        ##print(f"---- Adding metadata to the table:")
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
    clusters = clustertable("cluster_table",num)
    threshold = 10
    k = 0
    c = 0
    print("---- Creating clusters:")
    for k in tqdm.tqdm( range(0,len(scores.df))):
        
        clusters.df.iloc[k,0] = metadata.df.loc[k,'npl_publn_id']
        clusters.df.iloc[k,3] = dataset.loc[k,"npl_biblio"]
        if clusters.df.iloc[k,1] == 0:
            c += 1
            clusters.df.iloc[k,1] = c
        m = k + 1
        while m <  len(scores.df):
            if scores.df.iloc[m,k] > threshold:
                if clusters.df.iloc[m,2] < scores.df.iloc[m,k]:
                    clusters.df.iloc[m,1] = c
                    clusters.df.iloc[m,2] = scores.df.iloc[m,k]
            m += 1
        k += 1
    clusters.df = clusters.df.drop("Max Score", axis=1)

    """ Part IV Results"""
    #metadata.toCSV()
    metadata.insertIntoDB()
    #scores.toCSV()
    #scores.insertIntoDB()
    #clusters.toCSV()
    clusters.insertIntoDB()
    conn.close()

## only run main function if this script is directly executed by user, so importing this file does not trigger this function
if __name__ == '__main__':
    ## multiprocessing
    cores = mp.cpu_count()

    ## retrieve dataset from the databse
    data_set = 'Patstat_golden_set'
    sql_query = f'select * from {data_set}'
    sample_size = 1000
    df = pd.read_sql(sql_query,conn).head(sample_size)
    print(f'---- data set: {data_set}')
    print(f'---- Sample size: {sample_size}')
    ## start main function
    main(df)

    
################## after running this file, please run validate_final.py for the exercises on validation
