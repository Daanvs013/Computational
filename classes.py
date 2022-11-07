###
### Group 21
###


##modules
import pandas as pd
from conn import conn
import os


##classes
class metatable:
    def __init__(self,name):
        self.df = pd.DataFrame({
            "npl_publn_id":[],
            "authors":[],
            "title":[],
            "journal":[],
            "volume":[],
            "issue":[],
            "pages":[],
            "publication_year":[],
            "publication_month":[],
            "issn":[],
            "isbn":[],
            "xp":[],
            "doi":[]
        })
        self.name = name
        self.sqlname = f"group21_extracted_bib_items"

    def addEntry(self,id,author,title,journal,volume,issue,pages,year,month,issn,isbn,xp,doi):
        row = pd.DataFrame({'npl_publn_id':[id],'authors':[author],'title':[title],'journal':[journal],'volume':[volume],'issue':[issue],'pages':[pages],'publication_year':[year],'publication_month':[month],'issn':[issn],'isbn':[isbn],'xp':[xp],'doi':[doi]})
        self.df = pd.concat([self.df,row], ignore_index=True)

    def insertIntoDB(self):
        self.df.to_sql(self.sqlname,con=conn,if_exists='replace')
        print(f"---- Metadata table inserted into the SQL DB with the name '{self.sqlname}'")

    def dropFromDB(self):
        conn.execute(f"drop table if exists {self.sqlname}")

    def toCSV(self):
        self.df.to_csv(f'CSV\{self.name}.csv')
        print(f"---- Metadata table written to file {os.getcwd()}\CSV\{self.name}.csv")

class scoretable:
    def __init__(self,name,length):
        self.df = pd.DataFrame(data = 0, index=range(0,length), columns=range(0,length))
        self.name = name
        self.sqlname = f"group21_{name}"

    def updateEntry(self,i,scores):
        for j in range(0,len(scores)):
            self.df.iloc[i,j] = scores[j]

    def insertIntoDB(self):
        self.df.to_sql(self.sqlname,con=conn,if_exists='replace')
        print(f"---- Score table inserted into the SQL DB with the name '{self.sqlname}'")

    def dropFromDB(self):
        conn.execute(f"drop table if exists {self.sqlname}")

    def toCSV(self):
        self.df.to_csv(f'CSV\{self.name}.csv')
        print(f"---- Score table written to file {os.getcwd()}\CSV\{self.name}.csv")

class clustertable:
    def __init__(self,name,length):
        self.df = pd.DataFrame(data = 0, index=range(0,length), columns=['npl_publn_id', 'cluster_id','Max Score',"npl_biblio",])
        self.name = name
        self.sqlname = f"group21_{name}"

    def insertIntoDB(self):
        self.df.to_sql(self.sqlname,con=conn,if_exists='replace')
        print(f"---- Cluster table inserted into the SQL DB with the name '{self.sqlname}'")

    def dropFromDB(self):
        conn.execute(f"drop table if exists {self.sqlname}")

    def toCSV(self):
        self.df.to_csv(f'CSV\{self.name}.csv')
        print(f"---- Cluster table written to file {os.getcwd()}\CSV\{self.name}.csv")
