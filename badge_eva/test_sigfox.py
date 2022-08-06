from machine import UART
from machine import Pin
import time

# Initialize serial Port
lora = UART(0,baudrate = 9600,tx = Pin(0),rx = Pin(1))

def SigfoxInfo():        
                print("Get Status - should be OK")
                lora.write("AT\r\n")      # Write AT Command
                data=lora.read(2)         # Response Should be OK
                print(data)

                print("Get ID")
                lora.write("AT$I=10\r\n") # Send Command to Get ID
                data=lora.read(10)
                print(data)

                print("Get PAC")
                lora.write("AT$I=11\r\n") # Send Command to Get ID
                data=lora.read(18)
                print(data)

def SigfoxSend():
                # Initiate a Transmission
                print("Init Transmission")
                sleep(1)
                lora.write("AT$RC\r\n") # Send Command to Reset Macro Channels
                data=lora.read(4)
                print(data)
                lora.write("AT$SF=AABBCCDD\r\n")
                sleep(6)
                data=lora.read(4)        # We should get a OK response
                print(data)

  
#        SigfoxInfo()
#        SigfoxSend()

#dataRead = lora.read(2)
#print(dataRead)
#print(SigfoxInfo)
#print(SigfoxSend)

print("Get Status - should be OK")
lora.write("AT\r\n")      # Write AT Command
data1=lora.read(2)         # Response Should be OK
print(data1)

print("Get ID")
lora.write("AT$I=10\r\n") # Send Command to Get ID
data2=lora.read(10)
print(data2)

print("Get PAC")
lora.write("AT$I=11\r\n") # Send Command to Get ID
data3=lora.read(18)
print(data3)