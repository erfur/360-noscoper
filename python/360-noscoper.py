#!/usr/bin/python
#import daemon
import sys
from binascii import hexlify
import asyncio, evdev
import configparser

def playFile(fileName):
    print("playing {}".format(fileName))

def handleKey(keycode):
    if isinstance(keycode, list) and keycode[0] in bindings.keys():
        playFile(bindings[keycode[0]])
    elif keycode in bindings.keys():
        playFile(bindings[keycode])
    else:
        playFile(bindings['default'])

async def filterKeyEvents(device):
    async for event in device.async_read_loop():
        evt = evdev.categorize(event)
        if isinstance(evt, evdev.events.KeyEvent):
            if evt.key_down:
                handleKey(evdev.categorize(event).keycode)

def devicesWithButtons():
    return [evdev.InputDevice(path) for path in evdev.list_devices()\
                if ('EV_KEY', 1) in evdev.InputDevice(path).capabilities(verbose=True)]

def getConfig(file='config.ini'):
    global bindings
    config = configparser.ConfigParser()
    config.read(file)
    bindings = config['bindings']

def main(args):
    for device in devicesWithButtons():
        asyncio.ensure_future(filterKeyEvents(device))
    
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    getConfig()
    # with daemon.DaemonContext():
    main(sys.argv[1:])