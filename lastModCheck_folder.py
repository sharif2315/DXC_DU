import os
import time
import datetime


def runDU(start_path = r'C:\Users\sahmed243\Downloads\bootstrap-4.3.1'):
    total_size = 0
    total_count = 0

    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
                total_count += 1

    #return total_size
    print('total size: ' + str(total_size))
    print('total count: ' + str(total_count))

#print(get_size(), 'bytes')
#runDU()

#file = r'C:\Users\sahmed243\Downloads\bootstrap-4.3.1\README.md'
#print("last modified: %s" % time.ctime(os.path.getmtime(myfile)))

def getLastModDateSingle(file):
    # t = os.path.getmtime(myfile)
    # return datetime.datetime.fromtimestamp(t)
    lastMod_myfile = datetime.datetime.fromtimestamp(os.path.getmtime(file))
    rightNow = datetime.datetime.now()
    timeDiff = rightNow - lastMod_myfile
    if timeDiff.days > 30:
        print(file)
        print('This file is an Annex Candidate')
    else:
        print(file)
        print('This file is NOT an Annex Candidate')

# getLastModDateSingle(r'C:\Users\sahmed243\Documents\other\\myfolder\.babelrc.js')
# getLastModDateSingle(r'C:\Users\sahmed243\Documents\other\\myfolder\.browserslistrc')

def getListOfPaths(myDir):
    numFiles = 0
    numDirs = 0
    pathList = []
    for path, dirpath, filenames in os.walk(myDir):
        for filename in filenames:
            numFiles += 1
            #print( str(path) + '\\' + str(filename))
            path = str(path) + '\\' + str(filename)
            pathList.append(path)
    n = 0
    for path in pathList:
        n += 1
        print( str(n) + ': ' + path)


#getListOfPaths(myDir = r'C:\Users\sahmed243\Downloads\bootstrap-4.3.1')

def getListOfLastMod(mydir):
    numFiles = 0
    numDirs = 0
    pathList = []
    annexCandCount = 0
    annexList = []

    #print(os.listdir(r'C:\Users\sahmed243\Downloads\bootstrap-4.3.1'))
    files_path = [os.path.abspath(x) for x in os.listdir(mydir)]
    for i in files_path:
        print(i)
    # for path, dirpath, filenames in os.walk(mydir):
    #     for i in dirpath:
    #         print(i)
        # for filename in filenames:
        #     numFiles += 1
        #     #print( str(path) + '\\' + str(filename))
        #     path = str(path) + '\\' + str(filename)
        #
        #     pathList.append(path)

    # for i in pathList:
    #     print(i)
        #lastmod = os.stat(str(i)).st_mtime
        #print(type(lastmod))
        #lastMod_myfile = datetime.datetime.fromtimestamp(os.path.getmtime(i))

        # rightNow = datetime.datetime.now()
        # timeDiff = rightNow - lastMod_myfile
        # if timeDiff.days > 30:
        #     annexCandCount += 1
        #     annexList.append(i)
    #
    # print('List of Annex Candidates: ' + str(annexCandCount))

            #print('This file is an Annex Candidate')
        # else:
        #     continue
            #print('This file is NOT an Annex Candidate')
getListOfLastMod(r'C:\Users\sahmed243\Downloads\bootstrap-4.3.1')
