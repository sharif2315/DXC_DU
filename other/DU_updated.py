import os
import pyodbc

conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=GBPF0Y89C1\\SQLEXPRESS;"
                      "Database=Miradors;"
                      "Trusted_Connection=yes;")
cursor = conn.cursor()

class DU:
    def __init__(self, path, DU_FileCount, DU_FileSize):
        self.path = path
        self.DU_FileCount = DU_FileCount
        self.DU_FileSize = DU_FileSize

    def runDiskUsage(self):
        # conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
        #                       "Server=GBPF0Y89C1\\SQLEXPRESS;"
        #                       "Database=Miradors;"
        #                       "Trusted_Connection=yes;")
        cursor = conn.cursor()
        total_size = 0
        total_count = 0
        for dirpath, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                fp = os.path.join(dirpath, filename)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    self.DU_FileSize += os.path.getsize(fp)
                    self.DU_FileCount += 1
        updQry = 'INSERT INTO [Miradors].[dbo].[NewRepostatus] (DrivePath, NumberOfFiles, SizeOfFiles)' + ' VALUES(' + "'" + str(self.path) + "'" + ',' + str(self.DU_FileCount) + ',' + str(round(self.DU_FileSize/1024/1024,2)) + ')'
        # print(updQry)
        cursor.execute(updQry)
        conn.commit()
        # cursor.close()
        # conn.close()


def runDU(id, path):
    total_size = 0
    total_count = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            fp = os.path.join(dirpath, filename)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
                total_count += 1
    updQry = 'INSERT INTO [Miradors].[dbo].[NewRepostatus] (DrivePath, NumberOfFiles, SizeOfFiles)' + ' VALUES(' + "'" + str(path) + "'" + ',' + str(total_count) + ',' + str(round(total_size/1024/1024,2)) + ')'
    print(updQry)
    cursor.execute(updQry)
    conn.commit()


curJobQry = 'SELECT TOP 1 * FROM [Miradors].[dbo].[NewCurrentJobs]'
cursor.execute(curJobQry)

for row in cursor:
    jobid = path = row.PathID
    jobpath = row.Path

total_size = 0
total_count = 0
for dirpath, dirnames, filenames in os.walk(jobpath):
    for filename in filenames:
        fp = os.path.join(dirpath, filename)
        # skip if it is symbolic link
        if not os.path.islink(fp):
            total_size += os.path.getsize(fp)
            total_count += 1
updQry = 'INSERT INTO [Miradors].[dbo].[NewRepostatus] (DrivePath, NumberOfFiles, SizeOfFiles)' + ' VALUES(' + "'" + str(jobpath) + "'" + ',' + str(total_count) + ',' + str(round(total_size/1024/1024,2)) + ')'
print(updQry)
cursor.execute(updQry)
conn.commit()

# firstpath = DU(jobpath, 0, 0)
# firstpath.runDiskUsage()
# runDU(jobid, jobpath)
deleteJobQry = "delete from [Miradors].[dbo].[NewCurrentJobs] WHERE PathID = " + str(jobid)
# print(deleteJobQry)
cursor.execute(deleteJobQry)
conn.commit()
cursor.close()
conn.close()
