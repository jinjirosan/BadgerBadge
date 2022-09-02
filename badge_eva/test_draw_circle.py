import badger2040
import badger_os
import time
import math
import gfx

WIDTH = badger2040.WIDTH # 296
HEIGHT = badger2040.HEIGHT # 128

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
graphics = gfx.GFX(296, 128, display.pixel)
display.led(128)

ACTIVITY_TEXT_SIZE = 0.57
TITLE_SIZE = 0.56
MENU_TEXT_SIZE = 0.5

activity0 = 0
time0 = 0
bar_length = 0
activity_duration = 0
updated_timer = 16

#display.font("bitmap8")

display.update_speed(badger2040.UPDATE_FAST) # first draw is normal to get everything nice and sharp

# Draw the focus framework
def draw_focus_framework():
    display.led(128)
    display.pen(15)
    display.clear()
    # Set display parameters
    display.pen(15)
    display.font("sans")
    display.thickness(2)
    # black box on top
    display.pen(0)
    display.rectangle(100, 0, 296, 22)
    display.pen(15)
    display.text("Even tijd voor mezelf", 110, 10, TITLE_SIZE)
    display.pen(0)
    display.line(100, 39, 296, 39)
    display.line(182, 80, 296, 80)
    display.pen(0)
    display.thickness(1)
    #activity0, time0 = ACTIVITY_DURATION[state["selected_activity"]]
    #display.text(activity0, 5, 28, ACTIVITY_TEXT_SIZE)
    #time0_m = int(time0) / 60
    #time0_m_r= str(round(time0_m))
    #display.text(time0_m_r +" mins totaal", 165, 28, ACTIVITY_TEXT_SIZE)   
    display.font("bitmap8")
    display.pen(0)
    display.thickness(1)
    display.text(str(round(bar_length) )+" s", 280, 120, MENU_TEXT_SIZE)
    display.font("sans")
    display.thickness(2)
    #display.update()

draw_focus_framework()

# slices
display.pen(0)    
display.thickness(2) # nice fat pie and lines
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(246, 93, 266, 83, 266, 103) # 6 fill
display.pen(15)
graphics.triangle(246, 93, 266, 83, 266, 103) # 6 outline +200x
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(246, 113, 246, 93, 266, 103) # 5 fill +200x
display.pen(15)
graphics.triangle(246, 113, 246, 93, 266, 103) # 5 outline +200x
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(266, 123, 246, 113, 266, 103) # 4 fill +200x
display.pen(15)
graphics.triangle(266, 123, 246, 113, 266, 103) # 4 outline
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(286, 113, 266, 123, 266, 103) # 3 fill +200x
display.pen(15)
graphics.triangle(286, 113, 266, 123, 266, 103) # 3 outline +200x
display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(286, 93, 286, 113, 266, 103) # 2 fill
display.pen(15)
graphics.triangle(286, 93, 286, 113, 266, 103) # 2 outline +200x
display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
graphics.fill_triangle(266, 83, 286, 93, 266, 103) # 1 fill +200x
display.pen(15)
graphics.triangle(266, 83, 286, 93, 266, 103) # 1 outline +200x


# remaining time
display.pen(0)
display.text(str(updated_timer), 190, 102, 1)
display.thickness(1)
display.font("bitmap8")
display.text("mins over", 190, 120, 0.55)



# traffic light
display.pen(0)
display.thickness(2) # nice fat pie and lines
graphics.circle(47, 22, 20) # red outline
graphics.fill_circle(47, 22, 15) # red fill
graphics.fill_triangle(15, 28, 15, 16, 20, 22) # arrow
graphics.fill_rect(5, 20, 10, 5)
display.pen(15)
#graphics.triangle(10, 27, 10, 17, 20, 22)
display.pen(15) # disable for non-fill letter
display.font("sans")
display.thickness(1)
display.text("R", 40, 22, 0.7)

display.pen(0)
display.thickness(2) # nice fat pie and lines
graphics.circle(47, 64, 20) # orange outline
#graphics.fill_circle(47, 64, 15) # orange fill
#display.pen(15) # disable for non-fill letter
display.font("sans")
display.thickness(1)
display.text("O", 40, 64, 0.7)

display.pen(0)
display.thickness(2) # nice fat pie and lines
graphics.circle(47, 106, 20) # green outline
#graphics.fill_circle(47, 106, 15) # green fill
#display.pen(15) # disable for non-fill letter
display.font("sans")
display.thickness(1)
display.text("G", 40, 105, 0.7)

display.update()
display.led(0)