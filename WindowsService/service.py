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
import datetime
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
    _svc_name_ = "PythonDU"
    _svc_display_name_ = "Python DU Service"
    _svc_description_ = "Python DU Service"


    # cursor = conn.cursor()

    def start(self):
        self.isrunning = True

    def stop(self):
        self.isrunning = False

    def main(self):
        while self.isrunning:
            try:
                # conn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                #                       "Server=GBPF0Y89C1\\SQLEXPRESS;"
                #                       "Database=Miradors;"
                #                       "Trusted_Connection=yes;")
                # conn = pyodbc.connect(r'DRIVER={ODBC Driver 13 for SQL Server};SERVER=GBPF0Y89C1\SQLEXPRESS;DATABASE=Miradors;Trusted_Connection=yes')
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


            except Exception as e:
                # open(r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\DU_Github\DXC_DU\WindowsService\logs\log.txt', 'x')
                # open(r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\DU_Github\DXC_DU\WindowsService\logs\log_exception_error.txt', 'w')
                f = open(r'C:\Users\sahmed243\Documents\WebDevelopment\Python\Scripts\DU_Github\DXC_DU\WindowsService\logs\log_exception_error.txt', 'a')
                f.write(str(e))
                f.close()
                time.sleep(15)
                stop(self)
                # continue


if __name__ == '__main__':
    PythonCornerExample.parse_command_line()
