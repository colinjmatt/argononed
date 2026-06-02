#!/usr/bin/env python3

import sys
import smbus

# The Raspberry Pi 4 uses I2C bus 1
try:
    bus = smbus.SMBus(1)
except Exception as e:
    print(f"Error initializing SMBus 1: {e}")
    try:
        bus = smbus.SMBus(0)
    except:
        bus = None

if bus is not None and len(sys.argv) > 1:
    # First, tell the Argon MCU to stop the fan (send 0 to address 0x1a)
    try:
        bus.write_byte_data(0x1a, 0, 0)
    except IOError:
        pass
        
    # If systemd is halting or powering off the OS, tell the MCU to physically cut power
    if sys.argv[1] in ["poweroff", "halt"]:
        try:
            # 0xFF signals the Argon MCU to sever the power connection
            bus.write_byte_data(0x1a, 0, 0xFF)
        except IOError:
            pass