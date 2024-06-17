#!/usr/bin/env python3

"""
Author:   Tyler Santos
Date:     6/17/2024
Version:  9
Repo:     https://github.com/santost12/uf-abe-scripts
About:    This script is for multiple computers to backup to a central NFS share.

Cron example:
0 23 * * 5 /usr/local/bin/NFS-backups-v9.py

"""

import os, fnmatch
import subprocess
import tarfile
from datetime import date
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='/nfs-backup.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

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
# Don't edit or rename these variables unless you have a reason to.
###
hostname = subprocess.getoutput("hostname -s")
current_date = str(date.today())

current_backup = backup_destination + hostname + '-' + current_date + '.tar.gz'
current_backup_without_path = hostname + '-' + current_date + '.tar.gz'

output = backup_destination + hostname + '-' + current_date + '.tar.gz'


###
# Backup files
###
message = "Beginning to create backup for: " + hostname + '-' + current_date + '.tar.gz'
logger.info(message)

try:
    tar_archive = tarfile.open(output, mode='w:gz')

    for index, folder in enumerate(source_folders):
        for root, dirs, files in os.walk(folder):
            for file in files:
                tar_archive.add(os.path.join(root, file))

    tar_archive.close()
    message = "Successfully created backup:  " + hostname + '-' + current_date + '.tar.gz'
    logger.info(message)

except Exception as e:
    message = "An error occured when creating a backup for:  " + hostname + '-' + current_date + 'tar.gz'
    logger.info(message)


###
# Delete old files
###
try:
    if tarfile.is_tarfile(current_backup) == True:
        files = fnmatch.filter(os.listdir(backup_destination), hostname + "*")

        for file in files:
            if file == current_backup_without_path:
                pass
            else:
                os.remove(os.path.join(backup_destination, file))
                message = "Deleted " + file
                logger.info(message)


except Exception as e:
    message = "Didn't delete anything because an error occurred. Check the logged exception in the next line."
    logger.info(message)
    message = e
    logger.info(e)

