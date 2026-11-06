import schedule
import time
from dotenv import dotenv_values
import Requests_functions
import pandas as pd
config = dotenv_values(".env") 

def job():
    forecast = Requests_functions.query_forecast(config)
    station = Requests_functions.query_station(config)
    return forecast,station

def save_data(forecast,station):
    forecast.index = pd.to_datetime(forecast.index, utc=True)

    station.index = pd.to_datetime(station.index, utc=True)
    station = station.rename(columns={"temp_dry": "temp"})

    forecast = forecast[forecast.index.minute == 0]
    station = station[station.index.minute == 0].sort_index().tail(1)

    print(forecast)
    print(station)
# schedule.every(10).minutes.do(job)
# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().day.at("12:42", "Europe/Amsterdam").do(job)
# schedule.every().minute.at(":17").do(job)

if __name__ == "__main__":
    print("here")
    save_data(*job())