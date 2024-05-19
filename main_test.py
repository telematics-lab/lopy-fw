#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
# Copyright (C) 2024, Telematics Lab - Politecnico di Bari.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

import time
import pycom
import machine
from lib.pycoproc_2 import Pycoproc

from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

pycom.heartbeat(False)
pycom.rgbled(0x0A0A08) # white

py = Pycoproc()
while True:
    alt = MPL3115A2(py,mode=ALTITUDE) 
    print("Temperature: " + str(alt.temperature()))
    print("Altitude: " + str(alt.altitude()))
    pres = MPL3115A2(py,mode=PRESSURE) 
    print("Pressure: " + str(pres.pressure()))

    dht = SI7006A20(py)
    print("Temperature: " + str(dht.temperature())+ " deg C and Relative Humidity: " + str(dht.humidity()) + " %RH")

    li = LTR329ALS01(py)
    print("Light (channel Blue lux, channel Red lux): " + str(li.light()))

    acc = LIS2HH12(py)
    print("Acceleration: " + str(acc.acceleration()))
    print("Roll: " + str(acc.roll()))
    print("Pitch: " + str(acc.pitch()))

    print("Battery voltage: " + str(py.read_battery_voltage()))
    time.sleep(10)
