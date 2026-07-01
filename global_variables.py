PV_ENERGY_TOTAL = "pv_energy_total"
SOC_BATTERY_PERC = "soc_battery_perc"
PV_POWER_W = "pv_power_w"
BATTERY_DISCHARGING = "battery_discharging"
BATTERY_POWER_W = "battery_power_w"
ACTIVE_POWER = "active_power"
WATTAGE_TO_GRID = "energy_to_grid"
BATTERY_CHARGING_POWER_W = "battery_charging_power_w"
BATTERY_DISCHARGING_POWER_W = "battery_discharging_power_w"


# Modbus registers to log
REGISTERS_TO_LOG = {
    33029: PV_ENERGY_TOTAL,
    33139: SOC_BATTERY_PERC,  # "SOC battery (%)",
    # 33073: "phase A voltage",
    # 33076: "phase A current",
    33057: PV_POWER_W,  # "PV power (W)",
    33135: BATTERY_DISCHARGING,  # "Battery direction",
    33149: BATTERY_POWER_W,
    # "Battery power (W)",   value is enriched by script with charging direction, negative means the battery is charging.
    33079: ACTIVE_POWER,  # "Active power (W)",
    33083: WATTAGE_TO_GRID,  # "Meter total apparent power",  # Meter total apparent power
}


_VALUE_TYPES = {
    PV_POWER_W: {"friendly_name": "Current Solar Power",
                 "state_topic": "homeassistant/energy/solar_power/state",
                 "unit_of_measurement": "W",
                 "state_class": "measurement",
                 "device_class": "power"},
    BATTERY_POWER_W: {"friendly_name": "Current Battery Power",
                      "state_topic": "homeassistant/energy/battery_power/state",
                      "unit_of_measurement": "W",
                      "state_class": "measurement",
                      "device_class": "power"},
    BATTERY_CHARGING_POWER_W: {"friendly_name": "Current Battery Charging Power",
                               "state_topic": "homeassistant/energy/battery_charging_power/state",
                               "unit_of_measurement": "W",
                               "state_class": "measurement",
                               "device_class": "power"},
    BATTERY_DISCHARGING_POWER_W: {"friendly_name": "Current Battery Discharging Power",
                                  "state_topic": "homeassistant/energy/battery_discharging_power/state",
                                  "unit_of_measurement": "W",
                                  "state_class": "measurement",
                                  "device_class": "power"},
    SOC_BATTERY_PERC: {"friendly_name": "Battery Charge Level",
                       "state_topic": "homeassistant/energy/battery_charge_percent/state",
                       "unit_of_measurement": "%",
                       "state_class": "measurement",
                       "device_class": "energy"},
    PV_ENERGY_TOTAL: {"friendly_name": "Solar Energy Total",
                      "state_topic": "homeassistant/energy/solar_energy/state",
                      "unit_of_measurement": "Wh",
                      "state_class": "total_increasing",
                      "device_class": "energy"},
}