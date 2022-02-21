import json
from os import path

CONFIG_PATH = "config.json"

config_data = json.load(open(CONFIG_PATH))


def config_exists():
    return path.exists(CONFIG_PATH)


class Config:
    def __init__(
        self,
        token,
        device_id,
        station_id,
        units_temp,
        units_wind,
        units_pressure,
        units_precip,
        units_distance,
        elevation,
        on_time,
        off_time,
        is_on,
    ):
        self.token = token
        self.device_id = device_id
        self.station_id = station_id
        self.units_temp = units_temp
        self.units_wind = units_wind
        self.units_pressure = units_pressure
        self.units_precip = units_precip
        self.units_distance = units_distance
        self.elevation = elevation
        self.on_time = on_time
        self.off_time = off_time
        self.is_on = is_on

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data["token"],
            json_data["device_id"],
            json_data["station_id"],
            json_data["units_temp"],
            json_data["units_wind"],
            json_data["units_pressure"],
            json_data["units_precip"],
            json_data["units_distance"],
            json_data["elevation"],
            json_data["on_time"],
            json_data["off_time"],
            json_data["is_on"],
        )


CONFIG = Config.from_json(config_data)