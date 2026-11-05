import requests
import network
import socket
from time import sleep
import rp2
import sys
import credentials
from PicoOLED13 import OLED_1inch3
import time
from machine import Pin, RTC
import framebuf
from weather_icons import icon01d, icon02d, icon03d, icon04d, icon09d, icon10d, icon11d, icon13d, icon50d

keyA = Pin(15,Pin.IN,Pin.PULL_UP)
keyB = Pin(17,Pin.IN,Pin.PULL_UP)

OLED = OLED_1inch3()
ssid = credentials.ssid
password = credentials.password

def connect():
    print('Connecting to wifi...')
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if wlan.isconnected():
        wlan.disconnect()
        sleep(1)

    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    print('Connection details: %s' % str(wlan.ifconfig()))


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
        if found ==False:
            print("Invalid option, please try again")
    return location


def get_Weather(lat, lon, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        return  weather_data
    else:
        print("Failed to retrieve data: ", response.status_code)
    response.close()
    
def display_weather(weather_info):
    icons = [icon01d, icon02d, icon03d, icon04d, icon09d, icon10d, icon11d, icon13d, icon50d]
    if weather_info:
        weather = weather_info["weather"]
        main = weather_info["main"]
        icon_code = weather[0]["icon"]
        for i in range(len(icons)):
            if ("icon" + icon_code) == icons[i].__name__:
                icon = icons[i]()
                framebuffer_to_show = framebuf.FrameBuffer(icon, 32, 32, framebuf.MONO_HLSB)
        OLED.text("Today's Weather", 5, 5, OLED.white)
        OLED.text(f"{main["temp"]} C", 64, 28, OLED.white)
        OLED.text(f"{weather[0]["description"]}", 5, 51, OLED.white)
        OLED.blit(framebuffer_to_show,16,16)
        OLED.show()  


connect()
location = get_location()
weather_info = get_Weather(location[0], location[1], credentials.weather_api)
display_weather(weather_info)

