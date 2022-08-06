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
bme.sea_level_pressure = 1029

# Initial values
zeroed_level_pressure = 0
temp_ground = 0
press_ground = 0

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
    badger.line(98, 40, 98, 109)  # vertical center line 
    badger.line(215, 40, 215, 109)  # vertical floor line  
    badger.pen(0)
    # for debugging use, print values to console
    print("Sensor values")
    print(read_sensor_temp()+" C")
    print(read_sensor_pressure()+" hPa")
    print(read_sensor_altitude()+" m")
    print(calculate_floor())
    print("-------------")
    print("stored values")
    print(str(temp_ground)+" C")
    print(str(press_ground)+" hPa")
    # draw values to the eINK display
    badger.text("Groundlevel: ", 8, 29, 0.41)
    badger.text(str(temp_ground)+" C", 90, 29, 0.41)
    badger.text(str(press_ground)+" hPa", 150, 29, 0.41)
    # draw altitude in black - values in white
    badger.pen(0)
    badger.rectangle(0, 39, 98, 71)
    badger.pen(15)
    badger.text("Altitude", 12, 50, TEXT_SIZE)
    badger.text(read_sensor_altitude(), 10 , 79, 0.8)
    badger.text("meter", 20, 100, TEXT_SIZE)
    badger.pen(0)
    #draw temperature-pressure (calc) in white
    badger.text("Temperature", 110, 50, TEXT_SIZE)
    badger.text(read_sensor_temp()+" C", 110, 65, TEXT_SIZE)
    badger.text("Pressure", 110, 85, TEXT_SIZE)
    badger.text(read_sensor_pressure()+" hPa", 110, 100, TEXT_SIZE)
    # draw floor in black - values in white
    badger.pen(0)
    badger.rectangle(215, 39, 296, 71)
    badger.pen(15)
    badger.text("Floor", 237, 50, TEXT_SIZE)
    badger.text(calculate_floor(), 238, 85, 1.2)
    badger.pen(0)
    # draw menu options values in black    
    badger.text("Zero", 22, 120, TEXT_SIZE)
    badger.text("Calc", 138, 120, TEXT_SIZE)
    badger.text("Test", 240, 120, TEXT_SIZE)
    badger.thickness(1)
    badger.update()
    badger.pen(15)
    badger.clear()
    # turn of activity LED to indicate function done
    badger.led(0)

# ------------------------------
#        Program setup
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
        temp_ground = read_sensor_temp()
        read_sensor_pressure()
        press_ground = read_sensor_pressure()
        draw_elevation()

    if badger.pressed(badger2040.BUTTON_B): # calculate floor based on pressure difference
        read_sensor_temp()
        draw_elevation()

    if badger.pressed(badger2040.BUTTON_C): # set example height based on The Hague
        bme.sea_level_pressure = 1031
        draw_elevation()

    if badger.pressed(badger2040.BUTTON_UP):
        badger_os.warning(display, "je hebt op pijl omhoog gedrukt. Dit scherm gaat na 4 secs weg")
        time.sleep(4)
        draw_elevation()

    if badger.pressed(badger2040.BUTTON_DOWN):
        badger_os.warning(display, "je hebt op pijl omlaag gedrukt. Dit scherm gaat na 4 secs weg")
        time.sleep(4)
        draw_elevation()


#    display.update()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
#    display.halt()
