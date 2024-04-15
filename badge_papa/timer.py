# Badge Platform papa - hardware platform v3.0
# (2022-2024)
#
# timer.py : v3.1-refactor 0.0.0 (alpha4 code release - gfx) - fork eva_badge v3.0-refactor 0.9 (alpha4 code release - gfx)

import badger2040
import badger_os
import time
import gfx

# Default title and key/value file
TIMER_TITLE = "Wat moet ik doen?"
TIMER_FILE = "timer.txt"

# Open the timer file
try:
    badge = open("timer.txt", "r")
except OSError:
    with open("timer.txt", "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open("timer.txt", "r")
    
# Read in the next 6 lines
activity1 = badge.readline()  # "Japanse Thee"
time1 = badge.readline()      # "150" : 2.5mins
activity2 = badge.readline()  # "Presentatie 18"
time2 = badge.readline()      # "1080" : 18mins
activity3 = badge.readline()  # "Timer 5 "
time3 = badge.readline()      # "300" : 5mins
activity4 = badge.readline()  # "Timer 10"
time4 = badge.readline()      # "600" : 10mins
activity5 = badge.readline()  # "Timer 15"
time5 = badge.readline()      # "900" : 15mins
activity6 = badge.readline()  # "Timer 20"
time6 = badge.readline()      # "1200" : 20mins

# Global variables
ACTIVITY_DURATION = (
    (activity1, time1),
    (activity2, time2),
    (activity3, time3),
    (activity4, time4),
    (activity5, time5),
    (activity6, time6)
)

WIDTH = badger2040.WIDTH # 296
HEIGHT = badger2040.HEIGHT # 128

MENU_TEXT_SIZE = 0.5
MENU_SPACING = 16
MENU_WIDTH = 84
MENU_PADDING = 220  # Number of pixels between lefthandside and menu

TEXT_INDENT = MENU_WIDTH + 10

ARROW_THICKNESS = 3
ARROW_WIDTH = 18
ARROW_HEIGHT = 14
ARROW_PADDING = 2

ACTIVITY_TEXT_SIZE = 0.57
TITLE_SIZE = 0.56
ACTIVITY_HEIGHT = 30
TIME_HEIGHT = 20
ACTIVITY_TEXT_SIZE = 0.57
TIME_TEXT_SIZE = 1.8
LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

DEFAULT_TEXT="""
Japanse Thee
150
Presentatie 18
1080
Timer 5
300
Timer 10
600
Timer 15
900
Timer 20
1200"""

# Enable state for last activity selected
state = {"selected_activity": 0}
badger_os.state_load("timerstate", state)

# Number of bar positions
total_bars = 6

# State of draw_bars functions to enable the "run once"
draw_6bars_run_once = False
draw_5bars_run_once = False
draw_4bars_run_once = False
draw_3bars_run_once = False
draw_2bars_run_once = False
draw_1bars_run_once = False

# List items taken from timer.txt 
activity_list_items = [activity1, activity2, activity3, activity4, activity5, activity6]
activity_list_times = [time1, time2, time3, time4, time5, time6]
save_checklist = False
activity_iter = iter(activity_list_items)
activity_select = 0

# Temporary activity as placeholder for menu function
activity0 = 0
time0 = 0
updated_timer = 0

# Draw the title frame for the menu options
def draw_frame():
     # Set display parameters
    display.pen(15)
    display.clear()
    display.font("sans")
    display.thickness(2)
    # black box on top
    display.pen(12)
    display.rectangle(0, 0, 210, 22)
    display.pen(0)
    # title inverse
    display.text(TIMER_TITLE, 18, 10, TITLE_SIZE)
    display.pen(12)
    display.rectangle(0, HEIGHT - 20, WIDTH, 20) # ABC bar
    display.pen(0)
    display.line(0, 101, 296, 101)  # horizontal bottom line
    display.line(211, 0, 211, 100)  # vertical menu line
    display.text("START", 240, 120, MENU_TEXT_SIZE)
    display.thickness(ARROW_THICKNESS)

# Draw the menu on the righthand side
def draw_activity_menu():
    display.font("bitmap8")
    display.thickness(1)
    for i in range(len(ACTIVITY_DURATION)):
        activity0, time0 = ACTIVITY_DURATION[i]
        display.pen(0)
        if i == state["selected_activity"]:
            display.rectangle((MENU_PADDING - 5), i * MENU_SPACING, MENU_WIDTH, MENU_SPACING)
            display.pen(15)

        display.text(activity0, MENU_PADDING, (i * MENU_SPACING) + int((MENU_SPACING - 8) / 2), MENU_TEXT_SIZE)
        activity0, time0 = ACTIVITY_DURATION[state["selected_activity"]]
        time0_m = int(time0) / 60
        time0_m_r= str(round(time0_m))
        display.pen(15)
        display.rectangle(75, 45, 75, 25)
        display.pen(0)
        display.thickness(1)
        display.text(time0_m_r +" mins", 80, 50, 2)
    activity0, time0 = ACTIVITY_DURATION[state["selected_activity"]]
    display.thickness(1)
    display.update()

# Reduce the size of a string until it fits within a given width
def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text

# Convert time in timer.txt from seconds to minutes as string
def calculate_activity_time():
    time1_m = int(time1) / 60
    time1_m_r= str(round(time1_m))
    return activity_time

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
    activity0, time0 = ACTIVITY_DURATION[state["selected_activity"]]
    display.text(activity0, 5, 28, ACTIVITY_TEXT_SIZE)
    time0_m = int(time0) / 60
    time0_m_r= str(round(time0_m))
    display.text(time0_m_r +" mins totaal", 165, 28, ACTIVITY_TEXT_SIZE)   
    display.font("bitmap8")
    display.pen(0)
    display.thickness(1)
    display.text(str(round(bar_length) )+" s", 5, 120, MENU_TEXT_SIZE)
    display.font("sans")
    display.thickness(2)
    display.update()

# Calculate the duration each bar needs to represent
def calculate_bar_length(total_bars, activity_time):
    bar_duration = activity_time / total_bars
    d0 = [(i * bar_duration, (i + 1) * bar_duration) for i in range(total_bars)]
    #print("total bars (d0): ", d0) #debug
    d1 = (d0[0])
    #print("first bar size(d1): ", d0[0]) #debug
    d2 = [item[0] for item in d0]
    #print("get every second bar time (d2): ", d2) #debug
    d3 = d2[1]
    #print("bar duration unit (d3): ", d3) #debug
    d4 = d3 * 6
    #print("verification back to total time0 (d4): ", round(d4)) #debug
    d5 = round(d3,2)
    #print("rounded d3 to two digits (d5): ", d5) #keep this as function output only
    return d5, d4

# Draw 6 full bars and display the total time remaining (needs LED blink function to call)
def draw_6bars():
    global draw_6bars_run_once
    if draw_6bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST) # first draw is normal to get everything nice and sharp
    display.pen(0)    
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 65, 50, 45, 50, 85) # 6 fill
    display.pen(15)
    graphics.triangle(10, 65, 50, 45, 50, 85) # 6 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 105, 10, 65, 50, 85) # 5 fill
    display.pen(15)
    graphics.triangle(10, 105, 10, 65, 50, 85) # 5 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 125, 10, 105, 50, 85) # 4 fill
    display.pen(15)
    graphics.triangle(50, 125, 10, 105, 50, 85) # 4 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 105, 50, 125, 50, 85) # 3 fill
    display.pen(15)
    graphics.triangle(90, 105, 50, 125, 50, 85) # 3 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 65, 90, 105, 50, 85) # 2 fill
    display.pen(15)
    graphics.triangle(90, 65, 90, 105, 50, 85) # 2 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 45, 90, 65, 50, 85) # 1 fill
    display.pen(15)
    graphics.triangle(50, 45, 90, 65, 50, 85) # 1 outline
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("6bars_time0", time0)
    print("updated_timer", updated_timer)
    #print("6bars_time0_m_r", time0_m_r)
    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(100, 60, 72, 48)
    display.pen(0)
    display.text(str(updated_timer), 100, 85, 1.9)
    display.thickness(1)
    display.text("mins over", 100, 115, 0.55)
    display.update()
    draw_6bars_run_once = True

# Draw 5 full bars, 1 'empty' bar, specific activity placeholder and display the total time remaining
def draw_5bars():
    global draw_5bars_run_once
    if draw_5bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST) # first draw is normal to get everything nice and sharp
    display.pen(0)    
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 65, 50, 45, 50, 85) # 6 fill
    display.pen(15)
    graphics.triangle(10, 65, 50, 45, 50, 85) # 6 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 105, 10, 65, 50, 85) # 5 fill
    display.pen(15)
    graphics.triangle(10, 105, 10, 65, 50, 85) # 5 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 125, 10, 105, 50, 85) # 4 fill
    display.pen(15)
    graphics.triangle(50, 125, 10, 105, 50, 85) # 4 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 105, 50, 125, 50, 85) # 3 fill
    display.pen(15)
    graphics.triangle(90, 105, 50, 125, 50, 85) # 3 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 65, 90, 105, 50, 85) # 2 fill
    display.pen(15)
    graphics.triangle(90, 65, 90, 105, 50, 85) # 2 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 45, 90, 65, 50, 85) # 1 fill
    display.pen(15)
    graphics.triangle(50, 45, 90, 65, 50, 85) # 1 outline
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("5bars_time0", time0)
    print("updated_timer", updated_timer)
    #print("5bars_time0_m_r", time0_m_r)
    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(100, 60, 72, 48)
    display.pen(0)
    display.text(str(updated_timer), 100, 85, 1.9)
    display.thickness(1)
    display.text("mins over", 100, 115, 0.55)
    display.update()
    draw_5bars_run_once = True

# Draw 4 full bars, 2 'empty' bars, specific activity placeholder and display the total time remaining
def draw_4bars():
    global draw_4bars_run_once
    if draw_4bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST) # first draw is normal to get everything nice and sharp
    display.pen(0)    
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 65, 50, 45, 50, 85) # 6 fill
    display.pen(15)
    graphics.triangle(10, 65, 50, 45, 50, 85) # 6 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 105, 10, 65, 50, 85) # 5 fill
    display.pen(15)
    graphics.triangle(10, 105, 10, 65, 50, 85) # 5 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 125, 10, 105, 50, 85) # 4 fill
    display.pen(15)
    graphics.triangle(50, 125, 10, 105, 50, 85) # 4 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 105, 50, 125, 50, 85) # 3 fill
    display.pen(15)
    graphics.triangle(90, 105, 50, 125, 50, 85) # 3 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 65, 90, 105, 50, 85) # 2 fill
    display.pen(15)
    graphics.triangle(90, 65, 90, 105, 50, 85) # 2 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 45, 90, 65, 50, 85) # 1 fill
    display.pen(15)
    graphics.triangle(50, 45, 90, 65, 50, 85) # 1 outline
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("4bars_time0", time0)
    print("updated_timer", updated_timer)
    #print("4bars_time0_m_r", time0_m_r)
    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(100, 60, 72, 48)
    display.pen(0)
    display.text(str(updated_timer), 100, 85, 1.9)
    display.thickness(1)
    display.text("mins over", 100, 115, 0.55)
    display.update()
    draw_4bars_run_once = True

# Draw 3 full bars, 3 'empty' bars, specific activity placeholder and display the total time remaining
def draw_3bars():
    global draw_3bars_run_once
    if draw_3bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST) # first draw is normal to get everything nice and sharp
    display.pen(0)    
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 65, 50, 45, 50, 85) # 6 fill
    display.pen(15)
    graphics.triangle(10, 65, 50, 45, 50, 85) # 6 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 105, 10, 65, 50, 85) # 5 fill
    display.pen(15)
    graphics.triangle(10, 105, 10, 65, 50, 85) # 5 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 125, 10, 105, 50, 85) # 4 fill
    display.pen(15)
    graphics.triangle(50, 125, 10, 105, 50, 85) # 4 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 105, 50, 125, 50, 85) # 3 fill
    display.pen(15)
    graphics.triangle(90, 105, 50, 125, 50, 85) # 3 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 65, 90, 105, 50, 85) # 2 fill
    display.pen(15)
    graphics.triangle(90, 65, 90, 105, 50, 85) # 2 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 45, 90, 65, 50, 85) # 1 fill
    display.pen(15)
    graphics.triangle(50, 45, 90, 65, 50, 85) # 1 outline
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("3bars_time0", time0)
    print("updated_timer", updated_timer)
    #print("3bars_time0_m_r", time0_m_r)
    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(100, 60, 72, 48)
    display.pen(0)
    display.text(str(updated_timer), 100, 85, 1.9)
    display.thickness(1)
    display.text("mins over", 100, 115, 0.55)
    display.update()
    draw_3bars_run_once = True

# Draw 2 full bars, 4 'empty' bars, specific activity placeholder and display the total time remaining
def draw_2bars():
    global draw_2bars_run_once
    if draw_2bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST) # first draw is normal to get everything nice and sharp
    display.pen(0)    
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 65, 50, 45, 50, 85) # 6 fill
    display.pen(15)
    graphics.triangle(10, 65, 50, 45, 50, 85) # 6 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 105, 10, 65, 50, 85) # 5 fill
    display.pen(15)
    graphics.triangle(10, 105, 10, 65, 50, 85) # 5 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 125, 10, 105, 50, 85) # 4 fill
    display.pen(15)
    graphics.triangle(50, 125, 10, 105, 50, 85) # 4 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 105, 50, 125, 50, 85) # 3 fill
    display.pen(15)
    graphics.triangle(90, 105, 50, 125, 50, 85) # 3 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 65, 90, 105, 50, 85) # 2 fill
    display.pen(15)
    graphics.triangle(90, 65, 90, 105, 50, 85) # 2 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 45, 90, 65, 50, 85) # 1 fill
    display.pen(15)
    graphics.triangle(50, 45, 90, 65, 50, 85) # 1 outline
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("2bars_time0", time0)
    print("updated_timer", updated_timer)
    #print("2bars_time0_m_r", time0_m_r)
    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(100, 60, 72, 48)
    display.pen(0)
    display.text(str(updated_timer), 100, 85, 1.9)
    display.thickness(1)
    display.text("mins over", 100, 115, 0.55)
    display.update()
    draw_2bars_run_once = True

# Draw 1 full bar, 5 'empty' bars, specific activity placeholder and display the total time remaining
def draw_1bars():
    global draw_1bars_run_once
    if draw_1bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST) # first draw is normal to get everything nice and sharp
    display.pen(0)    
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 65, 50, 45, 50, 85) # 6 fill
    display.pen(15)
    graphics.triangle(10, 65, 50, 45, 50, 85) # 6 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(10, 105, 10, 65, 50, 85) # 5 fill
    display.pen(15)
    graphics.triangle(10, 105, 10, 65, 50, 85) # 5 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 125, 10, 105, 50, 85) # 4 fill
    display.pen(15)
    graphics.triangle(50, 125, 10, 105, 50, 85) # 4 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 105, 50, 125, 50, 85) # 3 fill
    display.pen(15)
    graphics.triangle(90, 105, 50, 125, 50, 85) # 3 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(90, 65, 90, 105, 50, 85) # 2 fill
    display.pen(15)
    graphics.triangle(90, 65, 90, 105, 50, 85) # 2 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(50, 45, 90, 65, 50, 85) # 1 fill
    display.pen(15)
    graphics.triangle(50, 45, 90, 65, 50, 85) # 1 outline
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("1bars_time0", time0)
    print("updated_timer", updated_timer)
    #print("1bars_time0_m_r", time0_m_r)
    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(100, 60, 196, 68)
    display.pen(0)
    display.text("bijna tijd", 100, 65, 1.1)
    display.text("opschieten", 100, 105, 1.1)
    display.pen(15)
    display.line(182, 85, 296, 85)
    display.update()
    draw_1bars_run_once = True

# The meat of the timer :-)
def countdown(time0):
    badger2040.system_speed(badger2040.SYSTEM_NORMAL)
    while time0:
        mins, secs = divmod(time0, 60)
        timeformat = '{:02d}:{:02d}'.format(mins,secs)
        print(timeformat, end='\r')
        #print("bar_length", bar_length)
        #print("time0", time0)
        display.led(255)
        if time0 > bar_length * 5:
            global updated_timer
            updated_timer = mins
            draw_6bars()
        if time0 > bar_length * 4 and time0 < bar_length * 5:
            global updated_timer
            updated_timer = mins
            draw_5bars()
        if time0 > bar_length * 3 and time0 < bar_length * 4:
            updated_timer = mins
            draw_4bars()
        if time0 > bar_length * 2 and time0 < bar_length * 3:
            updated_timer = mins
            draw_3bars()
        if time0 > bar_length * 1 and time0 < bar_length * 2:
            updated_timer = mins
            draw_2bars()
        if time0  < bar_length * 1:
            updated_timer = mins
            draw_1bars()        
        time.sleep(0.5) # Split the 1 sec countdown into 2* 0.5 secs to enable LED blink
        display.led(0)
        time.sleep(0.5)
        time0 -= 1
        #display.led(0) # get to this when countdown function is finished
        #display.pen(15)
        #display.rectangle(100, 45, 100, 30)
        #display.pen(0)
        #display.thickness(2)
        #display.text(timeformat, 100, 60, TIME_TEXT_SIZE)
        #display.update()
    print("stoppppp")
    display.update_speed(badger2040.UPDATE_FAST)

    # clear the minutes righthand side
    display.pen(15)
    display.rectangle(0, 45, 296, 83)
    display.pen(0)
    display.rectangle(100, 55, 112, 30)
    display.pen(15)
    display.thickness(2)
    display.text("KLAAR", 100, 70, 1.2)
    display.update()

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
graphics = gfx.GFX(296, 128, display.pixel)
display.led(128)

# Variable e-INK screen update speeds
changed = not badger2040.woken_by_button()

if changed:
    display.update_speed(badger2040.UPDATE_FAST)
    badger2040.system_speed(badger2040.SYSTEM_TURBO)
else:
    display.update_speed(badger2040.UPDATE_TURBO)
    badger2040.system_speed(badger2040.SYSTEM_NORMAL)

# system speed increased for activity menu. Slow down on countdown
#display.system_speed(badger2040.SYSTEM_FAST)
#badger2040.system_speed(badger2040.SYSTEM_FAST)

# ------------------------------
#       Main program loop
# ------------------------------

while True:
    if display.pressed(badger2040.BUTTON_UP):
        state["selected_activity"] -= 1
        if state["selected_activity"] < 0:
            state["selected_activity"] = len(ACTIVITY_DURATION) - 1
        changed = True
        
    if display.pressed(badger2040.BUTTON_DOWN):
        state["selected_activity"] += 1
        if state["selected_activity"] >= len(ACTIVITY_DURATION):
            state["selected_activity"] = 0
        changed = True

    if display.pressed(badger2040.BUTTON_C):    
        activity0, time0 = ACTIVITY_DURATION[state["selected_activity"]]
        time0_m = int(time0) / 60
        time0_m_r= str(round(time0_m))
        print(time0_m_r)
        bar_length, total_time = calculate_bar_length(total_bars,int(time0))
        draw_timer_framework()
        display.led(0)
        countdown(int(time0))

    if changed:
        draw_frame()
        draw_activity_menu()
        badger_os.state_save("timerstate", state)
        print(state["selected_activity"])
        changed = False
        display.led(0)

    display.halt()