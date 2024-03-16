#!/usr/bin/env python3

"""
Author:   Tyler Santos
Date:     3/14/2024
Version:  7.1
Repo:     https://github.com/santost12/uf-abe-scripts
About:    This script is for multiple computers to backup to a central NFS share.

Removed groupme. Print to console. Redirect output to log file.

Cron example:
0 23 * * 5 /usr/local/bin/NFS-backups-v7.py >> /nfs-backup.log 2>&1

"""

import os
import subprocess
import tarfile
from datetime import date
from datetime import timedelta

###
# Don't forget to include a slash at the end.
#
# Don't do:  /path/folder
# Do:        /path/folder/
###
backup_destination = '/nfs01/home/'

source_folders = [
    '/home/'
]


###
# Don't edit these variables unless you have a reason to.
###
hostname = subprocess.getoutput("hostname -s")
current_date = str(date.today())

this_week_backup = backup_destination + hostname + '-' + str(date.today()) + '.tar.gz'
last_week_backup = backup_destination + hostname + '-' + str(date.today() - timedelta(days=7)) + '.tar.gz'

output = backup_destination + hostname + '-' + current_date + '.tar.gz'


###
# Backup files
###
print("\n\nStarting log file on: " + current_date + " \n\n")
print("Beginning to create backup for: " + hostname + '-' + current_date + '.tar.gz')

try:
    tar_archive = tarfile.open(output, mode='w:gz')

    for index, folder in enumerate(source_folders):
        for root, dirs, files in os.walk(folder):
            for file in files:
                tar_archive.add(os.path.join(root, file))

    tar_archive.close()
    print("Successfully created backup:  " + hostname + '-' + current_date + '.tar.gz')

except Exception as e:
    print("An error occured when creating a backup for:  " + hostname + '-' + current_date + 'tar.gz')


###
# Delete old files
###
if tarfile.is_tarfile(this_week_backup) == True and tarfile.is_tarfile(last_week_backup) == True:
    os.remove(last_week_backup)
    message = "Deleted:  " + hostname + '-' + str(date.today() - timedelta(days=7)) + '.tar.gz'
    print(message)

else:
    print("[" + current_date + "] Error: Didn't delete anything because a previous or current backup failed.")
    exit
