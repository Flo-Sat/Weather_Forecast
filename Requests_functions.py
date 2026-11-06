from dotenv import dotenv_values
from datetime import datetime
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
        }))

def query_station(config):

    timestamp = datetime.now().isoformat(timespec="seconds")
    api_url =f"{config["API_KEY_STATION_KOLDING"]}&datetime={timestamp}%2B02:00/.."
    response = requests.get(api_url)

    df_data = pd.DataFrame(columns = ["temp_dry","wind_speed"])
    observed =""
    rows_dict={}
    for datalist in response.json()["features"]:
        properties = datalist["properties"]
        if properties["observed"] != observed : 
            observed = properties["observed"]
        if properties["parameterId"] == "temp_dry" or properties["parameterId"] == "wind_speed":
            rows_dict.setdefault(properties["observed"], {})[properties["parameterId"]] = properties["value"]
    df_temp = pd.DataFrame.from_dict(rows_dict,orient="index")
    df_data = pd.concat([df_data,df_temp])
    return(df_data)
