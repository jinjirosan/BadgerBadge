# Badge Platform Eva - hardware platform v3.0
# (2022-2024) Voor m'n lieve guppie
#
# temp.py : v3.2-refactor 1.4

import time
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
import pimoroni_i2c
import badger2040
import badger_os
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
    elif 10 <= temp < 14:
        description = "cold"
    elif 14 <= temp < 20:
        description = "fine"
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

def calculate_dew_point(temperature_c, humidity):
    """Calculate the dew point in degrees Celsius."""
    a = 17.27
    b = 237.7
    alpha = ((a * temperature_c) / (b + temperature_c)) + math.log(humidity / 100.0)
    dew_point = (b * alpha) / (a - alpha)
    return round(dew_point, 1)

def calculate_feels_like(temperature_c, humidity):
    """Calculate the 'Feels Like' temperature in degrees Celsius for the range -10°C to +40°C."""
    if temperature_c < 27:
        # Simplified adjustment for temperatures below 27°C
        adjustment = (humidity - 40) / 5  # Simplified illustrative adjustment factor
        feels_like = temperature_c - adjustment
    else:
        # Placeholder for the comprehensive Heat Index formula for temperatures 27°C and above
        # Assuming high humidity conditions. Replace with actual Heat Index calculation as needed.
        feels_like = temperature_c  # This should be replaced with the actual Heat Index calculation
    return round(feels_like, 1)

def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    return celsius + 273.15

def encode_temperature_for_6bit(celsius_temperature):
    """Encode corrected Celsius temperature into a 6-bit value for the -10°C to +40°C range."""
    # Convert Celsius to Kelvin
    kelvin_temperature = celsius_to_kelvin(celsius_temperature)
    # Define the Kelvin range based on the Celsius range -10°C to +40°C
    min_kelvin = celsius_to_kelvin(-10)  # 263.15 K
    max_kelvin = celsius_to_kelvin(40)   # 313.15 K
    # Normalize and encode the Kelvin temperature to fit within the 6-bit range (0 to 63)
    encoded_temperature = int((kelvin_temperature - min_kelvin) / (max_kelvin - min_kelvin) * 63)
    return encoded_temperature

def save_temperature_state(corrected_celsius_temperature):
    """Saves the corrected temperature state, adjusted for sensor offset, into a 6-bit representation."""
    # Encode the corrected Celsius temperature into a 6-bit value
    encoded_temperature = encode_temperature_for_6bit(corrected_celsius_temperature)
    # Prepare the state dictionary with the encoded temperature
    temperature_state = {"encoded_temperature": encoded_temperature}
    # Save the state using badger_os
    badger_os.state_save("temperature_state", temperature_state)

def approximate_aqi_from_bme680(gas_resistance):
    """Approximates AQI from BME680 gas resistance readings."""
    # Example thresholds and mappings, these should be calibrated
    if gas_resistance > 19:
        aqi = 50  # Good air quality
        mapping = "Good"
    elif gas_resistance > 14:
        aqi = 100  # Moderate air quality
        mapping = "Moderate"
    elif gas_resistance > 10:
        aqi = 150  # Unhealthy for Sensitive Groups
        mapping = "Low"
    elif gas_resistance > 5:
        aqi = 200  # Unhealthy
        mapping = "Unhealthy"
    elif gas_resistance > 2:
        aqi = 300  # Very Unhealthy
        mapping = "Hazardous"
    else:
        aqi = 500  # Hazardous
        mapping = "Deadly"
    return aqi, mapping


while True:
    temperature, pressure, humidity, gas, status, _, _ = bme.read()
    heater = "Stable" if status & STATUS_HEATER_STABLE else "Unstable"
    # Convert pressure from pascals to hPa for display
    pressurehpa = pressure / 100
    
    # Correct the measured temperature with the sensor's offset
    temp = temperature + temp_offset  # Corrected temperature
    
    # Output to console for debugging
    print("{:0.2f}c, {:0.2f}Pa, {:0.2f}%, {:0.2f} Ohms, Heater: {}".format(
        temp, pressurehpa, humidity, gas, heater))
    
    # Prepare variables for display, rounding to one decimal place
    correctedtemp = round(temp, 1)  # Now keeping it as a float for further calculations
    press = round(pressurehpa, 1)
    humid = round(humidity, 1)
    
    # Adjust gas sensor reading based on humidity
    correctedgas = math.log(gas) + 0.04 * humidity
    
    # Calculate Dew Point and "Feels Like" temperature with the corrected, rounded temperature
    dew_point = calculate_dew_point(correctedtemp, humid)  # Using the rounded corrected temperature
    feels_like = calculate_feels_like(correctedtemp, humid)  # Same here
    
    # Calculate AQI from corrected gas value
    aqi_value, aqi_mapping = approximate_aqi_from_bme680(correctedgas)
    
    # Display the corrected environment values and calculations
    print("Corrected environment values:")
    print(f"Temperature: {correctedtemp}C, Pressure: {press}hPa, Humidity: {humid}%, Corrected Gas: {correctedgas}")
    print(f"Dew Point: {dew_point}C, Feels Like: {feels_like}C, AQI: {aqi_value}, Quality: {aqi_mapping}")
    
    
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
    badger.text("Temperature   "+ str(correctedtemp) +" C", 8, 50, TEXT_SIZE)
    badger.text(describe_temperature(correctedtemp), 245, 50, TEXT_SIZE)
    badger.text("Pressure       "+ str(press) +" hPa", 8, 70, TEXT_SIZE)
    badger.text(describe_pressure(pressurehpa), 245, 70, TEXT_SIZE)
    badger.text("Humidity       "+ str(humid) +" %", 8, 90, TEXT_SIZE)
    badger.text(describe_humidity(humidity), 245, 90, TEXT_SIZE)
    badger.thickness(1)
    badger.text("Heater "+heater+" ", 205, 120, 0.4)
    badger.text("Feels like "+ str(feels_like) +" C", 8, 30, 0.4)
    badger.text("Dewpoint "+ str(dew_point) +" C", 190, 30, 0.4)
    badger.text("Air quality (AQI)", 8, 110, 0.4)
    badger.text(str(aqi_value) +" " +str(aqi_mapping), 8, 120, 0.4)
    badger.update()
    time.sleep(30.0)
    badger.pen(15)
    badger.clear()