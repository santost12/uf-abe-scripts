#!/usr/bin/env python3

"""
Author:   Tyler Santos
Date:     3/17/2024
Version:  8
Repo:     https://github.com/santost12/uf-abe-scripts
About:    This script is for multiple computers to backup to a central NFS share.

Use built-in logging Python library. 

Cron example:
0 23 * * 5 /usr/local/bin/NFS-backups-v7.py

"""

import os
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
    if tarfile.is_tarfile(this_week_backup) == True and tarfile.is_tarfile(last_week_backup) == True:
        os.remove(last_week_backup)
        message = "Deleted:  " + hostname + '-' + str(date.today() - timedelta(days=7)) + '.tar.gz'
        logger.info(message)

except Exception as e:
    message = "Didn't delete anything because a previous or current backup failed."
    logger.info(message)
    message = e
    logger.info(e)

