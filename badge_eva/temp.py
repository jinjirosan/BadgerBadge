import time
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
import pimoroni_i2c
import badger2040
import machine
import math

badger = badger2040.Badger2040()
badger.update_speed(badger2040.UPDATE_FAST)

PINS_PICO_EXPLORER = {"sda": 4, "scl": 5}

TITLE_SIZE = 0.68
TEXT_SIZE = 0.5

button_a = machine.Pin(badger2040.BUTTON_A, machine.Pin.IN, machine.Pin.PULL_DOWN)
i2c = pimoroni_i2c.PimoroniI2C(**PINS_PICO_EXPLORER)
bme = BreakoutBME68X(i2c,0x77)

#temperature offset to compensate for temperature of the sensor itself
temp_offset = -1.5

#pressure (hPa) at sea level The Hague
sea_level_pressure = 1013.25

# converts the temperature into a barometer-type description
def describe_temperature(correctedtemp):
    if temp < 10:
        description = "freeze"
    elif 10 <= temp < 20:
        description = "cold"
    elif 20 <= temp < 25:
        description = "nice"
    elif 25 <= temp < 30:
        description = "warm"
    elif temp >= 30:
        description = "hot"
    else:
        description = ""
    return description

# converts pressure into barometer-type description
def describe_pressure(pressure):
    if pressure < 970:
        description = "storm"
    elif 970 <= pressure < 990:
        description = "rain"
    elif 990 <= pressure < 1010:
        description = "change"
    elif 1010 <= pressure < 1030:
        description = "nice"
    elif pressure >= 1030:
        description = "dry"
    else:
        description = ""
    return description

# converts humidity into good/bad description
def describe_humidity(humidity):
    if 40 < humidity < 60:
        description = "good"
    else:
        description = "bad"
    return description

while True:
    temperature, pressure, humidity, gas, status, _, _ = bme.read()
    heater = "Stable" if status & STATUS_HEATER_STABLE else "Unstable"
    # pressure default is in pascals. Convert to hPa
    pressurehpa = pressure / 100
    # Output to console, for debugging use
    print("{:0.2f}c, {:0.2f}Pa, {:0.2f}%, {:0.2f} Ohms, m, Heater: {}".format(
        temperature, pressurehpa, humidity, gas, heater))
    temp = temperature + temp_offset
    correctedtemp = str(round(temp,1))
    press = str(round(pressurehpa,1))
    humid = str(round(humidity,1))
    # Correct gas sensor output to humidity
    correctedgas = math.log(gas) + 0.04 * humidity
    print("Corrected environment values")
    print(correctedtemp, press, humid, correctedgas)
    
    # Set display parameters
    badger.pen(15)
    badger.font("sans")
    badger.thickness(2)
    # black box on top
    badger.pen(0)
    badger.rectangle(0, 0, 296, 22)
    badger.pen(15)
    badger.text("Hoe is het weer nu ?", 38, 10, TITLE_SIZE)
    badger.pen(0)
    badger.line(0, 39, 296, 39)
    badger.line(0, 101, 296, 101)
    badger.pen(0)
    badger.text("Temperature   "+correctedtemp+" C", 8, 50, TEXT_SIZE)
    badger.text(describe_temperature(correctedtemp), 245, 50, TEXT_SIZE)
    badger.text("Pressure       "+press+" hPa", 8, 70, TEXT_SIZE)
    badger.text(describe_pressure(pressurehpa), 245, 70, TEXT_SIZE)
    badger.text("Humidity       "+humid+" %", 8, 90, TEXT_SIZE)
    badger.text(describe_humidity(humidity), 245, 90, TEXT_SIZE)
    badger.thickness(1)
    badger.text("Heater "+heater+" ", 205, 120, 0.4)
    badger.update()
    time.sleep(30.0)
    badger.pen(15)
    badger.clear()