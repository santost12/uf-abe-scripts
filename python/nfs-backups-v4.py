#!/usr/bin/env python3

"""
Author:   Tyler Santos
Date:     8/18/2023
Version:  4.0
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


###
# Don't forget to include a slash at the end.
#
# Don't do:  /path/folder
# Do:        /path/folder/
###
backup_destination = '/nfs01/home/'

source_folders = [
    '/home/tyler/test1/'
]

output = backup_destination + hostname + '-' + current_date + '.tar.gz'


###
# Backup files
###
try:
    tar_archive = tarfile.open(output, mode='w:gz')

    for index, folder in enumerate(source_folders):
        for root, dirs, files in os.walk(folder):
            for file in files:
                tar_archive.add(os.path.join(root, file))

    tar_archive.close()
    print("Successfully created backup: " + output)
except:
    print("Something went wrong. An error occured when creating a backup for: " + output)



###
# Delete old files
###
this_week_backup = backup_destination + hostname + '-' + str(date.today()) + '.tar.gz'
last_week_backup = backup_destination + hostname + '-' + str(date.today() - timedelta(days=7)) + '.tar.gz'


if os.path.isfile(this_week_backup) == True and os.path.isfile(last_week_backup) == True:
    #os.remove(last_week_backup)
    print("Deleted: " + last_week_backup)

else:  	
    print("Didn't delete: " + last_week_backup)
    exit

