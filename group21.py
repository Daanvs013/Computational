## modules
import pyodbc as db
import pandas as pd
import re
from functions import removeSpaces

## establish connection
server= 'uvtsql.database.windows.net'
database = 'db3'
user = 'user97'
db_password = 'CompEco1234'

conn = db.connect('Driver={SQL Server};'
                f'Server={server};'
                f'Database={database};'
                f'uid={user};'
                f'pwd={db_password};')


sql_query = 'select * from Patstat_golden_set'
df = pd.read_sql(sql_query,conn)
print(df)
for index,row in df.iterrows():
    print(row)



print(removeSpaces('test   tes     safsd sss     ss  s  s  test'))

## close connection
conn.close()