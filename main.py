from pyowm import OWM
import csv
from datetime import datetime

from os import environ, stat, path, access, R_OK, mkdir

API_key = environ.get('API_key')

if API_key is None:
    from creds import API_key

fields = ["time", "windspeed", "humidity", "temperature", "status"]

now = datetime.now()


cities = ["Praha", "Plzen", "Ceske Budejovice", "Karlovy Vary", "Usti nad Labem", "Liberec", "Hradec Kralove", "Pardubice", "Jihlava", "Brno", "Olomouc", "Zlin", "Ostrava"]

for city in cities:
    foldername = "data/"+city.lower().replace(" ", "_")+"/"
    filename = foldername + now.strftime("%Y.%m.%d")+".csv"
    if not path.isdir(foldername):
        mkdir(foldername)
    if not path.isfile(filename) and not access(filename, R_OK):
        pf = open(filename, "w")
        
    if stat(filename).st_size == 0:
            WriteData = open(filename, "a")
            WriteData.write("time, windspeed, humidity, temperature, pressure, rain, snow, clouds, status \n")
            WriteData.close()


def getWeatherInfo(city: str):
    owm = OWM(API_key)
    obs = owm.weather_at_place(city+',CZ')
    w = obs.get_weather()

    # Weather details
    wind = w.get_wind()
    humidity = w.get_humidity()
    temp = w.get_temperature('celsius')
    status = w.get_status().lower()
    pressure = w.get_pressure()
    rain = w.get_rain()
    snow = w.get_snow()
    clouds = w.get_clouds()

    def checkFor(objct):
        if len(objct) == 0:
            return 0
        else:
            return objct

    return [now.strftime("%H:%M"), wind['speed'], humidity, temp['temp'], pressure['press'], checkFor(rain[list(rain)[0]]), checkFor(snow[list(snow)[0]]), clouds, status]

def createString(csvArr):
    fnlStr = ""
    for i,el in enumerate(csvArr):
        fnlStr += str(el)
        if i != len(csvArr) - 1:
            fnlStr += ","
        else:
            fnlStr += "\n"
    return fnlStr

for city in cities:
    filename = "data/"+city.lower().replace(" ", "_")+"/"+now.strftime("%Y.%m.%d")+".csv"
    csvArrIn = getWeatherInfo(city)
    WriteData = open(filename, "a")
    WriteData.write(createString(csvArrIn))
    WriteData.close()

