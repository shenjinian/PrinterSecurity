import socket
from local_settings import DEBUG_PRINTERS
from shutil import which


async def is_host_port_open(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(5)
    try:
        result = 0 == sock.connect_ex((host, port))
        sock.shutdown(socket.SHUT_RDWR)
        return result
    except Exception:
        return False
    finally:
        sock.close()


def get_printer_lists():
    with open('data/1-printer-list.txt', 'r') as f:
        lines = f.readlines()

    if DEBUG_PRINTERS:
        lines = DEBUG_PRINTERS

    printer_lists = []
    for line in lines:
        if not line:
            continue
        line = line.strip()
        printer_lists.append(line)

    return printer_lists


def has_command(name):
    return which(name) is not None
