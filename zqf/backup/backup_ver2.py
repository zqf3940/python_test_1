import os
import time

source = [r'"c:\Users\zhongqif\zqf\note"']

target_dir = r'C:\Users\zhongqif\zqf\test'

if not os.path.exists(target_dir):
    os.mkdir(target_dir)

today = target_dir + os.sep + time.strftime('%Y%m%d')
now = time.strftime('%H%M%S')
target = today + os.sep + now + '.zip'

if not os.path.exists(today):
    os.mkdir(today)
    print('successfully created directory', today)

zip_command = 'zip -r {0} {1}'.format(target, ' '.join(source))

print('zip command is:')
print(zip_command)
print('running:')

if os.system(zip_command) == 0:
    print('successful baackup to', target)
else:
    print('backup faailed')

