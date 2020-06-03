import os

mypath = r'C:\Temp'

def listDir(dir):
    fileNames = os.listdir(dir)
    totalFileCount = 0
    totalFileSize = 0

    for filename in fileNames:
        #print('File Name: ' + filename)
        #print('Folder Path ' + os.path.abspath(os.path.join(dir, filename)), sep='\n')
        totalFileCount += 1

    print('Total File Count = ' + str(totalFileCount))

    for file in fileNames:
        totalFileSize += os.stat(file).st_size

    print('Total File Size = ' + str(totalFileSize))

if __name__ == '__main__':
    listDir(mypath)

#listDir(mypath)
