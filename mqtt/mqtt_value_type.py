import json

import paho.mqtt.client as mqtt

from config import MQTT_BROKER_USERNAME, MQTT_BROKER_PASSWORD, MQTT_BROKER_IP, MQTT_BROKER_PORT
from global_variables import MQTT_VALUE_TYPES

_client_1 = None


def get_mqtt_client():
    global _client_1
    if _client_1 is None or not _client_1.is_connected():
        _client_1 = mqtt.Client()
        _client_1.username_pw_set(MQTT_BROKER_USERNAME, MQTT_BROKER_PASSWORD)
        _client_1.tls_set()
        _client_1.connect(MQTT_BROKER_IP, MQTT_BROKER_PORT)
    return _client_1


class MqttValueType:
    def __init__(self, value_name, friendly_name, state_topic, unit_of_measurement, state_class, device_class):
        self.value_name = value_name
        self.friendly_name = friendly_name
        self.state_topic = state_topic
        self.unit_of_measurement = unit_of_measurement
        self.state_class = state_class
        self.device_class = device_class
        self.payload_on = None
        self.payload_off = None

    @staticmethod
    def create_mqtt_value_type(value_name):
        config = MQTT_VALUE_TYPES[value_name]
        mqtt_value_type = MqttValueType(value_name, config["friendly_name"],
                                        config["state_topic"],
                                        config["unit_of_measurement"],
                                        config["state_class"], config["device_class"])
        if "payload_on" in config:
            mqtt_value_type.payload_on = config["payload_on"]
        if "payload_off" in config:
            mqtt_value_type.payload_off = config["payload_off"]
        return mqtt_value_type

    def get_unique_id(self):
        return self.friendly_name.replace(' ', '_').lower()

    def get_config_topic(self):
        return f"homeassistant/sensor/{self.get_unique_id()}/config"

    def get_config_payload(self):
        result = {
            "name": self.friendly_name,
            "state_topic": self.state_topic,
            "device_class": self.device_class,
            "state_class": self.state_class,
            "unique_id": self.get_unique_id(),
            "device": {
                "identifiers": ["zeus"],
                "name": "Zeus Energy Controller",
                "model": "python"
            }
        }
        if self.unit_of_measurement:
            result["unit_of_measurement"] = self.unit_of_measurement
        if self.state_class:
            result["state_class"] = self.state_class

        return result

    def publish_discovery_message(self):
        client = get_mqtt_client()
        client.publish(self.get_config_topic(), json.dumps(self.get_config_payload()), retain=True)

    def publish_value(self, value):
        client = get_mqtt_client()
        client.publish(self.state_topic, value, retain=True)
