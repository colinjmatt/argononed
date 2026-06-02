#!/usr/bin/env python3

import os

# Trick gpiozero into thinking it sees a Raspberry Pi 4 Model B
# bypassing the mainline kernel's missing cpuinfo data.
os.environ['PI_REVISION'] = 'c03111'

import smbus
from gpiozero import Button
import time
from threading import Thread

# Set up the I2C bus. RPi 4 uses bus 1.
try:
    bus = smbus.SMBus(1)
except Exception as e:
    print(f"Error initializing SMBus: {e}")
    bus = None

# Argon One MCU power button signal is connected to GPIO 4.
# We set pull_up=False because the Argon MCU drives this pin directly.
shutdown_pin = Button(4, pull_up=False)

def shutdown_check():
    """
    The Argon One MCU sends tiny high pulses to GPIO 4 to signal button presses.
    A ~10-20ms pulse means double-tap (reboot).
    A ~30-50ms pulse means long-press (shutdown).
    """
    while True:
        shutdown_pin.wait_for_active()
        start_time = time.time()
        shutdown_pin.wait_for_inactive()
        pulse_duration = time.time() - start_time
        
        if 0.01 <= pulse_duration <= 0.03:
            os.system("reboot")
        elif 0.03 < pulse_duration <= 0.06:
            os.system("shutdown now -h")

def get_fanspeed(tempval, configlist):
    for curconfig in configlist:
        curpair = curconfig.split("=")
        tempcfg = float(curpair[0])
        fancfg = int(float(curpair[1]))
        if tempval >= tempcfg:
            return fancfg
    return 0

def load_config(fname):
    newconfig = []
    try:
        with open(fname, "r") as fp:
            for curline in fp:
                if not curline or curline.strip() == "" or curline.strip().startswith("#"):
                    continue
                tmppair = curline.strip().split("=")
                if len(tmppair) != 2:
                    continue
                try:
                    tempval = float(tmppair[0])
                    fanval = int(float(tmppair[1]))
                    if 0 <= tempval <= 100 and 0 <= fanval <= 100:
                        newconfig.append("{:5.1f}={}".format(tempval, fanval))
                except ValueError:
                    continue
        if len(newconfig) > 0:
            newconfig.sort(reverse=True)
    except Exception:
        return []
    return newconfig

def get_temp():
    """
    Reads the CPU temperature directly from the kernel's thermal zone
    instead of relying on vcgencmd, making it compatible with pure Arch Linux.
    """
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return float(f.read().strip()) / 1000.0
    except Exception:
        return 0.0

def temp_check():
    fanconfig = ["65=100", "60=55", "55=10"]
    tmpconfig = load_config("/opt/argonone/argononed.conf")
    if len(tmpconfig) > 0:
        fanconfig = tmpconfig
        
    address = 0x1a
    prevblock = -1
    
    while True:
        val = get_temp()
        block = get_fanspeed(val, fanconfig)
        
        # Hysteresis: wait before dropping fan speed to prevent revving up and down quickly
        if block < prevblock:
            time.sleep(30) 
            
        prevblock = block
        
        if bus is not None:
            try:
                bus.write_byte_data(address, 0, block)
            except IOError:
                pass
                
        time.sleep(30)

if __name__ == "__main__":
    try:
        # Run the checks as background daemon threads
        t1 = Thread(target=shutdown_check, daemon=True)
        t2 = Thread(target=temp_check, daemon=True)
        t1.start()
        t2.start()
        
        # Keep the main thread alive. If this exits, the daemon threads close automatically.
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        # gpiozero handles GPIO cleanup automatically on exit
        pass
