import badger2040
import badger_os
import time

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()

display.pen(0)
display.rectangle(100, 45, 112, 30)
display.pen(15)
display.text("KLAAR", 100, 60, 1.2)
display.update()