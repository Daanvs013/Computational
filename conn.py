###
### Group 21
###


## modules
from sqlalchemy import create_engine
import pandas as pd

## establish connection
server= 'uvtsql.database.windows.net'
database = 'db3'
user = 'user97'
db_password = 'CompEco1234'
driver = 'SQL Server Native Client 11.0'
db_connection = f'mssql://{user}:{db_password}@{server}/{database}?driver={driver}'
engine = create_engine(db_connection)
conn = engine.connect()