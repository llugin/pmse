#!/usr/bin/env python3

from os import listdir
from os.path import isfile, join
from subprocess import run

test_dir = 'jstests/core'

dev_dir = '/dev/shm'

tests = [test for test in listdir(test_dir) if isfile(join(test_dir, test)) and test.endswith('js')]

binary = ['buildscripts/resmoke.py']
args = ['--continueOnFailure', '--storageEngine=pmse', '--dbpath=/dev/shm']


failed = []
passed = []
for test in sorted(tests):
    cmd = binary + args
    cmd.append(join(test_dir, test))

    completed_process = run(cmd)
    if completed_process.returncode == 0:
        passed.append(test)
    else:
        failed.append(test)
    run('rm -rf {}/job0'.format(dev_dir), shell=True)


print('Failed tests:')
for test in failed:
    print(test)

print('Passed tests:')
for test in passed:
    print(test)
