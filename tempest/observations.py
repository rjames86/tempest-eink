from tempest.request import fetch_data, DEVICE_OBSERVATIONS_URL
from datetime import datetime, timedelta
import math

from os import environ


NOW = datetime.utcnow()
ONE_DAY_AGO = NOW - timedelta(hours=24)

# FIXME need to fetch or store this somehow
DEVICE_ID = 155234
# FIXME
TOKEN = environ["TEMPEST_TOKEN"]


class Observation:
    def __init__(self, type, values):
        self.type = type
        self.values = values

    def __repr__(self):
        return "<%s type=%r>" % (
            self.__class__.__name__,
            self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        )

    @property
    def time(self):
        return self.values[0]

    @property
    def timestamp(self):
        # Epoch UTC is always the first value in values
        return datetime.fromtimestamp(self.values[0])


class Air(Observation):
    @property
    def station_pressure(self):
        pass

    @property
    def air_pressure(self):
        pass

    @property
    def relative_humidity(self):
        pass

    @property
    def lightning_strike_count(self):
        pass

    @property
    def lightning_strike_average_distance(self):
        pass

    @property
    def battery(self):
        pass

    @property
    def report_intervals(self):
        pass


class Sky(Observation):
    @property
    def station_pressure(self):
        pass

    @property
    def illuminance(self):
        pass

    @property
    def uv(self):
        pass

    @property
    def rain_accumulation(self):
        pass

    @property
    def wing_lull(self):
        pass

    @property
    def wing_avg(self):
        pass

    @property
    def wind_gust(self):
        pass

    @property
    def wind_direction(self):
        pass

    @property
    def battery(self):
        pass

    @property
    def report_interval(self):
        pass

    @property
    def solar_radiation(self):
        pass

    @property
    def local_day_rain_accumulation(self):
        pass

    @property
    def precipitation_type(self):
        pass

    @property
    def wind(self):
        pass


class Tempest(Observation):
    @property
    def wind_lull(self):
        return self.values[1]

    @property
    def wind_avg(self):
        return self.values[2]

    @property
    def wind_gust(self):
        return self.values[3]

    @property
    def wind_direction(self):
        return self.values[4]

    @property
    def wind_sample_interval(self):
        return self.values[5]

    @property
    def sea_level_pressure(self):
        # https://weatherflow.github.io/Tempest/api/derived-metric-formulas.html
        e = 1065.0316162109375  # hard coded elevation
        sea_level_pressure = self.pressure * pow(
            1
            + pow(1013.25 / self.pressure, 1.865825 / 9.80665) * (0.0065 * e / 288.15),
            9.80665 / 1.865825,
        )
        return sea_level_pressure * 0.029529980164712

    @property
    def pressure(self):
        return self.values[6] * 0.029529980164712

    @property
    def air_temperature(self):
        return (self.values[7] * 1.8) + 32

    @property
    def relative_humidity(self):
        return self.values[8]

    @property
    def illuminance(self):
        return self.values[9]

    @property
    def uv(self):
        return self.values[10]

    @property
    def solar_radiation(self):
        return self.values[11]

    @property
    def rain_accumulation(self):
        return self.values[12]

    @property
    def precipitation_type(self):
        return self.values[13]

    @property
    def average_strike_count(self):
        return self.values[14]

    @property
    def strike_count(self):
        return self.values[15]

    @property
    def battery(self):
        return self.values[16]

    @property
    def report_interval(self):
        return self.values[17]

    @property
    def local_day_rain_accumulation(self):
        return self.values[18]


class Observations(list):
    @classmethod
    def from_response(cls, json_data):
        self = cls()
        tempest_type = json_data["type"]
        observations = json_data.get("obs") or []
        print(tempest_type)
        for observation in observations:
            if tempest_type == "obs_st":
                self.append(Tempest(tempest_type, observation))
            if tempest_type == "obs_air":
                self.append(Air(tempest_type, observation))
            if tempest_type == "obs_sky":
                self.append(Sky(tempest_type, observation))
        return self


def get_observations(obs_type="obs_air"):
    resp = fetch_data(
        DEVICE_OBSERVATIONS_URL(DEVICE_ID),
        dict(
            type=obs_type,
            time_start=ONE_DAY_AGO.strftime("%s"),
            time_end=NOW.strftime("%s"),
            token=TOKEN,
        ),
    )
    return Observations.from_response(resp)
