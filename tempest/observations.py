import json
from webbrowser import get
from request import fetch_data, DEVICE_OBSERVATIONS
from datetime import datetime, timedelta

from os import environ


NOW = datetime.utcnow()
ONE_DAY_AGO = NOW - timedelta(hours=24)

# FIXME need to fetch or store this somehow
DEVICE_ID = 155234
# FIXME
TOKEN = environ["TEMPEST_TOKEN"]


def get_observations(type):
    return fetch_data(
        DEVICE_OBSERVATIONS(DEVICE_ID),
        dict(
            type=type,
            time_start=ONE_DAY_AGO.strftime("%s"),
            time_end=NOW.strftime("%s"),
            token=TOKEN,
        ),
    )


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
    def pressure(self):
        return self.values[6]

    @property
    def air_temperature(self):
        return self.values[7]

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
        for observation in observations:
            if tempest_type == "obs_st":
                self.append(Tempest(tempest_type, observation))
            if tempest_type == "obs_air":
                self.append(Air(tempest_type, observation))
            if tempest_type == "obs_sky":
                self.append(Sky(tempest_type, observation))
        return self


obs_resp = get_observations("obs_st")
obs = Observations.from_response(obs_resp)

print(obs)
