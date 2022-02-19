import requests

BASE_URL = "https://swd.weatherflow.com/swd/rest"

DEVICE_OBSERVATIONS = lambda device_id: "%s/observations/device/%s" % (
    BASE_URL,
    device_id,
)
FORECAST = BASE_URL + "/better_forecast"


def fetch_data(url, params):
    return requests.get(url, params=params).json()