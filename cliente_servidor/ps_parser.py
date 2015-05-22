#!/usr/bin/env python

from subprocess import Popen, PIPE
from re import split
from sys import stdout
from modelo import Proc


def get_proc_list():
    ''' Retrieves a list [] of Proc objects representing the active
    process list list '''
    proc_list = []
    sub_proc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
    # Discard the first line (ps aux header)
    sub_proc.stdout.readline()
    for line in sub_proc.stdout:
        # The separator for splitting is 'variable number of spaces'
        proc_info = split(" *", line.strip())
        proc_list.append(Proc(proc_info))
    return proc_list


if __name__ == "__main__":
    _proc_list = get_proc_list()
    # Show the minimal proc list (user, pid, cmd)
    stdout.write('Process list:n')
    for proc in _proc_list:
        stdout.write('t' + proc.to_str() + 'n')
    # (proc.user == 'root')
    root_proc_list = [x for x in _proc_list if x.user == 'root']
    stdout.write('Owned by root:n')
    for proc in root_proc_list:
        stdout.write('t' + proc.to_str() + 'n')
