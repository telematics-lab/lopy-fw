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

""" LoPy LoRaWAN Nano Gateway configuration options """

import machine
import ubinascii
from network import LoRa
import ubinascii

#lora = LoRa()
#print("DevEUI: %s" % (ubinascii.hexlify(lora.mac()).decode('ascii')))

WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
# Set  the Gateway ID to be the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
DEV_EUI = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]
print("DEV_EUI", DEV_EUI)
SERVER = 'eu1.cloud.thethings.network'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

WIFI_SSID = 'xxxx'
WIFI_PASS = 'xxxx'

# for EU868
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF7BW125" # DR_5
LORA_NODE_DR = 5

# for US915
# LORA_FREQUENCY = 903900000
# LORA_GW_DR = "SF10BW125" # DR_0
# LORA_NODE_DR = 0
