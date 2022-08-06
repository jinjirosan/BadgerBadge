from machine import Pin, I2C
from time import sleep
from bme680 import *
import pimoroni_i2c

i2c = I2C(0, scl=Pin(5), sda=Pin(4))

bme = BME680_I2C(i2c=i2c)

# change this to match the location's pressure (hPa) at sea level
bme.sea_level_pressure = 1023.7

while True:
  try:
    temp = str(round(bme.temperature, 2)) + ' C'
    #temp = (bme.temperature) * (9/5) + 32
    #temp = str(round(temp, 2)) + 'F'
    
    hum = str(round(bme.humidity, 2)) + ' %'
    
    pres = str(round(bme.pressure, 2)) + ' hPa'
    
    gas = str(round(bme.gas/1000, 2)) + ' KOhms'
    
    alti = str(round(bme.altitude, 2)) + ' meter' 

    print('Temperature:', temp)
    print('Humidity:', hum)
    print('Pressure:', pres)
    print('Gas:', gas)
    print('Altitude:', alti)
#    print("Altitude = %0.2f meters" % bme.altitude)
    print('-------')
  except OSError as e:
    print('Failed to read sensor.')
 
  sleep(5)