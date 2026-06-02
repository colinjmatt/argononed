#!/usr/bin/env python3

import smbus
import lgpio
import os
import time
from threading import Thread

# Set up the I2C bus. RPi 4 uses bus 1.
try:
    bus = smbus.SMBus(1)
except Exception as e:
    print(f"Error initializing SMBus: {e}")
    bus = None

def shutdown_check():
    """
    Directly polls GPIO 4 using the lgpio C-library, bypassing all 
    board-detection wrappers.
    """
    try:
        # Open the primary GPIO chip and claim pin 4 as an input
        handle = lgpio.gpiochip_open(0)
        lgpio.gpio_claim_input(handle, 4)
    except Exception as e:
        print(f"Error claiming GPIO 4 via lgpio: {e}")
        return

    while True:
        # The Argon MCU sends a high pulse when the button is pressed
        if lgpio.gpio_read(handle, 4) == 1:
            start_time = time.time()
            
            # Wait for the pulse to finish (pin goes back to 0)
            while lgpio.gpio_read(handle, 4) == 1:
                time.sleep(0.01)
                
            pulse_duration = time.time() - start_time
            
            # Double-tap = Reboot (~10-30ms pulse)
            if 0.01 <= pulse_duration <= 0.03:
                os.system("reboot")
            # Long-press = Shutdown (~30-60ms pulse)
            elif 0.03 < pulse_duration <= 0.06:
                os.system("shutdown now -h")
                
        time.sleep(0.01)

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
        
        # Hysteresis: wait before dropping fan speed
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
        t1 = Thread(target=shutdown_check, daemon=True)
        t2 = Thread(target=temp_check, daemon=True)
        t1.start()
        t2.start()
        
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        pass