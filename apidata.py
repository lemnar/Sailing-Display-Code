import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import datetime


class dataparams:
    url = ""
    lat = 0.00
    long = 0.00
    hourly = []
    t_unit = ""
    w_unit = ""
    tz = ""
    fc_days = 0
    mintime = 0
    maxtime = 0
    mintemp = 0
    maxtemp = 0
    minwind = 0
    maxwind = 0

class Data:
    def __init__(self):
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.SESSION = openmeteo_requests.Client(session=retry_session)
        self.response_index = 0
    def inputData(self, data):
        self.url = data.url
        self.params = {
            "latitude": data.lat,
            "longitude": data.long,
            "hourly": data.hourly,
            "temperature_unit": data.t_unit,
            "wind_speed_unit": data.w_unit,
            "timezone": data.tz,
            "forecast_days": data.fc_days
        }
        self.mintime = data.mintime
        self.maxtime = data.maxtime
        self.mintemp = data.mintemp
        self.maxtemp = data.maxtemp
        self.minwind = data.minwind
        self.maxwind = data.maxwind
    def collect(self):
        self.responses = self.SESSION .weather_api(self.url, params=self.params)
        self.response = self.responses[0]
    def setResponse(self, i):
        self.response = self.responses[i]
    def determineEligibleTimes(self):
        hourly = self.response.Hourly()
        hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
        hourly_wind_speed_2m = hourly.Variables(2).ValuesAsNumpy()
        dates = pd.date_range(
            start = pd.to_datetime(hourly.Time(), unit = "s"),
            end = pd.to_datetime(hourly.TimeEnd(), unit = "s"),
            freq = pd.Timedelta(seconds = hourly.Interval()),
            inclusive = "left")
        hourly_data = {"date": dates}
        hourly_data["temp"] = hourly_temperature_2m
        hourly_data["precip"] = hourly_precipitation
        hourly_data["wind"] = hourly_wind_speed_2m
        hourly_dataframe = pd.DataFrame(data = hourly_data)
        self.hourly_dataframe = hourly_dataframe
        timearray = pd.to_datetime(self.hourly_dataframe["date"])
        hourly_dataframe["dateobjs"] = timearray
        self.eligible_times = hourly_dataframe.loc[hourly_dataframe["dateobjs"].dt.hour > self.mintime].loc[hourly_dataframe["dateobjs"].dt.hour < self.maxtime]

    def SailableTimesArray(self):
        self.determineEligibleTimes()
        temp_condition_array = self.eligible_times.loc[self.eligible_times["temp"] > self.mintemp].loc[self.eligible_times["temp"]<self.maxtemp]
        wind_condition_array = temp_condition_array.loc[temp_condition_array["wind"] > self.minwind].loc[temp_condition_array["wind"] < self.maxwind]
        self.sailable_times = wind_condition_array
        return self.sailable_times
    def TodaysSailableTimes(self):
        today  = datetime.datetime.today().day
        self.today_sailable_times = self.sailable_times.loc[self.sailable_times["dateobjs"].dt.day == today]
        return self.today_sailable_times
    def __call__(self, today = True):
        self.collect()
        self.SailableTimesArray()
        self.TodaysSailableTimes()
        if today:
            if not self.today_sailable_times.empty:
                print("Today is a good day to go sailing!\nTimes to go:\n")
                for index, i in self.today_sailable_times.iterrows():
                    print(str(i["dateobjs"].hour) + " o'clock is a good time to go")
                    print("Temp: " + str(i["temp"])[:5] + " F")
                    print("Wind: " + str(i["wind"])[:4] + " kn")
            else:
                print("Unfortunately, it is not a good day to go sailing today :(")
                print("Nikky loves you though!")
        else:
            if not self.sailable_times.empty:
                print("There are good times to go sailing in the next few days!\nTimes to go:\n")
                for index, i in self.sailable_times.iterrows():
                    print(str(i["dateobjs"].month) + "/"  + str(i["dateobjs"].day) + " at " + str(i["dateobjs"].hour) + " o'clock is a good time to go")
                    print("Temp: " + str(i["temp"])[:5] + " F")
                    print("Wind: " + str(i["wind"])[:4] + " kn")
            else:
                print("Unfortunately, there are no good nearby sailing days :(")
                print("Nikky loves you though!")
    
params = dataparams()
params.url = "https://api.open-meteo.com/v1/forecast"
params.lat = 40.1672
params.long = -105.1019
params.hourly = ["temperature_2m", "precipitation", "wind_speed_10m"]
params.t_unit = "fahrenheit"
params.w_unit = "kn"
params.tz = "America/Denver"
params.fc_days = 3
params.mintemp = 60
params.maxtemp = 90
params.minwind = 7
params.maxwind = 17
params.mintime = 9
params.maxtime = 21

d = Data()
d.inputData(params)
d(True)

