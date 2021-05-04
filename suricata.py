#!/usr/bin/python

# modified script by E. J. Fernandez Rodriguez
# original script by Christophe Vandeplas: https://github.com/cvandeplas/suricata_stats/blob/master/suricata_stats.py

import argparse
import os
import platform
import psutil
import time

# global vars
zabbixip = '1.2.3.4'                                            # zabbix server IP address
logfile = '/absolute/path/to/your/suricata/stats.log/file'      # path to the stats log file
prefix = 'script.suricata.for.example.'                         # data key prefix

# parse the arguments
parser = argparse.ArgumentParser(
    description='Consolidate the suricata stats file.')
parser.add_argument('-z', '--zabbix', action='store_true',
                    help='Send output to zabbix')
parser.add_argument('-q', '--quiet', action='store_true',
                    help='Be quiet (do not print to stdout)')
args = parser.parse_args()

# tail the stats file 'f' for 'n' lines


def tail(f, n):
    stdin, stdout = os.popen2("tail -n {0} '{1}'".format(n, f))
    stdin.close()
    lines = stdout.readlines()
    stdout.close()
    return lines

# boolean check for suricata's process


def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return 0

# return the index of the first item in the list containing the string


def substringIndexSearch(list, string):
    for i, s in enumerate(list):
        if string in s:
            return i
    return -1

# return 'now' in Unix epoch time


def now():
    return int(time.time())


# get the stats and trim the unnecesary output
f_content = tail(logfile, 100)
f_content.reverse()
separator_index = substringIndexSearch(f_content, '----------')
f_trimmed = f_content[:separator_index]

# build data object
data = {}
for line in f_trimmed:
    var, section, value = line.split('|')
    var = var.strip()
    section = section.strip()
    value = value.strip()
    try:
        data[var] = data[var] + int(value)
    except KeyError:
        data[var] = int(value)

# build the script's output
stats = []
stats.append("- {0}suricata.proc {1} {2}".format(prefix,
             now(), checkIfProcessRunning('suricata')))
for key, value in data.items():
    stats.append("- {0}{1} {2} {3}".format(prefix, key, now(), value))

# if 'zabbix' arg passed, send output directly to zabbix server
if args.zabbix:
    hostname = platform.node()
    stdin, stdout = os.popen2(
        "zabbix_sender -s {0} -z {1} -T -i -".format(hostname, zabbixip))
    stat_dump = '\n'.join(stats)
    stdin.write(stat_dump)
    stdin.close()
    # if 'quiet' arg passed too, do not output anything to console
    if not args.quiet:
        output = stdout.readlines()
        r = ''.join(output).replace('\n', ', ')
        line = r[:len(r) - 2]
        i = len(line)
        separator = ''
        while i > 0:
            separator += '-'
            i -= 1
        separator.join('\n')
        print separator
        print line
        print separator
        print stat_dump
    stdout.close()
