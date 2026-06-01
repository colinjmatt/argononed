# Script for the Argon One Raspberry Pi 4 case adapted for ArchLinux ARM

## Description

The [Argon One](https://argon40.com/argon-one-raspberry-pi-4-case.html) is a case for the Raspberry Pi 4.

This script has been adapted from the [script](https://download.argon40.com/argon1.sh) for Raspberry Pi OS, to work with ArchLinux ARM.

There are mainly three changes compared to the original:
1. Using Python 3 instead of Python 2.
2. Reading the temperature cannot be done using vcgencmd, but we can use the sysfs
   instead.
3. The list of packages on which the script depends has been adapted to ArchLinux ARM.
4. One of the dependencies relies on the AUR

## Install 

```bash
cd /tmp
git clone -b pkg https://github.com/a-usov/argond.git
cd argond
makepkg -si
```

The [python-raspberry-gpio](https://aur.archlinux.org/packages/python-raspberry-gpio) dependancy has to be installed from the AUR. For example using your favourite AUR helper.

```bash
paru -S python-raspberry-gpio
```

## Usage

Systemd service argond has to be started after install.

 
```bash
systemctl enable argond --now
```

The fan configuration can be edited in the [python script](https://github.com/a-usov/argond/blob/master/argond.py#L45) in the format `["temperature=fanspeed", ...]`.
Afterwards, the service has to be reloaded.

## Contribution

Has been modified from [Argon-one-case-ubuntu-20.04](https://github.com/meuter/argon-one-case-ubuntu-20.04) by Cédric Meuter.

## Warning

This has been only tested on my Raspberry Pi 4. No issues so far, but big disclaimer nonetheless: use at your own risk. 

