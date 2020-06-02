import os
import pyodbc
import logging

logpath = r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\DU_Github\DXC_DU\WindowsService\test.log'
logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

conn = pyodbc.connect(r'DRIVER={ODBC Driver 13 for SQL Server};SERVER=GBPF0Y89C1\SQLEXPRESS;DATABASE=Miradors;Trusted_Connection=yes;User ID=EAD\\sahmed243;pwd=!M1r4d0r5N0rw1ch!;Trusted_Connection=no')
cursor = conn.cursor()
jobExistsQry = 'SELECT COUNT(*) FROM [Miradors].[dbo].[NewCurrentJobs]'
cursor.execute(jobExistsQry)
count = 0
for row in cursor:
    if row[0] != 0:
        count += 1
    else:
        count = 0

if count > 0:
    curJobQry = 'SELECT TOP 1 * FROM [Miradors].[dbo].[NewCurrentJobs]'
    logging.info('Checking for new jobs in NewCurrentJobs table ...')
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
    updQry = 'INSERT INTO [Miradors].[dbo].[NewRepostatus] (DrivePath, NumberOfFiles, SizeOfFiles)' + ' VALUES(' + "'" + str(jobpath) + "'" + ',' + str(total_count) + ',' + str(round(total_size/1024/1024,2)) + ')'
    cursor.execute(updQry)
    conn.commit()

    logging.info('Step 4 - Removing job from CurrentJobs Table for path: ' + jobpath)
    deleteJobQry = "delete from [Miradors].[dbo].[NewCurrentJobs] WHERE PathID = " + str(jobid)
    cursor.execute(deleteJobQry)
    conn.commit()

    logging.info('Step 5 - Successfully completed DU scan for path: ' + jobpath)
    cursor.close()
    conn.close()
else:
    logging.info('No DU jobs available ... ')
