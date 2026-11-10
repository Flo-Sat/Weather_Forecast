from dotenv import dotenv_values
import time
from datetime import datetime, timedelta
import requests
import pandas as pd


def query_forecast(config):
    weather_url = config["API_KEY_FORECAST"]
    response = requests.get(weather_url)
    response.json()

    forecast = response.json()["hourly"]
    print(forecast.keys())
    time=forecast["time"]
    temp=forecast["temperature_2m"]
    rain=forecast["rain"]
    return(pd.DataFrame({   
        "time": time,
        "temp": temp,
        "rain": rain
        }).set_index("time"))

def construct_url (root, first, last, parameter):
    first_ts = first.isoformat(timespec="seconds")
    last_ts = last.isoformat(timespec="seconds")
    return f"{root}&parameterId={parameter}&datetime={first_ts}%2B02:00/{last_ts}%2B02:00"


def query_station(config):
    timestamp = datetime.now().isoformat(timespec="seconds")
    api_url =f"{config["API_KEY_STATION_KOLDING"]}&datetime={timestamp}%2B02:00/.."
    response = requests.get(api_url)
    return(process_station(response))


def process_station(response):
    rows_dict = {}
    for feature in response.json()["features"]:
        properties = feature["properties"]
        rows_dict.setdefault(properties["observed"], {})[properties["parameterId"]] = properties["value"]
    return pd.DataFrame.from_dict(rows_dict, orient="index")
