import badger2040
import badger_os
import time
import math

WIDTH = badger2040.WIDTH # 296
HEIGHT = badger2040.HEIGHT # 128

def circle(x,y,r,c):
    display.update_speed(badger2040.UPDATE_NORMAL)
    display.pen(0)
    display.line(x-r,y,r*2,c)
    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i)) # Pythagoras!
        display.line(x-a,y+i,a*2,c) # Lower half
        display.line(x-a,y-i,a*2,c) # Upper half
        display.update()
        #time.sleep(0.1)
    
    
# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
display.led(128)

circle(200, 60, 3, 30)