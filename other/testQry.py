

import pandas as pd
import openpyxl

qs = [
    {'id': 1, 'drivePath': 'C:\\temp', 'numOfFiles': 100, 'sizeOfFiles': 50},
    {'id': 2, 'drivePath': 'D:\\dir1', 'numOfFiles': 1000, 'sizeOfFiles': 1500},
    {'id': 3, 'drivePath': 'C:\\Users\\sahmed243\\Downloads\\CpMiradors\\heartbeatReportTesting', 'numOfFiles': 836, 'sizeOfFiles': 152},
    {'id': 4, 'drivePath': 'C:\\Temp\\MonitoringTables', 'numOfFiles': 3, 'sizeOfFiles': 0},
    {'id': 5, 'drivePath': 'C:\\Temp\\mydocs\\pdfs', 'numOfFiles': 9, 'sizeOfFiles': 0},
    {'id': 6, 'drivePath': 'C:\\Temp\\mydocs', 'numOfFiles': 18, 'sizeOfFiles': 0},
    {'id': 7, 'drivePath': 'C:\\Temp\\MonitoringTables', 'numOfFiles': 3, 'sizeOfFiles': 0},
    {'id': 8, 'drivePath': 'C:\\Temp\\mydocs\\pdfs', 'numOfFiles': 9, 'sizeOfFiles': 0},
    {'id': 9, 'drivePath': 'C:\\Temp\\mydocs', 'numOfFiles': 18, 'sizeOfFiles': 0},
    {'id': 10, 'drivePath': 'C:\\Temp\\MonitoringTables', 'numOfFiles': 3, 'sizeOfFiles': 0}
]

df = pd.DataFrame(qs)
# print(df)
del df['id']
writer = pd.ExcelWriter('C:\\temp\\Report.xlsx')
df.to_excel(writer, 'Sheet1', index=False)
writer.save()
