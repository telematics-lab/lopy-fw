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

""" LoPy/FiPy LoRaWAN Nano Gateway configuration options """

import machine
import ubinascii

# A Gateway ID is created using the first 3 bytes of MAC address + 'FFFF' + last 3 bytes of MAC address
WIFI_MAC = ubinascii.hexlify(machine.unique_id()).upper()
GATEWAY_ID = WIFI_MAC[:6] + "FFFF" + WIFI_MAC[6:12]
print("GATEWAY_EUI", GATEWAY_ID)

SERVER = 'eu1.cloud.thethings.network'
PORT = 1700

NTP = "pool.ntp.org"
NTP_PERIOD_S = 3600

# Put here your WiFi settings to forward LoRa packets to TTN
WIFI_SSID = 'xxxx' 
WIFI_PASS = 'xxxx'

# Phisical layer configurations for a single channel LoRaWAN gateway
LORA_FREQUENCY = 868100000
LORA_GW_DR = "SF7BW125" # DR_5
