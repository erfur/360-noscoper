#!/usr/bin/python
import daemon
import sys, os
from binascii import hexlify
import asyncio, evdev
import configparser
import simpleaudio as sa
import concurrent.futures

def playFile(file):
    open('/tmp/noscoper.log', 'a').write("playing {}\n".format(file))
    wav = sa.WaveObject.from_wave_file(file)
    play = wav.play()
    play.wait_done()

def handleKey(keycode):
    print(keycode)
    if isinstance(keycode, list) and keycode[0] in bindings.keys():
        playFile(os.path.join(cwd, "sounds", bindings[keycode[0]]))
    elif keycode in bindings.keys():
        playFile(os.path.join(cwd, "sounds", bindings[keycode]))
    else:
        playFile(os.path.join(cwd, "sounds", bindings['default']))

async def filterKeyEvents(device):
    async for event in device.async_read_loop():
        evt = evdev.categorize(event)
        if isinstance(evt, evdev.events.KeyEvent):
            # print(evt.keystate)
            if evt.keystate == 1:
                executor.submit(handleKey, evdev.categorize(event).keycode)

def devicesWithButtons():
    return [evdev.InputDevice(path) for path in evdev.list_devices()\
                if ('EV_KEY', 1) in evdev.InputDevice(path).capabilities(verbose=True)]

def getConfig(file='config.ini'):
    global bindings
    config = configparser.ConfigParser()
    config.read(file)
    bindings = config['bindings']

def setWorkers():
    global executor
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)

def setCWD():
    global cwd
    cwd = os.getcwd()

def main(args):
    for device in devicesWithButtons():
        asyncio.ensure_future(filterKeyEvents(device))
    
    loop = asyncio.get_event_loop()
    loop.run_forever()

if __name__ == "__main__":
    getConfig()
    setWorkers()
    setCWD()
    with daemon.DaemonContext():
        main(sys.argv[1:])