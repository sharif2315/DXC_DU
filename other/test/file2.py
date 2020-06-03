import os

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
runDU()
