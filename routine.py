import schedule
import time
from datetime import datetime, timedelta, timezone
from dotenv import dotenv_values
import Requests_functions
import requests
import pandas as pd
config = dotenv_values(".env") 

def job(config):
    parameter_ids = config["PARAMETERS"].split(", ")
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=7)
    responses = [
        Requests_functions.process_station(
            requests.get(Requests_functions.construct_url(
                config["API_KEY_STATION_KOLDING"],
                start,
                end,
                parameters
                ))) for parameters in parameter_ids]
    return (pd.concat(responses, axis=1))

def save_data(station):

    station.to_pickle(f"df_weekly_{datetime.now().date()}.pickle")

def weekly_task():
    save_data(job(config))

if __name__ == "__main__":
    schedule.every().wednesday.at("12:00").do(weekly_task)
    while True:
        schedule.run_pending()
        time.sleep(60)