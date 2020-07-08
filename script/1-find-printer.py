#!/usr/bin/env python3

import subprocess
import re
from multiprocessing import Pool
import sys

from local_settings import THREADPOOL_PROCESSES_COUNT

from helper import has_command


def getFirewallPortsByNmap(ips):
    # remove '-Pn'
    processResult = subprocess.run(['nmap', '--open', '-n', '-oG', '-', '-p515,631,9100', ips], stdout=subprocess.PIPE).stdout.decode('utf-8')

    result = []
    for line in processResult.split('\n'):
        m = re.match(r'Host: ([\d\.]+) \(\)	Ports: (.+)$', line)
        if m:
            portdescstr = m.group(2)
            portdescs = portdescstr.split()
            ports = []
            for p in portdescs:
                if '/open/' in p:
                    ports.append(p[0:p.find('/open/')])
            result.append({
                'ip': m.group(1),
                'ports': ','.join(ports)
            })

    return result


def MassGetFirewallPortsByNmap(work_ip_ranges):
    with Pool(THREADPOOL_PROCESSES_COUNT) as p:
        nmapresults = (p.map(getFirewallPortsByNmap, work_ip_ranges))

    result = []
    for item in nmapresults:
        if not item:
            continue

        for i in item:
            result.append(i)

    return result


def main():
    with open('data/0-CIDRs.txt', 'r') as f:
        lines = f.readlines()

    work_ip_ranges = []
    for line in lines:
        if not line:
            continue
        line = line.strip()
        work_ip_ranges.append(line)

    nmapresults = MassGetFirewallPortsByNmap(work_ip_ranges)

    with open('data/1-printer-list.txt', 'wt') as f:
        for item in nmapresults:
            f.write(item['ip'])
            f.write('\n')

    with open('data/1-printer-list-ports.txt', 'wt') as f:
        for item in nmapresults:
            f.write('{}\t{}'.format(item['ip'], item['ports']))
            f.write('\n')


if __name__ == "__main__":
    if not has_command('nmap'):
        sys.exit('Please install nmap first.')

    main()
