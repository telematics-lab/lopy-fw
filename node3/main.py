#!/usr/bin/env python
#
# Copyright (c) 2020, Pycom Limited.
# Copyright (C) 2024, Telematics Lab - Politecnico di Bari.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

import machine
import math
import network
from network import LoRa
import os
import time
import utime
import gc
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from pycoproc_1 import Pycoproc
import socket
import binascii
import struct
import config
import pycom

time.sleep(10)
gc.enable()

# initialize LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# create an OTA authentication params
dev_eui = binascii.unhexlify('xxxx')
app_eui = binascii.unhexlify('0000000000000000')
app_key = binascii.unhexlify('xxxx')

if config.SINGLE_CHANNEL:
    # set the 3 default channels to the same frequency (must be before sending the OTAA join request)
    lora.add_channel(0, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
    lora.add_channel(1, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)
    lora.add_channel(2, frequency=config.LORA_FREQUENCY, dr_min=0, dr_max=5)

# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=config.LORA_NODE_DR)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

if config.SINGLE_CHANNEL:
    # remove all the non-default channels
    for i in range(3, 16):
        lora.remove_channel(i)
else:
    # remove all the non-default channels
    for i in range(8, 16):
        lora.remove_channel(i)
        
# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket non-blocking
s.setblocking(False)

time.sleep(5.0)




# setup rtc
rtc = machine.RTC()
rtc.ntp_sync("pool.ntp.org")
utime.sleep_ms(750)
print('\nRTC Set from NTP to UTC:', rtc.now())
utime.timezone(7200)
print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')

py = Pycoproc(Pycoproc.PYTRACK)
l76 = L76GNSS(py, timeout=30)

while (True):
    coord = l76.coordinates()

    if coord[0] is not None:
        print("GPS informations: {} - {} - {}\n".format(coord, rtc.now(), gc.mem_free()))
        dataLa = bytearray(struct.pack("i", int(coord[0]*100000)))
        dataLo = bytearray(struct.pack("i", int(coord[1]*100000)))
        data = dataLa+dataLo
        s.send(data)
        print("GPS informations: {} - {} - {}\n".format(coord, rtc.now(), gc.mem_free()))
    else:
        print("Waiting GPS to lock...\n")

    time.sleep(5)