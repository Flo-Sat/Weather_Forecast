from datetime import datetime, timedelta
from dotenv import dotenv_values
import Requests_functions
import pandas as pd
import requests

import_start = "10/10/2025"
import_end =  "10/11/2025"

def week_ranges(start, end):
    """Yield (chunk_start, chunk_end) tuples covering [start, end] in 7-day chunks."""
    current = start
    while current <= end:
        chunk_end = min(current + timedelta(days=7), end)
        yield current, chunk_end
        chunk_end = min(current + timedelta(days=6), end)
        current = chunk_end + timedelta(days=1)

if __name__ == "__main__":
    config = dotenv_values(".env") 
    parameter_ids = config["PARAMETERS"].split(", ")
    dfs = []
    for chunk_start, chunk_end in week_ranges(datetime.strptime(import_start,'%d/%m/%Y'),datetime.strptime(import_end,'%d/%m/%Y')):
        responses = [
            Requests_functions.process_station(
                requests.get(Requests_functions.construct_url(
                    config["API_KEY_STATION_KOLDING"],
                    chunk_start,
                    chunk_end,
                    parameters
                    ))) for parameters in parameter_ids]
        dfs.append(pd.concat(responses, axis=1))
    df_final = pd.concat(dfs)
    df_final.sort_index().to_pickle("dfs.pickle")