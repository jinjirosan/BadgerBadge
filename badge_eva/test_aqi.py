# Badge Platform Eva - hardware platform v3.0
# (2022) Voor m'n lieve guppie
#
# test_aqi.py : v3.0-refactor 0.2

import math as np
from bme680 import *
from breakout_bme68x import BreakoutBME68X, STATUS_HEATER_STABLE
from machine import Pin, I2C
import pimoroni_i2c
from time import *

#i2c = I2C(0, scl=Pin(5), sda=Pin(4))
#sensor680 = BME680_I2C(i2c=i2c)

PINS_PICO_EXPLORER = {"sda": 4, "scl": 5}
i2c = pimoroni_i2c.PimoroniI2C(**PINS_PICO_EXPLORER)
sensor680 = BreakoutBME68X(i2c,0x77)

class IAQTracker:
    def __init__(self, burn_in_cycles = 300, gas_recal_period = 3600, ph_slope = 0.03):
        self.slope = ph_slope
        self.burn_in_cycles = burn_in_cycles        #determines burn-in-time, usually 5 minutes, equal to 300 cycles of 1s duration
        self.gas_cal_data = []
        self.gas_ceil = 0
        self.gas_recal_period = gas_recal_period    #number of cycles after which to drop last entry of the gas calibration list. Here: 1h
        self.gas_recal_step = 0
    
    
    
    
    #calculates the saturation water density of air at the current temperature (in °C)
    #return the saturation density rho_max in kg/m^3
    #this is equal to a relative humidity of 100% at the current temperature 
    def waterSatDensity(self, temp):
        rho_max = (6.112* 100 * np.exp((17.62 * temp)/(243.12 + temp)))/(461.52 * (temp + 273.15))
        return rho_max
    
        
        
    def getIAQ(self, bme_data):
        temp = bme_data.temperature
        press = bme_data.pressure
        hum = bme_data.humidity
        R_gas = bme_data.gas_resistance
        
        
        #calculate stauration density and absolute humidity
        rho_max = self.waterSatDensity(temp)
        hum_abs = hum * 10 * rho_max
        
        #compensate exponential impact of humidity on resistance
        comp_gas = R_gas * np.exp(self.slope * hum_abs)
        
        if self.burn_in_cycles > 0:
            #check if burn-in-cycles are recorded
            self.burn_in_cycles -= 1        #count down cycles
            if comp_gas > self.gas_ceil:    #if value exceeds current ceiling, add to calibration list and update ceiling
                self.gas_cal_data = [comp_gas]
                self.gas_ceil = comp_gas
            return None         #return None type as sensor burn-in is not yet completed
        else:
            #adapt calibration
            if comp_gas > self.gas_ceil:
                self.gas_cal_data.append(comp_gas)
                if len(self.gas_cal_data) > 100:
                    del self.gas_cal_data[0]
                self.gas_ceil = np.mean(self.gas_cal_data)
            
            
            #calculate and print relative air quality on a scale of 0-100%
            #use quadratic ratio for steeper scaling at high air quality
            #clip air quality at 100%
            AQ = np.minimum((comp_gas / self.gas_ceil)**2, 1) * 100
            
            
            
            #for compensating negative drift (dropping resistance) of the gas sensor:
            #delete oldest value from calibration list and add current value
            self.gas_recal_step += 1
            if self.gas_recal_step >= self.gas_recal_period:
                self.gas_recal_step = 0
                self.gas_cal_data.append(comp_gas)
                del self.gas_cal_data[0]
                self.gas_ceil = np.mean(self.gas_cal_data)
        
        
        return AQ


#BME680 initialization
bme680_temp_offset = -4.5       #temperature oofset: depends on heating profile and external heat sources close to mounting point (i.e. Raspberry Pi SoC)


#sensor680 = bme680(i2c_addr=0x77)

sensor680.set_humidity_oversample(bme680.OS_2X)
sensor680.set_pressure_oversample(bme680.OS_4X)
sensor680.set_temperature_oversample(bme680.OS_8X)
sensor680.set_filter(bme680.FILTER_SIZE_3)
sensor680.set_gas_status(bme680.ENABLE_GAS_MEAS)

sensor680.set_gas_heater_temperature(320)
sensor680.set_gas_heater_duration(150)
sensor680.select_gas_heater_profile(0)
sensor680.set_temp_offset(bme680_temp_offset)


sensor680.get_sensor_data()



temp = 0
press = 0
hum = 0
R_gas = 0


#data prompt function
def prompt_data(temp, press, hum, Rgas, AQ):    
    out_string = "{0}: {1:.2f}°C, {2:.2f}hPa, {3:.2f}%RH, {4:.1f}kOhm".format(strftime("%Y-%m-%d %H:%M:%S"),temp,press,hum,R_gas/1000)
    if AQ == None:
        out_string += ", cal."
    else:
        out_string += ", {0:.1f}%aq".format(AQ)
    print(out_string)
    

#Initialize IAQ calculator
iaq_tracker = IAQTracker()

#main loop
while True:
    if sensor680.get_sensor_data():
        temp = sensor680.data.temperature
        press = sensor680.data.pressure
        hum = sensor680.data.humidity
        
        
        if sensor680.data.heat_stable:
            R_gas = sensor680.data.gas_resistance
            AQ = iaq_tracker.getIAQ(sensor680.data)
        else:
            R_gas = 0
            AQ = None
            
            
        prompt_data(temp, press, hum, R_gas, AQ)
        
    sleep(1)