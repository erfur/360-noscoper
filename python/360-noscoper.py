#!/usr/bin/python
#import daemon
import sys
from binascii import hexlify
import asyncio, evdev

def playFile():
    pass

def handleKey():
    pass

async def print_events(device):
    async for event in device.async_read_loop():
        evt = evdev.categorize(event)
        if isinstance(evt, evdev.events.KeyEvent):
            if evt.key_down:
                handleKey()

def main(args):
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()\
                if ('EV_KEY', 1) in evdev.InputDevice(path).capabilities(verbose=True)]

    for device in devices:
        asyncio.ensure_future(print_events(device))
    
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    # with daemon.DaemonContext():
    main(sys.argv[1:])