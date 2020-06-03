import os
import pyodbc
import logging
import time

logpath = r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\DU_Github\DXC_DU\WindowsService\MAIN.log'
logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

conn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                      "Server=GBPF0Y89C1\\SQLEXPRESS;"
                      "Database=DriveExplorer;"
                      "User ID=EAD\\sahmed243;"
                      "Trusted_Connection=yes;")
cursor = conn.cursor()

jobExistsQry = 'SELECT COUNT(*) FROM [DriveExplorer].[dbo].[CurrentJobs]'
cursor.execute(jobExistsQry)
count = 0
for row in cursor:
    if row[0] != 0:
        count += 1
    else:
        count = 0

if count > 0:
    curJobQry = 'SELECT TOP 1 * FROM [DriveExplorer].[dbo].[CurrentJobs]'
    logging.info('Checking for new jobs in CurrentJobs table ...')
    cursor.execute(curJobQry)
    jobid = 1
    jobpath = ''

    for row in cursor:
        logging.info('Step 1 - Found job for PathID: ' + str(row.PathID) + ', path: ' + row.Path)
        jobid = row.PathID
        jobpath = row.Path

    logging.info('Step 2 - Running DU Scan for path: ' + row.Path)
    total_size = 0
    total_count = 0
    for dirpath, dirnames, filenames in os.walk(jobpath):
        for filename in filenames:
            fp = os.path.join(dirpath, filename)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
                total_count += 1

    logging.info('Step 3 - Updating Repostatus table DU figures')
    updQry = 'INSERT INTO [DriveExplorer].[dbo].[Repostatus] (DrivePath, NumberOfFiles, SizeOfFiles)' + ' VALUES(' + "'" + str(jobpath) + "'" + ',' + str(total_count) + ',' + str(round(total_size/1024/1024,2)) + ')'
    cursor.execute(updQry)
    conn.commit()

    logging.info('Step 4 - Removing job from CurrentJobs Table for path: ' + jobpath)
    deleteJobQry = "DELETE FROM [DriveExplorer].[dbo].[CurrentJobs] WHERE PathID = " + str(jobid)
    cursor.execute(deleteJobQry)
    conn.commit()

    logging.info('Step 5 - Successfully completed DU scan for path: ' + jobpath)
    cursor.close()
    conn.close()
