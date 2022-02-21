import json
from os import path
import pathlib
from datetime import datetime

CURRENT_PATH = pathlib.Path(__file__).parent.absolute()
CONFIG_PATH = path.join(CURRENT_PATH, "config.json")

default_config = dict(
    token="",
    device_id="",
    station_id="",
    units_temp="f",
    units_wind="mph",
    units_pressure="inhg",
    units_precip="in",
    units_distance="mi",
    elevation=0,
    on_time="05:00",
    off_time="23:00",
    is_on=True,
    include_daily_forecast=True,
)


def create_or_get_config(recreate=False):
    if not path.exists(CONFIG_PATH) or recreate is True:
        print("config doesnt exist")
        with open(CONFIG_PATH, "w") as f:
            json.dump(default_config, f)
    return json.load(open(CONFIG_PATH))


def save_config(new_config):
    print("new config", new_config)
    with open(CONFIG_PATH, "w") as f:
        json.dump(new_config, f)


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
        include_daily_forecast=True,
        *args,
        **kwargs,
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
        self.on_time = datetime.strptime(on_time, "%H:%M").time()
        self.off_time = datetime.strptime(off_time, "%H:%M").time()
        self.is_on = is_on
        self.include_daily_forecast = include_daily_forecast

    def as_json(self):
        return dict(
            token=self.token,
            device_id=self.device_id,
            station_id=self.station_id,
            units_temp=self.units_temp,
            units_wind=self.units_wind,
            units_pressure=self.units_pressure,
            units_precip=self.units_precip,
            units_distance=self.units_distance,
            elevation=self.elevation,
            on_time=self.on_time.strftime("%H:%M"),
            off_time=self.off_time.strftime("%H:%M"),
            is_on=self.is_on,
            include_daily_forecast=self.include_daily_forecast,
        )

    @classmethod
    def from_json(cls):
        json_data = create_or_get_config()
        print("data in from_json", json_data)
        return cls(**json_data)


CONFIG = Config.from_json()
