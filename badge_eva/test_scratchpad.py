import badger2040
import badger_os
import time
import gfx

#from threading import Thread

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
graphics = gfx.GFX(296, 128, display.pixel)

#graphics.line(0, 0, 296, 128)
#graphics.rect(10, 40, 50, 50)
#graphics.fill_rect(50, 5, 50, 50)

ACTIVITY_TEXT_SIZE = 0.57
TITLE_SIZE = 0.56
MENU_TEXT_SIZE = 0.5

activity0 = "schoenen"
time0 = 300
bar_length = 2.67

# Draw the timer framework
def draw_timer_framework():
    display.led(128)
    display.pen(15)
    display.clear()
    # Set display parameters
    display.pen(15)
    display.font("sans")
    display.thickness(2)
    # black box on top
    display.pen(0)
    display.rectangle(0, 0, 296, 22)
    display.pen(15)
    display.text("Hoelang heb ik de tijd ?", 30, 10, TITLE_SIZE)
    display.pen(0)
    display.line(0, 39, 296, 39)
    display.line(182, 85, 296, 85)
    display.pen(0)
    display.thickness(1)
    #activity0, time0 = ACTIVITY_DURATION[state["selected_activity"]]
    display.text(activity0, 5, 28, ACTIVITY_TEXT_SIZE)
    time0_m = int(time0) / 60
    time0_m_r= str(round(time0_m))
    #display.text(time0_m_r +" mins totaal", 165, 28, ACTIVITY_TEXT_SIZE)   
    display.thickness(2)
    #display.update()

draw_timer_framework()



# Draw pie with 6 triangled parts
display.thickness(2)

display.pen(0)
graphics.fill_triangle(10, 65, 50, 45, 50, 85) # 6 fill
display.pen(15)
graphics.triangle(10, 65, 50, 45, 50, 85) # 6 outline

display.pen(0)
graphics.fill_triangle(10, 105, 10, 65, 50, 85) # 5 fill
display.pen(15)
graphics.triangle(10, 105, 10, 65, 50, 85) # 5 outline

display.pen(0)
graphics.fill_triangle(50, 125, 10, 105, 50, 85) # 4 fill
display.pen(15)
graphics.triangle(50, 125, 10, 105, 50, 85) # 4 outline

display.pen(0)
graphics.fill_triangle(90, 105, 50, 125, 50, 85) # 3 fill
display.pen(15)
graphics.triangle(90, 105, 50, 125, 50, 85) # 3 outline

display.pen(12)
graphics.fill_triangle(90, 65, 90, 105, 50, 85) # 2 fill
display.pen(15)
graphics.triangle(90, 65, 90, 105, 50, 85) # 2 outline

display.pen(12)
graphics.fill_triangle(50, 45, 90, 65, 50, 85) # 1 fill
display.pen(15)
graphics.triangle(50, 45, 90, 65, 50, 85) # 1 outline

#display.pen(15)
#graphics.fill_circle(50, 85, 25)
#display.pen(0)
#display.text(str(6), 30, 85, 1.1)


display.pen(15)
display.rectangle(100, 60, 72, 48)
display.pen(0)
display.text(str(17), 100, 85, 1.9)
#display.text("bijna tijd", 100, 65, 1.1)
display.thickness(1)
display.text("mins over", 100, 115, 0.55)
#display.text("opschieten", 100, 105, 1.1)
display.pen(15)
display.line(182, 85, 296, 85)

display.font("bitmap8")
display.pen(0)
display.thickness(1)
display.text(str(bar_length), 5, 120, MENU_TEXT_SIZE)

display.update()
