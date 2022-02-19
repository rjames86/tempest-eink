from os import environ

from tempest.request import FORECAST_URL, fetch_data

TOKEN = environ["TEMPEST_TOKEN"]


class BetterForecastHourlyForecast:
    def __init__(
        self,
        time,
        conditions,
        icon,
        air_temperature,
        sea_level_pressure,
        relative_humidity,
        precip,
        precip_probability,
        wind_avg,
        wind_direction,
        wind_direction_cardinal,
        wind_gust,
        uv,
        feels_like,
        local_hour,
        local_day,
    ):
        self.time = time
        self.conditions = conditions
        self.icon = icon
        self.air_temperature = air_temperature
        self.sea_level_pressure = sea_level_pressure
        self.relative_humidity = relative_humidity
        self.precip = precip
        self.precip_probability = precip_probability
        self.wind_avg = wind_avg
        self.wind_direction = wind_direction
        self.wind_direction_cardinal = wind_direction_cardinal
        self.wind_gust = wind_gust
        self.uv = uv
        self.feels_like = feels_like
        self.local_hour = local_hour
        self.local_day = local_day

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data.get("time"),
            json_data.get("conditions"),
            json_data.get("icon"),
            json_data.get("air_temperature"),
            json_data.get("sea_level_pressure"),
            json_data.get("relative_humidity"),
            json_data.get("precip"),
            json_data.get("precip_probability"),
            json_data.get("wind_avg"),
            json_data.get("wind_direction"),
            json_data.get("wind_direction_cardinal"),
            json_data.get("wind_gust"),
            json_data.get("uv"),
            json_data.get("feels_like"),
            json_data.get("local_hour"),
            json_data.get("local_day"),
        )


class BetterForecastDailyForecast:
    def __init__(
        self,
        day_start_local,
        day_num,
        month_num,
        conditions,
        icon,
        sunrise,
        sunset,
        air_temp_high,
        air_temp_low,
        precip_probability,
        precip_icon,
        precip_type,
    ):
        self.day_start_local = day_start_local
        self.day_num = day_num
        self.month_num = month_num
        self.conditions = conditions
        self.icon = icon
        self.sunrise = sunrise
        self.sunset = sunset
        self.air_temp_high = air_temp_high
        self.air_temp_low = air_temp_low
        self.precip_probability = precip_probability
        self.precip_icon = precip_icon
        self.precip_type = precip_type

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data.get("day_start_local"),
            json_data.get("day_num"),
            json_data.get("month_num"),
            json_data.get("conditions"),
            json_data.get("icon"),
            json_data.get("sunrise"),
            json_data.get("sunset"),
            json_data.get("air_temp_high"),
            json_data.get("air_temp_low"),
            json_data.get("precip_probability"),
            json_data.get("precip_icon"),
            json_data.get("precip_type"),
        )


class BetterForecastForecast:
    def __init__(self, daily, hourly):
        self.daily = daily
        self.hourly = hourly

    @classmethod
    def from_json(cls, json_data):
        daily = map(BetterForecastDailyForecast.from_json, json_data.get("daily"))
        hourly = map(BetterForecastHourlyForecast.from_json, json_data.get("hourly"))
        return cls(daily, hourly)


class BetterForecastUnits:
    def __init__(
        self,
        units_temp,
        units_wind,
        units_precip,
        units_pressure,
        units_distance,
        units_brightness,
        units_solar_radiation,
        units_other,
        units_air_density,
    ):
        self.units_temp = units_temp
        self.units_wind = units_wind
        self.units_precip = units_precip
        self.units_pressure = units_pressure
        self.units_distance = units_distance
        self.units_brightness = units_brightness
        self.units_solar_radiation = units_solar_radiation
        self.units_other = units_other
        self.units_air_density = units_air_density

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data.get("units_temp"),
            json_data.get("units_wind"),
            json_data.get("units_precip"),
            json_data.get("units_pressure"),
            json_data.get("units_distance"),
            json_data.get("units_brightness"),
            json_data.get("units_solar_radiation"),
            json_data.get("units_other"),
            json_data.get("units_air_density"),
        )

    def units_temp_letter(self):
        print("calling units temp", self.units_temp)
        if self.units_temp == "f":
            return "+"
        else:
            return "*"


class BetterForecastCurrentConditions:
    def __init__(
        self,
        time,
        conditions,
        icon,
        air_temperature,
        sea_level_pressure,
        station_pressure,
        pressure_trend,
        relative_humidity,
        wind_avg,
        wind_direction,
        wind_direction_cardinal,
        wind_direction_icon,
        wind_gust,
        solar_radiation,
        uv,
        brightness,
        feels_like,
        dew_point,
        wet_bulb_temperature,
        delta_t,
        air_density,
        lightning_strike_count_last_1hr,
        lightning_strike_count_last_3hr,
        lightning_strike_last_distance,
        lightning_strike_last_distance_msg,
        lightning_strike_last_epoch,
        precip_accum_local_day,
        precip_accum_local_yesterday,
        precip_minutes_local_day,
        precip_minutes_local_yesterday,
        is_precip_local_day_rain_check,
        is_precip_local_yesterday_rain_check,
    ):
        self.time = time
        self.conditions = conditions
        self.icon = icon
        self.air_temperature = air_temperature
        self.sea_level_pressure = sea_level_pressure
        self.station_pressure = station_pressure
        self.pressure_trend = pressure_trend
        self.relative_humidity = relative_humidity
        self.wind_avg = wind_avg
        self.wind_direction = wind_direction
        self.wind_direction_cardinal = wind_direction_cardinal
        self.wind_direction_icon = wind_direction_icon
        self.wind_gust = wind_gust
        self.solar_radiation = solar_radiation
        self.uv = uv
        self.brightness = brightness
        self.feels_like = feels_like
        self.dew_point = dew_point
        self.wet_bulb_temperature = wet_bulb_temperature
        self.delta_t = delta_t
        self.air_density = air_density
        self.lightning_strike_count_last_1hr = lightning_strike_count_last_1hr
        self.lightning_strike_count_last_3hr = lightning_strike_count_last_3hr
        self.lightning_strike_last_distance = lightning_strike_last_distance
        self.lightning_strike_last_distance_msg = lightning_strike_last_distance_msg
        self.lightning_strike_last_epoch = lightning_strike_last_epoch
        self.precip_accum_local_day = precip_accum_local_day
        self.precip_accum_local_yesterday = precip_accum_local_yesterday
        self.precip_minutes_local_day = precip_minutes_local_day
        self.precip_minutes_local_yesterday = precip_minutes_local_yesterday
        self.is_precip_local_day_rain_check = is_precip_local_day_rain_check
        self.is_precip_local_yesterday_rain_check = is_precip_local_yesterday_rain_check

    @classmethod
    def from_json(cls, json_data):
        return cls(
            json_data.get("time"),
            json_data.get("conditions"),
            json_data.get("icon"),
            json_data.get("air_temperature"),
            json_data.get("sea_level_pressure"),
            json_data.get("station_pressure"),
            json_data.get("pressure_trend"),
            json_data.get("relative_humidity"),
            json_data.get("wind_avg"),
            json_data.get("wind_direction"),
            json_data.get("wind_direction_cardinal"),
            json_data.get("wind_direction_icon"),
            json_data.get("wind_gust"),
            json_data.get("solar_radiation"),
            json_data.get("uv"),
            json_data.get("brightness"),
            json_data.get("feels_like"),
            json_data.get("dew_point"),
            json_data.get("wet_bulb_temperature"),
            json_data.get("delta_t"),
            json_data.get("air_density"),
            json_data.get("lightning_strike_count_last_1hr"),
            json_data.get("lightning_strike_count_last_3hr"),
            json_data.get("lightning_strike_last_distance"),
            json_data.get("lightning_strike_last_distance_msg"),
            json_data.get("lightning_strike_last_epoch"),
            json_data.get("precip_accum_local_day"),
            json_data.get("precip_accum_local_yesterday"),
            json_data.get("precip_minutes_local_day"),
            json_data.get("precip_minutes_local_yesterday"),
            json_data.get("is_precip_local_day_rain_check"),
            json_data.get("is_precip_local_yesterday_rain_check"),
        )

    def get_icon_letter(self):
        icon_mapping = {
            "clear-day": "B",
            "clear-night": "C",
            "cloudy": "N",
            "foggy": "M",
            "partly-cloudy-day": "H",
            "partly-cloudy-night": "I",
            "possibly-rainy-day": "Q",
            "possibly-rainy-night": "Q",
            "possibly-sleet-day": "X",
            "possibly-sleet-night": "X",
            "possibly-snow-day": "W",
            "possibly-snow-night": "W",
            "possibly-thunderstorm-day": "0",
            "possibly-thunderstorm-night": "0",
            "rainy": "R",
            "sleet": "X",
            "snow": "W",
            "thunderstorm": "0",
            "windy": "F",
        }
        return icon_mapping.get(self.icon, ")")


class Status:
    def __init__(self, status_code, status_message):
        self.status_code = status_code
        self.status_message = status_message

    @classmethod
    def from_json(cls, json_data):
        return cls(json_data.get("status_code"), json_data.get("status_message"))


class BetterForecast:
    def __init__(
        self,
        status,
        current_conditions,
        forecast,
        units,
        latitude,
        longitude,
        timezone,
        timezone_offset_minutes,
    ):
        self.status = status
        self.current_conditions = current_conditions
        self.forecast = forecast
        self.units = units
        self.latitude = latitude
        self.longitude = longitude
        self.timezone = timezone
        self.timezone_offset_minutes = timezone_offset_minutes

    @classmethod
    def from_response(cls, json_data):
        return cls(
            Status.from_json(json_data.get("status")),
            BetterForecastCurrentConditions.from_json(
                json_data.get("current_conditions")
            ),
            BetterForecastForecast.from_json(json_data.get("forecast")),
            BetterForecastUnits.from_json(json_data.get("units")),
            json_data.get("latitude"),
            json_data.get("longitude"),
            json_data.get("timezone"),
            json_data.get("timezone_offset_minutes"),
        )


def get_forecast():
    resp = fetch_data(
        FORECAST_URL,
        dict(
            station_id=55396,
            token=TOKEN,
            units_temp="f",
            units_wind="mph",
            units_pressure="inhg",
            units_precip="in",
            units_distance="mi",
        ),
    )
    return BetterForecast.from_response(resp)
