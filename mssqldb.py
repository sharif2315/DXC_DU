import pyodbc
import pandas as pd

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=GBPF0Y89C1\\SQLEXPRESS;"
                      "Database=Miradors;"
                      "Trusted_Connection=yes;")

#cursor = conn.cursor()
#qry = cursor.execute('  SELECT TOP 1 * FROM [Miradors].[dbo].[Repository]')

df = pd.read_sql_query('SELECT TOP 1 * FROM [Miradors].[dbo].[Repository]', conn)

uncPath = df['UNCPath'].iloc[0]

print(uncPath)
