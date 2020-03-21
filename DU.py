import os

class Scan:
    def __init__(self, path, DU_FileCount, DU_FileSize, Scan_FileCount, Scan_FileSize):
        self.path = path
        self.DU_FileCount = DU_FileCount
        self.DU_FileSize = DU_FileSize
        self.Scan_FileCount = Scan_FileCount
        self.Scan_FileSize = Scan_FileSize

    def runDU(self):
        total_size = 0
        total_count = 0
        for dirpath, dirnames, filenames in os.walk(self.path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                # skip if it is symbolic link
                if not os.path.islink(fp):
                    self.DU_FileSize += os.path.getsize(fp)
                    self.DU_FileCount += 1

    def ReportDU(self):
        print('DU Report')
        print('Path: ' + str(self.path))
        print('Total File Count: ' + str(self.DU_FileCount))
        print('Total File Size: ' + str(round(self.DU_FileSize/1024/1024,2)) + 'MB')


dir1 = Scan(r'C:\Users\sahmed243\Downloads\bootstrap-4.3.1',0 ,0 ,0 ,0)
dir1.runDU()
dir1.ReportDU()
#print(dir1.DU_FileCount)
#print(dir1.DU_FileSize)
