import io
import os
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

from dotenv import load_dotenv

load_dotenv()

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

class Client(object):
    DEFAULT_BASE_URL = "https://airquality.googleapis.com"

    def __init__(self, key):
        self.session = requests.Session()
        self.key = key

    def request_post(self, url, params):
        request_url = self.compose_url(url)
        request_header = self.compose_header()
        request_body = params

        response = self.session.post(
            request_url,
            headers=request_header,
            json=request_body,
        )

        return self.get_body(response)

    def compose_url(self, path):
        return self.DEFAULT_BASE_URL + path + "?" + "key=" + self.key

    @staticmethod
    def get_body(response):
        body = response.json()

        if "error" in body:
            return body["error"]

        return body

    @staticmethod
    def compose_header():
        return {
            "Content-Type": "application/json",
        }

GOOGLE_MAPS_API_KEY = os.environ["GOOGLE_MAPS_API_KEY"]  

client = Client(key=GOOGLE_MAPS_API_KEY)

def historical_conditions(
                        client,
                        location,
                        specific_time=None,
                        lag_time=None,
                        specific_period=None,
                        include_local_AQI=False,
                        include_health_suggestion=False,
                        include_all_pollutants=True,
                        include_additional_pollutant_info=False,
                        include_dominant_pollutant_conc=True,
                        language=None,

                    
                    
    ):
    
    params = {}
    
    if isinstance(location, dict):
        params["location"] = location
    else:
        raise ValueError(
            "Location argument must be a dictionary containing latitude and longitude"
        )

    if isinstance(specific_period, dict) and not specific_time and not lag_time:
        assert "startTime" in specific_period
        assert "endTime" in specific_period

        params["period"] = specific_period

    elif specific_time and not lag_time and not isinstance(specific_period, dict):
        # note that time must be in the "Zulu" format
        # e.g. datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%dT%H:%M:%SZ")
        params["dateTime"] = specific_time

    # lag periods in hours
    elif lag_time and not specific_time and not isinstance(specific_period, dict):
        params["hours"] = lag_time

    else:
        raise ValueError(
            "Must provide specific_time, specific_period or lag_time arguments"
        )

    extra_computations = []

    if include_local_AQI:
        extra_computations.append("LOCAL_AQI")


    if include_health_suggestion:
        extra_computations.append("HEALTH_RECOMMENDATIONS")

    if include_additional_pollutant_info:
        extra_computations.append("POLLUTANT_ADDITIONAL_INFO")

    if include_all_pollutants:
        extra_computations.append("POLLUTANT_CONCENTRATION")

    if include_dominant_pollutant_conc:
        extra_computations.append("DOMINANT_POLLUTANT_CONCENTRATION")

    if language:
        params["language"] = language


    params["extraComputations"] = extra_computations
    # page size default set to 100 here
    params["pageSize"] = 100
    # page token will get filled in if needed by the request_post method
    params["pageToken"] = ""

    return client.request_post("/v1/history:lookup", params)

@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """

    # List of cities
    cities = [
              "Zurich",
               "Geneva", 
            "Bern", "Basel", "Lucerne", "Lausanne", "St. Gallen", "Locarno",
           "Davos", "Interlaken", "Zermatt", "Andermatt", "Neuchatel", "Schaffhausen"
            ]


    # Create an empty DataFrame to store the data
    final_df = pd.DataFrame()

    dfs = []

    # Set initial_end_date to today and initial_start_date to 4 days before today
    initial_end_date = datetime.now() - timedelta(hours=1)
    initial_start_date = initial_end_date - timedelta(days=4)

    # Specify the number of periods to generate
    num_periods = 2

    loc = Nominatim(user_agent="Geopy Library")
    # Generate periods using a loop
    for i in range(num_periods):
        start_date = initial_start_date - timedelta(days=i * 4)
        end_date = start_date + timedelta(days=3, hours=23, minutes=59, seconds=59)
        periods = {"start": start_date, "end": end_date}

        for city in cities:
            loc = Nominatim(user_agent="weather_app")
            getLoc = loc.geocode(city)

            if getLoc:
                location_info = {"longitude": getLoc.longitude, "latitude": getLoc.latitude}

                start_time_str = start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                end_time_str = end_date.strftime("%Y-%m-%dT%H:%M:%SZ")

                print(city)
                print(start_time_str)
                print(end_time_str)

                specific_period = {
                    "startTime": start_time_str,
                    "endTime": end_time_str
                }

                history_conditions_data = historical_conditions(
                    client,
                    location_info,
                    specific_period=specific_period
                )

            df = pd.json_normalize(history_conditions_data['hoursInfo'])
            df = df.explode('indexes').reset_index(drop=True)
            df = df.explode('pollutants').reset_index(drop=True)
            df = pd.concat([df.drop(['indexes'], axis=1), df['indexes'].apply(pd.Series)[['aqi', 'category', 'dominantPollutant']]], axis=1)
            df = pd.concat([df.drop(['pollutants'], axis=1), df['pollutants'].apply(pd.Series)[['displayName', 'fullName', 'concentration']]], axis=1)
            # df = df.dropna()
            df['concentration_value'] = df['concentration'].apply(lambda x: x['value'] if isinstance(x, dict) and 'value' in x else np.nan)
            df = df.drop(['concentration'], axis=1)

            df['city'] = city
            df['latitude'] = getLoc.latitude
            df['longitude'] = getLoc.longitude

            dfs.append(df)
    


    # Concatenate all DataFrames in the list into the final DataFrame
    final_df = pd.concat(dfs, ignore_index=True)

    print(f'Dataframe length before transformation: {len(final_df)} rows')

    print(f'NaN rows: {final_df.isna().any(axis=1).sum()} rows')

    print(f'Duplicated rows: {final_df.duplicated().sum()} rows')


    # Display the final DataFrame
    return final_df

# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'
