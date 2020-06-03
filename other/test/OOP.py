import os

class Scan:
    def __init__(self, path, DU_FileCount, DU_FileSize, Scan_FileCount, Scan_FileSize):
        self.path = path
        self.DU_FileCount = DU_FileCount
        self.DU_FileSize = DU_FileSize
        self.Scan_FileCount = Scan_FileCount
        self.Scan_FileSize = Scan_FileSize

    def runDU(self):
        fileNames = os.listdir(self.path)
        totalFileCount = 0
        for filename in fileNames:
            #print('File Name: ' + filename)
            totalFileCount += 1
        #print('Total File Count = ' + str(totalFileCount))
        self.DU_FileCount = totalFileCount
        #return self.DU_FileCount


dir1 = Scan(r'C:\Temp',0 ,0 ,0 ,0)

#print(dir1.runDU())

dir1.runDU()

print(dir1.DU_FileCount)
