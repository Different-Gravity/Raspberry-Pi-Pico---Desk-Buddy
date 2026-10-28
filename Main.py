import requests
import network
import socket
from time import sleep
import machine
import rp2
import sys
import credentials

ssid = credentials.ssid
password = credentials.password

def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)    
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip


def get_location():
    city = ["edinburgh", "dundee","stirling","glasgow", "inverness", "perth", "dunfermline", "aberdeen"]
    latitude = [55.953251, 	56.462002, 	56.119, 55.8652, 57.4791, 56.3952, 	56.0716, 57.1437]
    longitude = [-3.188267, -2.970700, -3.93682, -4.25763, -4.22398, -3.43139, -3.45887, -2.09814]
    location = []
    found = False
    while found == False:
        user_city = str(input("Please enter your closest Scottish city: "))
        user_city =  user_city.lower().strip()
        for i in range(len(city)):
            if city[i] == user_city:
                lat = latitude[i]
                location.append(lat)
                lon = longitude[i]
                location.append(lon)
                found = True
        print("Invalid option, please try again")
    return location


def get_Weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    response = requests.get(url)
    print(response)


connect()
location = get_location()
get_Weather(location[0], location[1], credentials.weather_api)