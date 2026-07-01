import time

import minimalmodbus

from config import COMM_PORT, COMM_BAUD_RATE, COMM_TIMEOUT, COMM_PARITY, COMM_BYTE_SIZE, COMM_STOP_BITS
from global_variables import REGISTERS_TO_LOG


def poll_server():
    instrument = minimalmodbus.Instrument(COMM_PORT, 1)
    instrument.serial.baudrate = COMM_BAUD_RATE
    instrument.serial.bytesize = COMM_BYTE_SIZE
    instrument.serial.parity = COMM_PARITY
    instrument.serial.stopbits = COMM_STOP_BITS
    instrument.serial.timeout = COMM_TIMEOUT

    for register in REGISTERS_TO_LOG:
        value = instrument.read_register(register)
        print(f"{REGISTERS_TO_LOG[register]}: {value}")
        print(instrument.read_register(33139, functioncode=4))
        time.sleep(0.1)


if __name__ == '__main__':
    poll_server()