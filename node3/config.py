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

""" LoPy/FiPy LoRaWAN node configuration options """

import machine
import ubinascii
from network import LoRa
import ubinascii

# A Device ID is created using the first 3 bytes of MAC address + 'FFFE' + last 3 bytes of MAC address
WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
DEV_EUI = WIFI_MAC[:6] + "FFFE" + WIFI_MAC[6:12]
print("DEV_EUI", DEV_EUI)

# Set True when using a single channel Gateway, False otherwise  
SINGLE_CHANNEL = True

# Phisical layer configurations for a single channel LoRaWAN node
LORA_FREQUENCY = 868100000
LORA_NODE_DR = 5
