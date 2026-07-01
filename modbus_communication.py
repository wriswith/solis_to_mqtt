import minimalmodbus

from config import COMM_PORT


def poll_server():
    instrument = minimalmodbus.Instrument(COMM_PORT, 1)
    print(instrument.read_register(33139))


if __name__ == '__main__':
    poll_server()