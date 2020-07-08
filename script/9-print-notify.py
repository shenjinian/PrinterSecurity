#!/usr/bin/env python3
import subprocess
import time
import sys

from helper import get_printer_lists, has_command


def print_notify_to_ip(ip):
    print('process {}'.format(ip))

    printer_name = 'inc-temp-{}'.format(ip)
    _ = subprocess.run(['lpadmin', '-p', printer_name, '-v', 'socket://{}'.format(ip), '-o', "'Color=Mono'", '-o', "'Enhance Black Printing=ON'", '-o', "'Skip Blank Page=ON'", '-E'], stdout=subprocess.PIPE).stdout.decode('utf-8')

    _ = subprocess.run(['lpr', '-P', printer_name, 'inc-temp-notify-A4.pdf'], stdout=subprocess.PIPE).stdout.decode('utf-8')
    time.sleep(5)
    _ = subprocess.run(['lpadmin', '-x', printer_name], stdout=subprocess.PIPE).stdout.decode('utf-8')


def main():
    printer_lists = get_printer_lists()

    for printer in printer_lists:
        print_notify_to_ip(printer)


if __name__ == "__main__":
    if not has_command('lpadmin'):
        sys.exit('Please install lpadmin first.')

    if not has_command('lpr'):
        sys.exit('Please install lpr first.')

    main()
