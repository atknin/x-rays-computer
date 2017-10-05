# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import paramiko
import os
from time import gmtime, strftime

commit = input("Enter pass: ")
if commit == '123':
    print(os.system('sudo git fetch --all'))
    print(os.system('sudo git reset --hard origin/master'))
else:
    print('Пароль не верен')
    #sdasd
