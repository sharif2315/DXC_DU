import os

def getFolderSize(folder):
    total_count = 0
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
            total_count =+ 1
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    print('size in bytes: 'total_size)
    print(total_size)
    print(total_size)

print(getFolderSize(r'C:\Users\sahmed243\Downloads\bootstrap-4.3.1'))
