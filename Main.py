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
import json

buttonA = Pin(15,Pin.IN,Pin.PULL_UP)
buttonB = Pin(17,Pin.IN,Pin.PULL_UP)

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
    user_city = str(input("Please enter your closest UK city: "))
    user_city =  user_city.lower().strip()
    return user_city


def get_Weather(city_name, api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},GB&appid={api_key}&units=metric"
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
        OLED.fill(0x0000)
        OLED.text("Today's Weather", 5, 5, OLED.white)
        OLED.text(f"{main["temp"]} C", 64, 28, OLED.white)
        OLED.text(f"{weather[0]["description"]}", 5, 51, OLED.white)
        OLED.blit(framebuffer_to_show,16,16)
        OLED.show()  
def status():
    OLED.fill(0x0000)
    OLED.text("Update status:", 5, 5, OLED.white)
    OLED.text("1.Yay, sunshine!!", 5, 20, OLED.white)
    OLED.text("2.Boring clouds...", 5, 35, OLED.white)
    OLED.text("3.Rain :(", 5, 50, OLED.white)
    OLED.show()
    counter = 0
    while True:
        if buttonB.value() == 0:
            counter += 1
            print("Counter: ", counter)
            if counter > 2:
                counter = 0
        if counter == 0:
            OLED.hline(5, 30, 118, OLED.white)
            OLED.hline(5, 45, 118, OLED.balck)
            OLED.hline(5, 60, 118, OLED.balck)
            OLED.show()
            status = {"status": "Yay, sunshine!!"}
            json_status = json.dumps(status)
        elif counter == 1:
            OLED.hline(5, 45, 118, OLED.white)
            OLED.hline(5, 30, 118, OLED.balck)
            OLED.hline(5, 60, 118, OLED.balck)
            OLED.show()
            status = {"status": "Boring clouds..."}
            json_status = json.dumps(status)
        else:
            OLED.hline(5, 60, 118, OLED.white)
            OLED.hline(5, 30, 118, OLED.balck)
            OLED.hline(5, 45, 118, OLED.balck)
            OLED.show()
            status = {"status": "Rain :("}
            json_status = json.dumps(status)
        if buttonA.value() == 0:
            break
def loading_screen():
    OLED.fill(0x0000)
    OLED.text("Loading...", 5, 28, OLED.white)
    OLED.show()


    
loading_screen()
connect()
city_name = get_location()
buttonState = 0
prevState = 0
latchOn = True
display_weather(get_Weather(city_name, credentials.weather_api))
while True:
    buttonState = buttonA.value()
    if buttonState != prevState:
        if buttonState == 1:
            if latchOn == False:
                latchOn = True
            elif latchOn == True:
                latchOn = False
        if latchOn == True:
            status()
        else:
            display_weather(get_Weather(city_name, credentials.weather_api))
    prevState = buttonState
    sleep(0.1)


