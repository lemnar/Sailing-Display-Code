import requests
import time
class params:
    url = "https://api.open-meteo.com/v1/forecast?latitude=40.1672&longitude=-105.1019&hourly=temperature_2m,precipitation,cloud_cover,wind_speed_10m,wind_gusts_10m&temperature_unit=fahrenheit&wind_speed_unit=kn&timezone=America%2FDenver&forecast_days=3"
    mintime = 0
    maxtime = 0
    mintemp = 0
    maxtemp = 0
    minwind = 0
    maxwind = 0
    mingust = 0
    maxgust = 0
    mincloud = 0
    maxcloud = 0


class weatherObj:
    def __init__(self, time = None, temp = None, precip = None, wind = None, cloud = None, gust = None):
        self.time = time
        self.hour = 0
        self.year = 0
        self.month = 0
        self.day = 0
        self.minute = 0
        self.makedt()
        self.temp = temp
        self.precip = precip
        self.wind = wind
        self.cloud = cloud
        self.gust = gust
    def makedt(self):
        date, time = self.time.split("T")
        self.year, self.month, self.day = date.split("-")
        self.hour, self.minute = time.split(":")
        self.hour = int(self.hour)
        self.year = int(self.year)
        self.month = int(self.month)
        self.day = int(self.day)
        self.minute = int(self.minute)
class DATA: 
    def __init__(self, url):
        for i in range(5):
            
            try:
                s = requests.get(url)
                print("response: ", s.status_code)
                break
            except Exception as e:
                print("Attempt ", i+1, "FAILED for reason", e)
                time.sleep(1)
        
        if s.status_code != 200:
            print("Something has failed when connecting to API... ask Nikky for help.")
            return
        data = s.json()
        hourly = data["hourly"]
        self.times = hourly["time"]
        self.precips = hourly["precipitation"]
        self.temps = hourly["temperature_2m"]
        self.winds = hourly["wind_speed_10m"]
        self.clouds = hourly["cloud_cover"]
        self.gusts = hourly["wind_gusts_10m"]
        self.weatherlist = []
        self.createObjects()
    def createObjects(self):
        for i in range(len(self.times)):
            self.weatherlist.append(weatherObj(time=self.times[i], temp=self.temps[i], precip=self.precips[i], wind=self.winds[i], cloud=self.clouds[i],gust=self.gusts[i]))
    def getObjAtIndex(self, index):
        return self.weatherlist[index]
    def getDataWithinRange(self, list_, c, low, high):
        returnlist = []
        for i in list_:
                if c == "time":
                    if i.hour >=low and i.hour <=high:
                        returnlist.append(i)
                elif c ==  "precip":
                    if i.precip >=low and i.precip <=high:
                        returnlist.append(i)
                elif c ==  "temp":
                    if i.temp >=low and i.temp <=high:
                        returnlist.append(i)
                elif c ==  "wind":
                    if i.wind >=low and i.wind <=high:
                        returnlist.append(i)
                elif c ==  "cloud":
                    if i.cloud >=low and i.cloud <=high:
                        returnlist.append(i)
                elif c ==  "gust":
                    if i.gust >=low and i.gust <=high:
                        returnlist.append(i)
                else:
                    return
        return returnlist
    def returnSailingTimes(self, params):
        ls = self.getDataWithinRange(self.weatherlist, "time", params.mintime, params.maxtime)
        ls = self.getDataWithinRange(ls, "temp", params.mintemp, params.maxtemp)
        ls = self.getDataWithinRange(ls, "wind", params.minwind, params.maxwind)
        return ls
        

def do():
    p = params()
    p.mintemp = 62.5
    p.maxtemp = 100
    p.mintime = 8
    p.maxtime = 22
    p.minwind = 5
    p.maxwind = 20
    d = DATA(p.url)
    d.weatherlist = d.weatherlist[:20]
    print()
    for i in d.returnSailingTimes(p):
        print(i.time)   
        print(str(i.hour) + ":00 --> \n     temp:", i.temp, "F\n     wind speed:", i.wind, "kn")
        print("     gust speed:", i.gust, "kn\n     cloud cover:", i.cloud, "%")
        print("     precipitation:", i.precip, "in")
    return d.returnSailingTimes(p)