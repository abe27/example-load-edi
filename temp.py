#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
import requests
import sys
import os
import DHT22 as DHT22
from datetime import datetime
from random import *
from dotenv import load_dotenv
## Load .env file
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

def notification(message=""):
    url = "https://notify-api.line.me/api/notify"
    payload = f'message={message}'
    headers = {
        'Authorization': f'Bearer {LINE_NOTIFY_TOKEN}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


if __name__ == '__main__':
    try:
        serveName = "TEM001"
        onPin = 17
        alertOn = 26
        print(f"serve: {serveName} pin: {onPin} alert: {alertOn}")
        units = 'c'
        sensor = DHT22.DHT22(onPin, units)
        humidity, temperature = sensor.get_value()
        if humidity is not None and temperature is not None:
            print(
                'Temp={0:0.1f}*C  Humidity={1:0.1f}%'.format(temperature, humidity))

        if round(temperature, 2) >= alertOn:
            # notification
            d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            msg = f"""\n{serveName}\nTemperature: {round(temperature, 2)}\nHumidity: {round(humidity, 2)}\nAt: {d}"""
            notification(message=msg)

    except Exception as ex:
        print(ex)
        pass

    sys.exit(0)
