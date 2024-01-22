#!/usr/bin/env python3

"""
Author:   Tyler Santos
Date:     8/18/2023
Version:  5.0
Repo:     https://github.com/santost12/uf-abe-scripts
About:    This script is for multiple computers to backup to a central NFS share.

This version adds GroupMe notifications.
Refer to the GorupMe and groupy module documentation for more information.

"""

import os
import subprocess
import tarfile
from datetime import date
from datetime import timedelta

from groupy import Client

"""
Setup GroupMe so you can get notified when a backup is successful
or fails, install the groupy python module and put your API
key and bot id below. Do NOT leak the API key to github.

https://groupme.com/
https://dev.groupme.com/bots


"""

###
# Groupme bot config
###
client = Client.from_token("YOUR_API_KEY_HERE")
bot_gid = "YOUR_BOT_ID"


###
# Don't edit these variables unless you have a reason to.
###
hostname = subprocess.getoutput("hostname -s")
current_date = str(date.today())

this_week_backup = backup_destination + hostname + '-' + str(date.today()) + '.tar.gz'
last_week_backup = backup_destination + hostname + '-' + str(date.today() - timedelta(days=7)) + '.tar.gz'


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
    message = "Created backup for:  " + hostname + '-' + current_date + '.tar.gz'
    client.bots.post(bot_id=bot_gid, text=message)

except:
    message = "An unknown error occured when creating backup for:  " + hostname + '-' + current_date + 'tar.gz'
    client.bots.post(bot_id=bot_gid, text=message)



###
# Delete old files
###
if os.path.isfile(this_week_backup) == True and os.path.isfile(last_week_backup) == True:
    os.remove(last_week_backup)
    message = "Deleted:  " + hostname + '-' + str(date.today() - timedelta(days=7)) + '.tar.gz'
    client.bots.post(bot_id=bot_gid, text=message)

else:
    message = "Error: Didn't delete anything because a previous or current backup failed."
    client.bots.post(bot_id=bot_gid, text=message)
    exit

