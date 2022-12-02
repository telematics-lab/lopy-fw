#!/usr/bin/env python
#
# Copyright (c) 2019, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

""" OTAA Node example compatible with the LoPy Nano Gateway """


from network import LoRa
import socket
import binascii
import struct
import time
import config
import pycom
from pycoproc_2 import Pycoproc
import machine


from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

pycom.heartbeat(False)

py = Pycoproc()
if py.read_product_id() != Pycoproc.USB_PID_PYSENSE:
    raise Exception('Not a Pysense')

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

# remove all the non-default channels
for i in range(3, 16):
    lora.remove_channel(i)

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, config.LORA_NODE_DR)

# make the socket non-blocking
s.setblocking(False)

time.sleep(5.0)


for i in range (200):
    pycom.heartbeat(False)
    pycom.rgbled(0xffff00)
    lt = LTR329ALS01(py) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascal
    #print(lt.light())
    print("LTR329ALS01 light: " + str(lt.light()))
    li = float('.'.join(str(elem) for elem in lt.light()))
    #print(dir(lt.light()))

    li = li/10
    li= round(li)
    print(li)
    pr= MPL3115A2(py, mode=PRESSURE)
    print("la pressione e':" + str(pr.pressure()))
    pressure=pr.pressure()*10
    pressure=round(pressure)
    print(pressure)
    #si = SI7006A20(py)
    #print("Relative Humidity: " + str(si.humidity()) + " %RH")
    #= si.humidity()*10
    #humidity = round(humidity)
    # print(humidity)
    datal = bytearray(struct.pack("H",li))
    print(datal)
    datam = bytearray(struct.pack("L", pressure))
    print(datam)
    data_joined= datal+datam
    print("luce e pressione:"+str(data_joined))
    s.send(data_joined)
    pycom.heartbeat(True)

    time.sleep(6)
