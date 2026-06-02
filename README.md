# Argon One Daemon (`argononed`) for Mainline Arch Linux ARM

## Description

The [Argon One](https://argon40.com/argon-one-raspberry-pi-4-case.html) is a case for the Raspberry Pi 4 featuring software-controlled active cooling and power management.

This project is a heavily modified fork designed specifically to work on **64-bit mainline Arch Linux ARM** (Linux 6.x+ kernels).

### Key Changes from Upstream
The transition to the mainline 6.x kernel breaks legacy GPIO memory mapping (`RPi.GPIO`) and board-detection wrappers (`gpiozero` looking for Pi-specific `/proc/cpuinfo` strings). To resolve this, this version:
1. **Bypasses Wrappers:** Uses the `lgpio` C-library directly to poll the hardware `gpiochip`, making it immune to board-detection failures on pure, mainline Arch Linux.
2. **Sysfs Temperatures:** Reads the CPU temperature directly from the kernel (`/sys/class/thermal/thermal_zone0/temp`) instead of relying on the proprietary `vcgencmd`.
3. **I2C Power Cut:** Uses a systemd shutdown hook (`argononed-poweroff.py`) to send the `0xFF` signal via I2C to the Argon MCU, physically cutting power after a graceful OS halt.
4. **CLI Configuration:** Includes a fully functional `argonone-config` terminal tool for generating fan curves.

---

## Prerequisites & Dependencies

Because Arch Linux ARM is bleeding-edge, the required `lgpio` C-library must be compiled from source before the Python wrapper can be installed.

**1. Install build tools and base dependencies:**
```bash
sudo pacman -Syu i2c-tools python python-pip swig base-devel
```

**2. Enable the I2C Bus:**
Ensure the I2C hardware bus is enabled in your bootloader. Open `/boot/config.txt` and add:
```text
dtparam=i2c_arm=on
```
Then ensure the software driver loads on boot:
```bash
echo "i2c-dev" | sudo tee /etc/modules-load.d/i2c-dev.conf
sudo reboot
```

**3. Compile and install `lgpio` from source:**
```bash
curl -LO [https://github.com/joan2937/lg/archive/refs/heads/master.tar.gz](https://github.com/joan2937/lg/archive/refs/heads/master.tar.gz)
tar -xzf master.tar.gz
cd lg-master
make
sudo make install
sudo cp liblgpio.so* /usr/lib/
sudo cp lgpio.h /usr/include/
sudo ldconfig
```

**4. Install the Python wrapper:**
```bash
sudo pip install rpi-lgpio --break-system-packages
```

---

## Installation

Once the backend hardware drivers are fully in place, you can build and install the daemon using `makepkg`.

```bash
cd /tmp
git clone [https://github.com/colinjmatt/argononed.git](https://github.com/colinjmatt/argononed.git)
cd argononed
makepkg -si
```

---

## Usage

Enable and start the background service so it runs automatically on boot:
 
```bash
sudo systemctl enable --now argond.service
```

### Fan Configuration
You do not need to manually edit Python scripts to change fan behavior. Simply run the included configuration tool from anywhere in your terminal:

```bash
sudo argonone-config
```
This tool allows you to set the fan to "Always On", use default temperature thresholds (55C, 60C, 65C), or define your own custom temperature/speed pairs. The script will automatically save your changes to `/opt/argonone/argononed.conf` and restart the daemon to apply them immediately.

---

## Contribution & Licensing

This project is distributed under the MIT License (Dual Copyright).

* Modified for mainline Arch Linux ARM by Colin Matt (2026).
* Originally forked from [a-usov/argond](https://github.com/a-usov/argond) by Artem Usov.
* Which in turn was modified from [Argon-one-case-ubuntu-20.04](https://github.com/meuter/argon-one-case-ubuntu-20.04) by Cédric Meuter.

## Warning

This has been tested exclusively on a Raspberry Pi 4 running 64-bit Arch Linux ARM on the mainline kernel. No issues so far, but big disclaimer nonetheless: **use at your own risk.**