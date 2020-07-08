#!/usr/bin/env python3
import asyncio
from multiprocessing import Pool
import subprocess
import re
import sys

from local_settings import THREADPOOL_PROCESSES_COUNT
from helper import is_host_port_open, get_printer_lists, has_command


async def get_attributes(ip):
    print('process {}'.format(ip))
    pagetitle = None

    is_open = await is_host_port_open(ip, 631)
    if not is_open:
        return pagetitle

    processResult = subprocess.run(['ipptool', '-T', '10', '-4', '-V', '1.0', '-t', '-v', '-d', 'REQ_USER=', 'http://{}:631/ipp/print'.format(ip), 'ipp_printer_attributes.test'], stdout=subprocess.PIPE).stdout.decode('utf-8')

    for line in processResult.split('\n'):
        m = re.match(r'\s*printer-make-and-model [^=]+=\s*(.*)', line)
        if m:
            return m.group(1)
        # m = re.match(r'\s*printer-name [^=]+=\s*(.*)', line)
        # if m:
        #     print(m.group(1))
        # m = re.match(r'\s*printer-dns-sd-name [^=]+=\s*(.*)', line)
        # if m:
        #     print(m.group(1))
    return pagetitle


async def get_attributes_async(ip):
    try:
        return await asyncio.wait_for(get_attributes(ip), timeout=(10))
    except asyncio.TimeoutError:
        print('{} timeout.'.format(ip))
        return None


def get_attributes_poolfunc(ip):
    result = asyncio.get_event_loop().run_until_complete(get_attributes_async(ip))
    if result:
        with open('data/3-printer-attributes.txt', 'at') as f:
            f.write('{}\t{}'.format(ip, result))
            f.write('\n')


def main():
    printer_lists = get_printer_lists()

    with open('data/3-printer-attributes.txt', 'wt'):
        pass

    with Pool(THREADPOOL_PROCESSES_COUNT) as p:
        p.map(get_attributes_poolfunc, printer_lists)


if __name__ == "__main__":
    if not has_command('ipptool'):
        sys.exit('Please install ipptool first.')

    main()
