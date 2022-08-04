import badger2040
import time

from breakout_bme68x import BreakoutBME68X
import pimoroni_i2c

display = badger2040.Badger2040()

WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

PINS_PICO_EXPLORER = {"sda": 4, "scl": 5}

TITLE_SIZE = 0.8
TEXT_SIZE = 0.5

button_a = machine.Pin(badger2040.BUTTON_A, machine.Pin.IN, machine.Pin.PULL_DOWN)
i2c = pimoroni_i2c.PimoroniI2C(**PINS_PICO_EXPLORER)
bme = BreakoutBME68X(i2c,0x77)

n = 0

timer = 0

firstcolumn = 35
secondcolumn = 150
bigtext = 0.7
smalltext = 0.6
arrowtext = 0.8

# the gas readings vary a lot between BME680 and BME688 so you might need to adjust these values
gas_min = 50
gas_max = 113
# air quality is considered good if over this number
gas_ok = 80

hum_min = 0
hum_max = 100
hum_low = 40
hum_high = 60

barwidth_min = 0
barwidth_max = WIDTH - 30

def clear():
    display.invert(False)
    
    # white background
    display.pen(15)
    display.clear()
    
    # grey box on right
    display.pen(8)
    display.rectangle(secondcolumn - 5, 0, 153, 128)
    
    # black box on left
    display.pen(0)
    display.rectangle(0, 0, 30, 128)
    
    # text down the side
    display.pen(15)
    display.font("sans")
    display.thickness(2)
    display.text("environment", 15, 119, 0.6, 270)
    
def drawandupdate():
    global timer
           
    clear()
    
    display.pen(0)
    display.font("sans")
    display.thickness(2)
    display.text(f"Temp.", firstcolumn, 15, bigtext)       
    display.text(f"Pressure", firstcolumn, 35, bigtext)          
    display.text(f"Humidity", firstcolumn, 55, bigtext)
    display.text(f"Gas", firstcolumn, 95, bigtext)
    
    display.pen(15)
    display.font("sans")
    display.thickness(2)       
    display.text(f"{temperature_average} C", secondcolumn, 15, bigtext)
    display.text(f"{pressure_average} hPa", secondcolumn, 35, bigtext)
    display.text(f"{humidity_average:.0f}%", secondcolumn, 55, bigtext)
    display.text(f"{gas_average:.0f} kOhm", secondcolumn, 95, bigtext)

    display.font("sans")
    display.thickness(3)
    
    if temperature_average < last_temperature:
        display.text(f"v", WIDTH - 20, 15, arrowtext)
    if temperature_average > last_temperature:
        display.text(f"v", WIDTH - 10, 15, arrowtext, 180)

    if pressure_average < last_pressure:
        display.text(f"v", WIDTH - 20, 35, arrowtext)
    if pressure_average > last_pressure:
        display.text(f"v", WIDTH - 10, 35, arrowtext, 180)

    if humidity_average < last_humidity:
        display.text(f"v", WIDTH - 20, 55, arrowtext)
    if humidity_average > last_humidity:
        display.text(f"v", WIDTH - 10, 55, arrowtext, 180)
        
    if gas_average < last_gas:
        display.text(f"v", WIDTH - 20, 95, arrowtext)
    if gas_average > last_gas:
        display.text(f"v", WIDTH - 10, 95, arrowtext, 180)
    
    display.pen(8)
    display.thickness(1)
    display.rectangle(30, 65, round((humidity - hum_min) / (hum_max - hum_min) * barwidth_max), 18)
    display.rectangle(30, 105, round((gas_resistance/1000 - gas_min) / (gas_max - gas_min) * barwidth_max), 18)
    
    display.pen(0)
    display.thickness(2)
    
    # invert the display if the humidity or gas conditions are bad
    if humidity_average <= hum_low:
        display.text(f"low", secondcolumn, 75, smalltext)
        display.invert(True)

    elif humidity_average >= hum_high:
        display.text(f"high", secondcolumn, 75, smalltext)
        display.invert(True)
    
    if gas_average < gas_ok:
        display.text(f"poor", secondcolumn, 115, smalltext)
        display.invert(True)
      
    display.update()
    timer = 0
    
# Set up the arrays and populate them with a read
temperature, pressure, humidity, gas_resistance, status, gas_index, meas_index = bme.read()

temperature_array = [temperature] * 12
humidity_array = [humidity] * 12
pressure_array = [pressure] * 12
gas_array = [gas_resistance] * 12

last_temperature = round(temperature,1)
last_pressure = round(pressure/100)
last_humidity = round(humidity)
last_gas = round(gas_resistance/1000)

clear()
display.pen(0)
display.font("sans")
display.thickness(2)
display.text(f"Waiting", firstcolumn, 15, bigtext)       
display.text(f"for", firstcolumn, 35, bigtext)          
display.text(f"readings", firstcolumn, 55, bigtext)
display.thickness(2) 
display.text(f"this will", secondcolumn, 90, bigtext)
display.text(f"take a min", secondcolumn, 110, bigtext)
display.update()


while True:    
    if timer % 5 == 0:
   
        #read the sensor
        temperature, pressure, humidity, gas_resistance, status, gas_index, meas_index = bme.read()
    
        # add the reading to the array
        if n >= len(temperature_array):
            n= 0
        temperature_array[n] = temperature
        pressure_array[n] = pressure
        humidity_array[n] = humidity
        gas_array[n] = gas_resistance
        n += 1
            
        # calculate a moving average from the contents of the array
        temperature_average = round(sum(temperature_array)/len(temperature_array))
        pressure_average = round((sum(pressure_array)/len(pressure_array)/100))
        humidity_average = round(sum(humidity_array)/len(humidity_array))
        gas_average = round((sum(gas_array)/len(gas_array)/1000))
        print(f"Temp: {temperature_average} c, Pressure: {pressure_average} hPa, Humidity: {humidity_average} %, Gas: {gas_average} kOhm")
       
        if (temperature_average != last_temperature or pressure_average != last_pressure or humidity_average != last_humidity or gas_average != last_gas) and timer >= 60:
            drawandupdate()
              
            # record the last readings
            last_temperature = temperature_average
            last_pressure = pressure_average
            last_humidity = humidity_average
            last_gas = gas_average
            
        #refresh every 5 mins even if nothing has changed
        if timer >= 300:
            drawandupdate()
      
    timer += 1
    time.sleep(1)
    