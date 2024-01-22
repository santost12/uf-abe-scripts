#!/usr/bin/env python3

"""
Author:   Tyler Santos
Date:     8/17/2023
Version:  3.0
Repo:     https://github.com/santost12/uf-abe-scripts
About:    This script is for multiple computers to backup to a central NFS share.

"""

import os
import subprocess
import tarfile
from datetime import date
from datetime import timedelta


###
# Don't edit these variables unless you have a reason to.
###
hostname = subprocess.getoutput("hostname -s")
current_date = str(date.today())
lastweek_date = str(date.today() - timedelta(days=7))


###
# Don't forget to include a slash at the end.
#
# Don't do:  /path/folder
# Do:        /path/folder/
###
backup_destination = '/nfs01/home/'

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
old_backup_archive = backup_destination + hostname + '-' + lastweek_date + '.tar.gz'

os.chdir(backup_destination)
files = sorted(os.listdir(backup_destination), key=os.path.getctime)


"""
IMPORTANT

1) The two lines above find out how many files are in the backup destination folder.

2) If there are less than X number of files in the backup location,
this script won't delete anything. X can be adjusted below. Remove the
if-else below if you do not want this behavior.

3) This version of the script also won't delete anything that
is not from EXACTLY 7 days ago. Therefore, it is important that
you run it on a regular schedule. If you want to change this behavior,
rename and edit the lastweek_date variable.

"""

if len(files) < 3:
    exit
else:
    try:
        os.remove(old_backup_archive)
        print("Deleted " + old_backup_archive)
    except:
        print("Error: Unable to delete " + old_backup_archive)

