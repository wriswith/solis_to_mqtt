import time

import minimalmodbus

from config import COMM_PORT, COMM_BAUD_RATE, COMM_TIMEOUT, COMM_PARITY, COMM_BYTE_SIZE, COMM_STOP_BITS
from global_variables import REGISTERS_TO_LOG
from mqtt.log_to_mqtt import publish_mqtt_discovery_messages, push_readings_to_mqtt


def poll_server():
    publish_mqtt_discovery_messages()

    instrument = minimalmodbus.Instrument(COMM_PORT, 1)
    instrument.serial.baudrate = COMM_BAUD_RATE
    instrument.serial.bytesize = COMM_BYTE_SIZE
    instrument.serial.parity = COMM_PARITY
    instrument.serial.stopbits = COMM_STOP_BITS
    instrument.serial.timeout = COMM_TIMEOUT

    while True:
        readings = []
        for register in REGISTERS_TO_LOG:
            value = instrument.read_register(register, functioncode=4)
            readings.append((REGISTERS_TO_LOG[register], value, time.time()))
            print(f"{REGISTERS_TO_LOG[register]}: {value}")
            time.sleep(0.3)

        push_readings_to_mqtt(readings)


if __name__ == '__main__':
    poll_server()