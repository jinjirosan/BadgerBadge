# Badger 2040 graphics - colours
import badger2040
import machine
import time
fonts = ["sans","gothic","cursive","serif","serif_italic"]
display = badger2040.Badger2040()
display.update_speed(badger2040.UPDATE_NORMAL) # Slow but clearest
# Clear screen to white
display.pen(15)
display.clear()
display.update()
w = 18
# Set up text
display.font(fonts[3])
display.thickness(2)
display.pen(0)

# Centred text heading
space = (display.measure_text("Dither/Colour",0.8))
space = int((296-space)/2)
display.text("Dither/Colour",space,15,0.8)

# Hexadecimal dither colour values
hexa = ["0","1","2","3","4","5","6","7","8","9","A","B","C","D","E","F"]
w = 18 # Width of bars
for c in range(16):
    display.pen(c)
    display.rectangle(4+18*c,30,18,140)
    display.pen(15)
    if c > 7:
        display.pen(0)
    display.text(hexa[c],6+18*c,60+ c*3,0.6)
display.update()
time.sleep(5)