import pyodbc
import pandas as pd

from epl_predictions.src.config.config import AZURE_SQL_CONNECTIONSTRING
from epl_predictions.src.utils.loader import Loader
    
connection_string = AZURE_SQL_CONNECTIONSTRING

l = Loader()
df = l.load_table_from_file("raw/current_table.csv")
df = df.drop(columns=["index", "Attendance", "Top Team Scorer", "Goalkeeper", "Notes"])
df["Date_posted"] = pd.to_datetime("today")
df["Season"] = "2024/2025"
# print(df)

conn = pyodbc.connect(connection_string)

cursor = conn.cursor()

for index, row in df.iterrows():
    cursor.execute("INSERT INTO [dbo].[league_table] (Indeks,Date_posted,Rk,Squad,MP,W,D,L,GF,GA,GD,Pts,Pts_MP,xG,xGA,xGD,xG_90,Last_5,Season) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", 
                   row["index.1"], row["Date_posted"], row["Rk"], row["Squad"], row["MP"], row["W"], row["D"], row["L"], row["GF"], row["GA"], row["GD"], row["Pts"], row["Pts/MP"], row["xG"], row["xGA"], row["xGD"], row["xGD/90"], row["Last 5"], row["Season"])
    
conn.commit()
cursor.close()