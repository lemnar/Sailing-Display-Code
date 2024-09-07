import requests
import datetime

apikey = "ae1851f608a03c453b053b24488e83e8"

class params: 
    mintemp = 0
    maxtemp = 0
    minwind = 0
    maxwind = 0
    mintime = 0
    maxtime = 0
    url = ""
    long = 0
    lat = 0
    def createurl(self):
        self.url = "https://api.openweathermap.org/data/2.5/forecast?lat={}&lon={}&exclude={}&appid={}&units=metric".format(self.lat, self.long, "minutely,daily,alerts",apikey)

class weatherObject:
    def __init__(self, temp=None,wind=None,clouds=None,time=None,data=None):
        if data!=None:
            self.temp = None
            self.wind = None
            self.clouds = None
            self.time = None

        if temp != None and wind != None and time != None and clouds != None: 
            self.temp = temp
            self.wind = wind
            self.time = time
            self.clouds = clouds
    def to_dt(self, dt):
        year = 1970
        month = 0
        day = 0
        minute = 0
        second = 0
        
class Data: 
    def __init__(self, params):
        self.url = params.url
        self.params = params
        self.objlist = []
        self.response = ""
    def __repr__(self):
        return "----- Data class -----\nResult amount: " + str(self.objlist.__sizeof__()) + "\nAPI call: " + self.url + "\n"
    def getdata(self):
        self.response = requests.get(self.url).json()
        data = self.response.list
        print(data.time)

    def makeWeatherObj(self, temp=None,wind=None,clouds=None,time=None,data=None):
        if data!=None:
            return weatherObject(data = data)

        if temp != None and wind != None and time != None and clouds != None: 
            return weatherObject(temp = temp, wind = wind, clouds = clouds, time = time)
    def addObjToList(self, obj):
        self.objlist.append(obj)

    # below are the data parsing techniques using the parameters and end cases
    # I might be able to use the onecall api if i trust them enough and think they won't charge my card
    # I could also put in a temp card so that they don't charge it when I make a call.
        
    
p = params()
p.long = -105.102
p.lat = 40.1672
p.createurl()
d = Data(p)
d.getdata()
print(d)