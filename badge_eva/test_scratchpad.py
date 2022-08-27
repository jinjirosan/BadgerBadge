import badger2040
import badger_os
import time
#from threading import Thread

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()



display.pen(10)
display.rectangle(230, 45, 700, 50)
display.pen(0)
display.text(str(16), 230, 70, 1.8)
display.update()
