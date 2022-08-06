from machine import Pin, I2C
from time import sleep
from bme680 import *
import pimoroni_i2c
import badger2040
import badger_os
import math

# Default badges setup
badger = badger2040.Badger2040()
badger.update_speed(badger2040.UPDATE_FAST)

TITLE_SIZE = 0.68
TEXT_SIZE = 0.5

# BME680 sensor setup
i2c = I2C(0, scl=Pin(5), sda=Pin(4))
bme = BME680_I2C(i2c=i2c)

# Temperature offset to compensate for temperature of the sensor itself
temp_offset = -1.5

# Pressure (hPa) at sea level The Hague
bme.sea_level_pressure = 1023.7

# Pressure (hPa) at zeroed level (not sure I'll use this in this version)
zeroed_level_pressure = 1000

def read_sensor_temp():
    temperature = bme.temperature
    temp = temperature + temp_offset
    correctedtemp = str(round(temp,1))
    return correctedtemp

def read_sensor_pressure():
    pressure = bme.pressure
    press = str(round(pressure,1))
    return press

def read_sensor_altitude():
    altitude = bme.altitude
    alti= str(round(altitude,2))
    return alti

def calculate_floor():
    calcfloor = bme.altitude / 2.5
    floor= str(round(calcfloor))
    return floor

def draw_elevation():
    badger.led(128)
    # Set display parameters
    badger.pen(15)
    badger.font("sans")
    badger.thickness(2)
    # black box on top with title
    badger.pen(0)
    badger.rectangle(0, 0, 296, 22)
    badger.pen(15)
    badger.text("Hoe hoog zitten we?", 38, 10, TITLE_SIZE)
    # draw framework
    badger.pen(0)
    badger.line(0, 39, 296, 39) # top horizontal line
    badger.line(0, 110, 296, 110) # bottom horizontal line
    badger.line(215, 40, 215, 109)  # vertical floor line  
    badger.pen(0)
    # for debugging use, print values to console
    print(read_sensor_temp()+" C")
    print(read_sensor_pressure()+" hPa")
    print(read_sensor_altitude()+" m")
    print(calculate_floor())
    # draw values to the eINK display
    badger.text("Temperature   "+read_sensor_temp()+" C", 8, 50, TEXT_SIZE)
    badger.text("Pressure      "+read_sensor_pressure()+" hPa", 8, 70, TEXT_SIZE)
    badger.text("Altitude        "+read_sensor_altitude()+" m", 8, 90, TEXT_SIZE)
    badger.text("Floor", 237, 50, TEXT_SIZE)
    badger.text(calculate_floor(), 238, 85, 2)
    badger.text("Zero", 22, 120, TEXT_SIZE)
    badger.text("Calc", 138, 120, TEXT_SIZE)
    badger.text("The Hague", 215, 120, TEXT_SIZE)
    badger.thickness(1)
    badger.update()
    badger.pen(15)
    badger.clear()
    # turn of activity LED to indicate function done
    badger.led(0)

# ------------------------------
# Setup for elevation.py
# ------------------------------

# Create a new Badger and set it to update NORMAL
badger.led(128)
badger.update_speed(badger2040.UPDATE_NORMAL)

# ------------------------------
#       Main program
# ------------------------------
read_sensor_temp()
read_sensor_pressure()

draw_elevation()

while True:
    if badger.pressed(badger2040.BUTTON_A): # reset groundlevel to this pressurelevel
        bme.sea_level_pressure = bme.pressure
        read_sensor_temp()
        read_sensor_pressure()
        draw_elevation()

    if badger.pressed(badger2040.BUTTON_B): # calculate floor based on pressure difference
        read_sensor_temp()
        draw_elevation()

    if badger.pressed(badger2040.BUTTON_C): # set example height based on The Hague
        bme.sea_level_pressure = 1025
        draw_elevation()

    if badger.pressed(badger2040.BUTTON_UP):
        badger_os.warning(display, "je hebt op pijl omhoog gedrukt. Dit scherm gaat na 4 secs weg")
        time.sleep(4)
        draw_elevation()

    if badger.pressed(badger2040.BUTTON_DOWN):
        badger_os.warning(display, "je hebt op pijl omlaag gedrukt. Dit scherm gaat na 4 secs weg")
        time.sleep(4)
        draw_elevation()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    #badger.halt()