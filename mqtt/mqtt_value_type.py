import json

import paho.mqtt.client as mqtt

from config import MQTT_BROKER_USERNAME, MQTT_BROKER_PASSWORD, MQTT_BROKER_IP, MQTT_BROKER_PORT, MQTT_VALUE_TYPES, \
    PV_POWER_W

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

    @staticmethod
    def create_mqtt_value_type(value_name):
        config = MQTT_VALUE_TYPES[value_name]
        return MqttValueType(value_name, config["friendly_name"], config["state_topic"], config["unit_of_measurement"],
                             config["state_class"], config["device_class"])

    def get_unique_id(self):
        return self.friendly_name.replace(' ', '_').lower()

    def get_config_topic(self):
        return f"homeassistant/sensor/{self.get_unique_id()}/config"
    
    def get_config_payload(self):
        return {
            "name": self.friendly_name,
            "state_topic": self.state_topic,
            "unit_of_measurement": self.unit_of_measurement,
            "device_class": self.device_class,
            "state_class": self.state_class,
            "unique_id": self.get_unique_id(),
            "device": {
                "identifiers": ["zeus"],
                "name": "Zeus Energy Controller",
                "model": "python"
            }
        }

    def publish_discovery_message(self):
        client = get_mqtt_client()
        client.publish(self.get_config_topic(), json.dumps(self.get_config_payload()), retain=True)

    def publish_value(self, value):
        client = get_mqtt_client()
        client.publish(self.state_topic, value, retain=True)


if __name__ == '__main__':
    test_type = MqttValueType.create_mqtt_value_type(PV_POWER_W)
    # test_type.publish_discovery_message()
    test_type.publish_value(1)
