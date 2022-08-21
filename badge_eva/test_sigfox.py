from machine import UART
from machine import Pin
import time

# Initialize serial Port
lora = UART(0,baudrate = 9600,tx = Pin(0),rx = Pin(1))

def SigfoxInfo():        
    sf_info = dict();
    print("Get Status - should be OK")
    lora.write("AT\r\n")      # Write AT Command
    time.sleep(2)
    sf_status = lora.read(2)         # Response Should be OK
    sf_info['Status'] = sf_status
    print(sf_status)

    print("Get ID")
    lora.write("AT$I=10\r\n") # Send Command to Get ID
    time.sleep(2)
    sf_id = lora.read(10)
    sf_info['ID'] = sf_id
    print(sf_id)

    print("Get PAC")
    lora.write("AT$I=11\r\n") # Send Command to Get ID
    time.sleep(2)
    sf_pac = lora.read(18)
    sf_info['PAC'] = sf_pac
    print(sf_pac)
    
    return sf_info
    
def SigfoxSend():
    # Initiate a Transmission
    print("Init Transmission")
    time.sleep(1)
    lora.write("AT$RC\r\n") # Send Command to Reset Macro Channels
    time.sleep(2)
    data=lora.read(4)
    print(data)
    lora.write("AT$SF=AABBCCDD\r\n")  # sends a test string "AABBCCDD"
    time.sleep(6)
    data=lora.read(4)        # We should get a OK response
    print(data)

  
#SigfoxInfo()
#SigfoxSend()

#dataRead = lora.read(2)
#print(dataRead)
#print(SigfoxInfo)
#print(SigfoxSend)

print(SigfoxInfo())

SigfoxSend()