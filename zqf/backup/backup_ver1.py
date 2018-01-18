#-*- coding:utf-8 -*-
import os
import time

source = [r'"c:\Users\zhongqif\zqf\note"']
target_dir = r'C:\Users\zhongqif\zqf\test'

target = target_dir + os.sep + \
         time.strftime('%Y%m%d%H%M%S') + '.ZIP'

if not os.path.exists(target_dir):
    os.mkdir(target_dir)

zip_command = 'zip -r {0} {1}'.format(target, ''.join(source))

print('zip command is:')
print(zip_command)
print('running:')

if os.system(zip_command) == 0:
    print('successful backup to', target)
else:
    print('backup failed')