#!/usr/bin/python3

"""

Author: Tyler Santos
Date: 8/2/2023

"""

import os
import subprocess
import tarfile
from datetime import date

current_date = str(date.today())
hostname = subprocess.getoutput("hostname -s")
backup_destination = '/home/tyler/backups/'


source_folders = [
    '/home/tyler/test1/',
    '/home/tyler/test2/'
]

output = backup_destination + hostname + '-' + current_date + '.tar.gz'

###
# Backup files
###
tar_archive = tarfile.open(output, mode='w:gz')

for index, folder in enumerate(source_folders):
    for root, dirs, files in os.walk(folder):
        for file in files:
            tar_archive.add(os.path.join(root, file))

tar_archive.close()


###
# Delete old files
###
os.chdir(backup_destination)
files = sorted(os.listdir(backup_destination), key=os.path.getctime)

counter = 0

if len(files) < 3:
    print("There are less than 3 files found in the backup folder. Not deleting anything.")
    exit

else:
    while counter < 3:
        #os.remove(files[counter])
        print("Deleted " + files[counter])
        counter = counter + 1

