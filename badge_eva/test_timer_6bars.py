# Badge Platform Eva - hardware platform v3.0
# (2022) Voor m'n lieve guppie
#
# timer.py : v3.0-refactor 0.6 (alpha5 code release)

import badger2040
import badger_os
import time

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
activity1 = badge.readline()  # "aankleden"
time1 = badge.readline()      # "900" : 15mins
activity2 = badge.readline()  # "ontbijt"
time2 = badge.readline()      # "960" : 16mins
activity3 = badge.readline()  # "schoenen"
time3 = badge.readline()      # "300" : 5mins
activity4 = badge.readline()  # "douchen"
time4 = badge.readline()      # "1200" : 20mins
activity5 = badge.readline()  # "pootjes wassen"
time5 = badge.readline()      # "720" : 12mins
activity6 = badge.readline()  # "pyama"
time6 = badge.readline()      # "420" : 7mins

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
aankleden
900
ontbijt
960
schoenen
300
douchen
1200
pootjes wassen
720
pyama
420"""

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
    display.line(0, 101, 296, 101)
    display.pen(0)
    display.thickness(1)
    activity0, time0 = ACTIVITY_DURATION[state["selected_activity"]]
    display.text(activity0, 5, 28, ACTIVITY_TEXT_SIZE)
    time0_m = int(time0) / 60
    time0_m_r= str(round(time0_m))
    display.text(time0_m_r +" mins totaal", 165, 28, ACTIVITY_TEXT_SIZE)   
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
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    display.thickness(2)
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("6bars_time0", time0)
    print("updated_timer", updated_timer)
    #print("6bars_time0_m_r", time0_m_r)
    display.pen(15)
    display.rectangle(226, 45, 700, 50)
    display.pen(0)
    display.text(str(updated_timer), 226, 70, TIME_TEXT_SIZE)
    display.update()
    draw_6bars_run_once = True

# Draw 5 full bars, 1 'empty' bar, specific activity placeholder and display the total time remaining
def draw_5bars():
    global draw_5bars_run_once
    if draw_5bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST) # screen update turbo for easy quick refresh
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.pen(12)
    display.line(185, 92, 205, 92) # bar 6
    display.thickness(2)
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("5bars_time0", time0)
    print("updated_timer", updated_timer)
    display.pen(15)
    display.rectangle(226, 45, 700, 50)
    display.pen(0)
    display.text(str(updated_timer), 226, 70, TIME_TEXT_SIZE)
    display.update()
    draw_5bars_run_once = True

# Draw 4 full bars, 2 'empty' bars, specific activity placeholder and display the total time remaining
def draw_4bars():
    global draw_4bars_run_once
    if draw_4bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.pen(12)
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    display.thickness(2)
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("4bars_time0", time0)
    print("updated_timer", updated_timer)
    display.pen(15)
    display.rectangle(226, 45, 700, 50)
    display.pen(0)
    display.text(str(updated_timer), 226, 70, TIME_TEXT_SIZE)
    display.update()
    draw_4bars_run_once = True

# Draw 3 full bars, 3 'empty' bars, specific activity placeholder and display the total time remaining
def draw_3bars():
    global draw_3bars_run_once
    if draw_3bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.pen(12)
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    display.thickness(2)
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("3bars_time0", time0)
    print("updated_timer", updated_timer)
    display.pen(15)
    display.rectangle(226, 45, 700, 50)
    display.pen(0)
    display.text(str(updated_timer), 226, 70, TIME_TEXT_SIZE)
    display.update()
    draw_3bars_run_once = True

# Draw 2 full bars, 4 'empty' bars, specific activity placeholder and display the total time remaining
def draw_2bars():
    global draw_2bars_run_once
    if draw_2bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.pen(12)
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    display.thickness(2)
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("2bars_time0", time0)
    print("updated_timer", updated_timer)
    display.pen(15)
    display.rectangle(226, 45, 700, 50)
    display.pen(0)
    display.text(str(updated_timer), 226, 70, TIME_TEXT_SIZE)
    display.update()
    draw_2bars_run_once = True

# Draw 1 full bar, 5 'empty' bars, specific activity placeholder and display the total time remaining
def draw_1bars():
    global draw_1bars_run_once
    if draw_1bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_FAST)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.pen(12)
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    display.thickness(2)
    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("1bars_time0", time0)
    print("updated_timer", updated_timer)
    display.pen(15)
    display.rectangle(226, 45, 700, 50)
    display.pen(0)
    display.text(str(updated_timer), 226, 70, TIME_TEXT_SIZE)
    display.update()
    draw_1bars_run_once = True

# The meat of the timer :-)
def countdown(time0):
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
    display.pen(15)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    # clear the minutes righthand side
    display.pen(15)
    display.rectangle(230, 45, 700, 50)
    display.pen(0)
    display.rectangle(100, 55, 112, 30)
    display.pen(15)
    display.thickness(2)
    display.text("KLAAR", 100, 70, 1.2)
    display.update()

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
display.led(128)

# Variable e-INK screen update speeds
changed = not badger2040.woken_by_button()

if changed:
    display.update_speed(badger2040.UPDATE_FAST)
else:
    display.update_speed(badger2040.UPDATE_TURBO)

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

