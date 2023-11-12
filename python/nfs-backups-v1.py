#!/usr/bin/python3

"""

Author: Tyler Santos
Date: 8/1/2023

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

output = [
    backup_destination + 'test1' + '-' + hostname + current_date + '.tar.gz',
    backup_destination + 'test2' + '-' + hostname + current_date + '.tar.gz'
]

###
# Backup files
###
for index, folder in enumerate(source_folders):
    tar_archive = tarfile.open(output[index], mode='w:gz')

    for root, dirs, files in os.walk(folder):
        for file in files:
            tar_archive.add(os.path.join(root, file))

    tar_archive.close()


###
# Delete the 2 oldest files
###
os.chdir(backup_destination)
files = sorted(os.listdir(backup_destination), key=os.path.getctime)

os.remove(files[0])
os.remove(files[1])

print("Deleted " + files[0] + " and " + files[1])
