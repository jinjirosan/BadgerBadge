import badger2040
import badger_os
import time
#import gfx

#from threading import Thread

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
#graphics = gfx.GFX(296, 128, display.pixel)

badger = badger2040.Badger2040()
badger.system_speed(badger2040.SYSTEM_FAST)

