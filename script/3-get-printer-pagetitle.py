#!/usr/bin/env python3
import asyncio
from pyppeteer import launch
from multiprocessing import Pool

from local_settings import THREADPOOL_PROCESSES_COUNT
from helper import is_host_port_open, get_printer_lists


async def get_screenshot(ip):
    print('process {}'.format(ip))
    pagetitle = None

    is_open = await is_host_port_open(ip, 80)
    if not is_open:
        return pagetitle

    try:
        browser = await launch()
        page = await browser.newPage()
        await page.setViewport(viewport={'width': 1280, 'height': 800})
        await page.goto('http://{}'.format(ip))  # , waitUntil='networkidle2')
        pagetitle = await page.title()
        print(pagetitle)
        await page.screenshot({'path': 'data/screenshot/{}.png'.format(ip)})
    except Exception as e:
        print(e)
        pass
    finally:
        # await browser.close()
        return pagetitle


async def get_screenshot_async(ip):
    try:
        return await asyncio.wait_for(get_screenshot(ip), timeout=(60 * 2))
    except asyncio.TimeoutError:
        print('{} timeout.'.format(ip))
        return None


def get_screenshot_poolfunc(ip):
    return (ip, asyncio.get_event_loop().run_until_complete(get_screenshot_async(ip)))


def main():
    printer_lists = get_printer_lists()

    with open('data/3-printer-pagetitle.txt', 'wt') as f:
        pass

    with Pool(THREADPOOL_PROCESSES_COUNT) as p:
        results = (p.map(get_screenshot_poolfunc, printer_lists))

    for r in results:
        if r[1]:
            with open('data/3-printer-pagetitle.txt', 'at') as f:
                f.write('{}\t{}'.format(r[0], r[1]))
                f.write('\n')


if __name__ == "__main__":
    main()
