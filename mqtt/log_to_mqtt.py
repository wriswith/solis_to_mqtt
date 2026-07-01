import logging

from global_variables import MQTT_VALUE_TYPES
from mqtt.mqtt_value_type import MqttValueType

_mqtt_value_types = None


def get_mqtt_value_types():
    global _mqtt_value_types
    if _mqtt_value_types is None:
        _mqtt_value_types = {}
        for value_type_name in MQTT_VALUE_TYPES:
            _mqtt_value_types[value_type_name] = MqttValueType.create_mqtt_value_type(value_type_name)
    return _mqtt_value_types


def push_readings_to_mqtt(readings):
    mqtt_value_types = get_mqtt_value_types()
    for reading_name, reading_value, timestamp in readings:
        logging.info(f"Reading {reading_name} -> {reading_value}")
        if reading_name in mqtt_value_types:
            mqtt_value_types[reading_name].publish_value(reading_value)
            logging.info(f"Published reading {reading_name} value {reading_value}.")


def publish_mqtt_discovery_messages():
    mqtt_value_types = get_mqtt_value_types()
    for value_type_name in mqtt_value_types:
        mqtt_value_types[value_type_name].publish_discovery_message()
