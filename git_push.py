# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import paramiko
import os
from time import gmtime, strftime

commit = input("Enter commit: ")
if commit == '':
    commit = strftime("%Y-%m-%d %H:%M:%S", gmtime())

print(os.system('git add .'))
print(os.system('git rm --cached git_push.py'))
print(os.system('git commit -m "'+ commit + '"'))
print(os.system('git push'))
