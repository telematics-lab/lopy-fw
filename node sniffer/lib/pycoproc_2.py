#!/usr/bin/env python
#
# Copyright (c) 2020, Pycom Limited.
#
# This software is licensed under the GNU GPL version 3 or any
# later version, with permitted additional terms. For more information
# see the Pycom Licence v1.0 document supplied with this file, or
# available at https://www.pycom.io/opensource/licensing
#

# See https://docs.pycom.io for more information regarding library specifics

from machine import Pin
from machine import I2C
import time
import pycom

__version__ = '0.0.5'

""" PIC MCU wakeup reason types """
WAKE_REASON_ACCELEROMETER = 1
WAKE_REASON_PUSH_BUTTON = 2
WAKE_REASON_TIMER = 4
WAKE_REASON_INT_PIN = 8

class Pycoproc:
    """ class for handling the interaction with PIC MCU """

    I2C_SLAVE_ADDR = const(8)

    CMD_PEEK = const(0x0)
    CMD_POKE = const(0x01)
    CMD_MAGIC = const(0x02)
    CMD_HW_VER = const(0x10)
    CMD_FW_VER = const(0x11) #define SW_VERSION (15)
    CMD_PROD_ID = const(0x12) #USB product ID, e.g. PYSENSE (0xF012)
    CMD_SETUP_SLEEP = const(0x20)
    CMD_GO_SLEEP = const(0x21)
    CMD_CALIBRATE = const(0x22)
    CMD_GO_NAP = const(0x23)
    CMD_BAUD_CHANGE = const(0x30)
    CMD_DFU = const(0x31)
    CMD_RESET = const(0x40)
    # CMD_GO_NAP options
    SD_CARD_OFF       = const(0x1)
    SENSORS_OFF       = const(0x2)
    ACCELEROMETER_OFF = const(0x4)
    FIPY_OFF          = const(0x8)


    REG_CMD = const(0)
    REG_ADDRL = const(1)
    REG_ADDRH = const(2)
    REG_AND = const(3)
    REG_OR = const(4)
    REG_XOR = const(5)

    ANSELA_ADDR = const(0x18C)
    ANSELB_ADDR = const(0x18D)
    ANSELC_ADDR = const(0x18E)

    ADCON0_ADDR = const(0x9D)
    ADCON1_ADDR = const(0x9E)

    IOCAP_ADDR = const(0x391)
    IOCAN_ADDR = const(0x392)

    INTCON_ADDR = const(0x0B)
    OPTION_REG_ADDR = const(0x95)

    _ADCON0_CHS_POSN = const(0x02)
    _ADCON0_CHS_AN5 = const(0x5) # AN5 / RC1
    _ADCON0_CHS_AN6 = const(0x6) # AN6 / RC2
    _ADCON0_ADON_MASK = const(0x01)
    _ADCON0_ADCS_F_OSC_64 = const(0x6) #  A/D Conversion Clock
    _ADCON0_GO_nDONE_MASK = const(0x02)
    _ADCON1_ADCS_POSN = const(0x04)

    ADRESL_ADDR = const(0x09B)
    ADRESH_ADDR = const(0x09C)

    TRISA_ADDR = const(0x08C)
    TRISB_ADDR = const(0x08D)
    TRISC_ADDR = const(0x08E)

    LATA_ADDR = const(0x10C)
    LATB_ADDR = const(0x10D)
    LATC_ADDR = const(0x10E)

    PORTA_ADDR = const(0x00C)
    PORTB_ADDR = const(0x00C)
    PORTC_ADDR = const(0x00E)

    WPUA_ADDR = const(0x20C)

    WAKE_REASON_ADDR = const(0x064C)
    MEMORY_BANK_ADDR = const(0x0620)

    PCON_ADDR = const(0x096)
    STATUS_ADDR = const(0x083)

    EXP_RTC_PERIOD = const(7000)

    USB_PID_PYSENSE = const(0xf012)
    USB_PID_PYTRACK = const(0xf013)

    @staticmethod
    def wake_up():
        # P9 is connected to RC1, make P9 an output
        p9 = Pin("P9", mode=Pin.OUT)
        # toggle rc1 to trigger wake up
        p9(1)
        time.sleep(0.1)
        p9(0)
        time.sleep(0.1)

    def __init__(self, i2c=None, sda='P22', scl='P21'):
        if i2c is not None:
            self.i2c = i2c
        else:
            self.i2c = I2C(0, mode=I2C.MASTER, pins=(sda, scl), baudrate=100000)

        self.sda = sda
        self.scl = scl
        self.clk_cal_factor = 1
        self.reg = bytearray(6)

        # Make sure we are inserted into the
        # correct board and can talk to the PIC
        retry = 0
        while True:
            try:
                self.read_fw_version()
                break
            except Exception as e:
                if retry > 10:
                    raise Exception('Board not detected: {}'.format(e))
                print("Couldn't init Pycoproc. Maybe the PIC is still napping. Try to wake it. ({}, {})".format(retry, e))
                Pycoproc.wake_up()
                # # p9 is connected to RC1, toggle it to wake PIC
                # p9 = Pin("P9", mode=Pin.OUT)
                # p9(1)
                # time.sleep(0.1)
                # p9(0)
                # time.sleep(0.1)
                # Pin("P9", mode=Pin.IN)
                retry += 1

        usb_pid=self.read_product_id()
        if usb_pid != USB_PID_PYSENSE and usb_pid != USB_PID_PYTRACK:
            raise ValueError('Not a Pysense2/Pytrack2 ({})'.format(hex(usb_pid)))
        # for Pysense/Pytrack 2.0, the minimum firmware version is 15
        fw = self.read_fw_version()
        if fw < 16:
            raise ValueError('Firmware for Shield2 out of date', fw)

        # init the ADC for the battery measurements
        self.write_byte(ANSELC_ADDR, 1 << 2) # RC2 analog input
        self.write_byte(ADCON0_ADDR, (_ADCON0_CHS_AN6 << _ADCON0_CHS_POSN) | _ADCON0_ADON_MASK) # select analog channel and enable ADC
        self.write_byte(ADCON1_ADDR, (_ADCON0_ADCS_F_OSC_64 << _ADCON1_ADCS_POSN)) # ADC conversion clock

        # enable the pull-up on RA3
        self.write_byte(WPUA_ADDR, (1 << 3))

        # set RC6 and RC7 as outputs
        self.write_bit(TRISC_ADDR, 6, 0) # 3V3SENSOR_A, power to Accelerometer
        self.write_bit(TRISC_ADDR, 7, 0) # PWR_CTRL power to other sensors

        # enable power to the sensors and the GPS
        self.gps_standby(False) # GPS, RC4
        self.sensor_power() # PWR_CTRL, RC7
        self.sd_power() # LP_CTRL, RA5


    def _write(self, data, wait=True):
        self.i2c.writeto(I2C_SLAVE_ADDR, data)
        if wait:
            self._wait()

    def _read(self, size):
        return self.i2c.readfrom(I2C_SLAVE_ADDR, size + 1)[1:(size + 1)]

    def _wait(self):
        count = 0
        time.sleep_us(10)
        while self.i2c.readfrom(I2C_SLAVE_ADDR, 1)[0] != 0xFF:
            time.sleep_us(100)
            count += 1
            if (count > 500):  # timeout after 50ms
                raise Exception('Board timeout')

    def _send_cmd(self, cmd):
        self._write(bytes([cmd]))

    def read_hw_version(self):
        self._send_cmd(CMD_HW_VER)
        d = self._read(2)
        return (d[1] << 8) + d[0]

    def read_fw_version(self):
        self._send_cmd(CMD_FW_VER)
        d = self._read(2)
        return (d[1] << 8) + d[0]

    def read_product_id(self):
        self._send_cmd(CMD_PROD_ID)
        d = self._read(2)
        return (d[1] << 8) + d[0]

    def read_byte(self, addr):
        self._write(bytes([CMD_PEEK, addr & 0xFF, (addr >> 8) & 0xFF]))
        return self._read(1)[0]

    def write_byte(self, addr, value):
        self._write(bytes([CMD_POKE, addr & 0xFF, (addr >> 8) & 0xFF, value & 0xFF]))

    def magic_write_read(self, addr, _and=0xFF, _or=0, _xor=0):
        self._write(bytes([CMD_MAGIC, addr & 0xFF, (addr >> 8) & 0xFF, _and & 0xFF, _or & 0xFF, _xor & 0xFF]))
        return self._read(1)[0]

    def toggle_bits_in_memory(self, addr, bits):
        self.magic_write_read(addr, _xor=bits)

    def mask_bits_in_memory(self, addr, mask):
        self.magic_write_read(addr, _and=mask)

    def set_bits_in_memory(self, addr, bits):
        self.magic_write_read(addr, _or=bits)

    def read_bit(self, address, bit):
        b = self.read_byte(address)
        # print("{0:08b}".format(b))
        mask = (1<<bit)
        # print("{0:08b}".format(mask))
        # print("{0:08b}".format(b & mask))
        if b & mask:
            return 1
        else:
            return 0

    def write_bit(self, address, bit, level):
        if level == 1:
            self.set_bits_in_memory(address, (1<<bit) )
        elif level == 0:
            self.mask_bits_in_memory(address, ~(1<<bit) )
        else:
            raise Exception("level", level)

    def setup_sleep(self, time_s):
        try:
            time.sleep_ms(30) # sleep before the calibrate, to make sure all preceeding repl communication has finished. In my tests 20ms was enough, make it 30ms to have some slack
            # note: calibrate_rtc will interrupt the UART, means we temporarily lose REPL. the serial terminal in use may or may not succeed in reconnecting immediately/automatically, e.g. atom/pymakr
            self.calibrate_rtc()
        except Exception:
            pass
        time_s = int((time_s * self.clk_cal_factor) + 0.5)  # round to the nearest integer
        if time_s >= 2**(8*3):
            time_s = 2**(8*3)-1
        self._write(bytes([CMD_SETUP_SLEEP, time_s & 0xFF, (time_s >> 8) & 0xFF, (time_s >> 16) & 0xFF]))

    def go_to_sleep(self, gps=True, pycom_module_off=True, accelerometer_off=True, wake_interrupt=False):
        # enable or disable back-up power to the GPS receiver
        self.gps_standby(gps)

        # disable the ADC
        self.write_byte(ADCON0_ADDR, 0)

        # RC0, RC1, RC2, analog input
        self.set_bits_in_memory(TRISC_ADDR, (1<<2) | (1<<1) | (1<<0) )
        self.set_bits_in_memory(ANSELC_ADDR, (1<<2) | (1<<1) | (1<<0) )

        # RA4 analog input
        self.set_bits_in_memory(TRISA_ADDR, (1<<4) )
        self.set_bits_in_memory(ANSELA_ADDR, (1<<4) )

        # RB4, RB5 analog input
        self.set_bits_in_memory(TRISB_ADDR, (1<<5) | (1<<4) )
        self.set_bits_in