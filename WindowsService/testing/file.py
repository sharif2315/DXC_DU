import socket
import win32serviceutil
import servicemanager
import win32event
import win32service
import os
import pyodbc
import shutil
import time
import random
from pathlib import Path
import logging
#from SMWinservice import SMWinservice


class SMWinservice(win32serviceutil.ServiceFramework):
    '''Base class to create winservice in Python'''

    _svc_name_ = 'pythonService'
    _svc_display_name_ = 'Python Service'
    _svc_description_ = 'Python Service Description'

    @classmethod
    def parse_command_line(cls):
        '''
        ClassMethod to parse the command line
        '''
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        '''
        Constructor of the winservice
        '''
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        '''
        Called when the service is asked to stop
        '''
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        '''
        Called when the service is asked to start
        '''
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        '''
        Override to add logic before the start
        eg. running condition
        '''
        pass

    def stop(self):
        '''
        Override to add logic before the stop
        eg. invalidating running condition
        '''
        pass

    def main(self):
        '''
        Main class to be ovverridden to add logic
        '''
        pass


class PythonCornerExample(SMWinservice):
    _svc_name_ = "ExcelFileMoverService"
    _svc_display_name_ = "Excel File Mover Service"
    _svc_description_ = "Moves xlsx files into archive folder"

    def movefiles(self):
        mypath = r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\excel_Import\test'
        myarchive = r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\excel_Import\test\archive'
        filelist = []
        # reading directory
        for dirpath, dirnames, filenames in os.walk(mypath):
            for filename in filenames:
                # Reading directory for only xlsx files which are in dir test
                if (filename.lower().endswith('.xlsx')) and (dirpath == mypath):
                    filepath = dirpath + '\\' + filename
                    filelist.append(filepath)
                else:
                    continue

        for file in filelist:
            filename = os.path.basename(file)
            shutil.move( file, str(myarchive + '\\' + filename) )
            #print('File: ' + str(file) + ' has been successfully moved to archive folder')
            print('File: ' + str(filename) + ' has been successfully moved to archive folder')

    def start(self):
        self.isrunning = True
        self.isrunning = True
        logpath = r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\DU_Github\DXC_DU\WindowsService\MAIN.log'
        logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
        logging.info('Successfully started Python DU Service')

    def stop(self):
        self.isrunning = False
        logpath = r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\DU_Github\DXC_DU\WindowsService\MAIN.log'
        logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')
        logging.info('Stopping Python DU Service')
        time.sleep(25)
        if self.isrunning == False:
            logging.info('Successfully stopped Python DU Service')

    def main(self):
        #
        #movefiles()
        #i = 0
        while self.isrunning:
            try:
                logpath = r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\DU_Github\DXC_DU\WindowsService\MAIN.log'
                logging.basicConfig(filename=logpath, level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

                conn = pyodbc.connect("Driver={ODBC Driver 13 for SQL Server};"
                                      "Server=GBPF0Y89C1\\SQLEXPRESS;"
                                      "Database=DriveExplorer;"
                                      "User ID=EAD\\sahmed243;"
                                      "Trusted_Connection=yes;")
                cursor = conn.cursor()

                jobExistsQry = 'SELECT COUNT(*) FROM [DriveExplorer].[dbo].[diskUsage_currentjobs]'
                cursor.execute(jobExistsQry)
                count = 0
                for row in cursor:
                    if row[0] != 0:
                        count += 1
                    else:
                        count = 0

                if count > 0:
                    curJobQry = 'SELECT TOP 1 * FROM [DriveExplorer].[dbo].[diskUsage_currentjobs]'
                    logging.info('Checking for new jobs in CurrentJobs table ...')
                    cursor.execute(curJobQry)
                    jobid = 1
                    jobpath = ''

                    for row in cursor:
                        # logging.info('Step 1 - Found job for PathID: ' + str(row.PathID) + ', path: ' + row.Path)
                        logging.info('Step 1 - Found job for path: ' + row.path)
                        jobid = row.id
                        jobpath = row.path

                    logging.info('Step 2 - Running DU Scan for path: ' + row.path)
                    total_size = 0
                    total_count = 0
                    for dirpath, dirnames, filenames in os.walk(jobpath):
                        for filename in filenames:
                            fp = os.path.join(dirpath, filename)
                            if not os.path.islink(fp):
                                total_size += os.path.getsize(fp)
                                total_count += 1

                    logging.info('Step 3 - Updating Repostatus table DU figures')
                    updQry = 'INSERT INTO [DriveExplorer].[dbo].[diskUsage_repostatus] (drivePath, numOfFiles, sizeOfFiles)' + ' VALUES(' + "'" + str(jobpath) + "'" + ',' + str(total_count) + ',' + str(round(total_size/1024/1024,2)) + ')'
                    cursor.execute(updQry)
                    conn.commit()

                    logging.info('Step 4 - Removing job from CurrentJobs Table for path: ' + jobpath)
                    deleteJobQry = "DELETE FROM [DriveExplorer].[dbo].[diskUsage_currentJobs] WHERE id = " + str(jobid)
                    cursor.execute(deleteJobQry)
                    conn.commit()

                    logging.info('Step 5 - Successfully completed DU scan for path: ' + jobpath)
                    cursor.close()
                    conn.close()
                else:
                    if self.isrunning == True:
                        logging.info('No DU jobs available ... ')
                        time.sleep(15)


            except Exception as e:
                logging.info(e)
                stop(self)



if __name__ == '__main__':
    PythonCornerExample.parse_command_line()
