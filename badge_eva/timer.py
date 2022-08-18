# Badge Platform Eva - hardware platform v3.0
# (2022) Voor m'n lieve guppie
#
# timer.py : v3.0-refactor 0.5 (alpha code release)

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

WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

MENU_TEXT_SIZE = 0.5
MENU_SPACING = 16
MENU_WIDTH = 84
MENU_PADDING = 220  # number of pixels between lefthandside and menu

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
TIME_TEXT_SIZE = 1.0
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

state = {"selected_activity": 0}
badger_os.state_load("timerstate", state)

# List items taken from timer.txt 
activity_list_items = [activity1, activity2, activity3, activity4, activity5, activity6]
activity_list_times = [time1, time2, time3, time4, time5, time6]
save_checklist = False
activity_iter = iter(activity_list_items)
activity_select = 0

# temporary activity as placeholder for menu function
activity0 = 0
time0 = 0

# Draw a upward arrow
def draw_up(x, y, width, height, thickness, padding):
    border = (thickness // 4) + padding
    display.line(x + border, y + height - border,
                 x + (width // 2), y + border)
    display.line(x + (width // 2), y + border,
                 x + width - border, y + height - border)


# Draw a downward arrow
def draw_down(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(x + border, y + border,
                 x + (width // 2), y + height - border)
    display.line(x + (width // 2), y + height - border,
                 x + width - border, y + border)


# Draw the title frame for the menu options
def draw_frame():
     # Set display parameters
    display.pen(15)
    display.clear()
    display.font("sans")
    display.thickness(2)
    # black box on top
    display.pen(12)
    display.rectangle(0, 0, 180, 22)
    display.pen(0)
    # title inverse
    display.text(TIMER_TITLE, 10, 10, TITLE_SIZE)
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

def calculate_activity_time():
    time1_m = int(time1) / 60
    time1_m_r= str(round(time1_m))
    return activity_time

# draw the timer framework
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
    display.text(time0_m_r +" mins", 220, 28, ACTIVITY_TEXT_SIZE)
    #display.text(str(round(time1_m)), 180, 50, TIME_TEXT_SIZE)
    display.thickness(2)
    display.update()

def countdown(time_sec):
    display.update_speed(badger2040.UPDATE_TURBO)
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins,secs)
        print(timeformat, end='\r')
        time.sleep(1)
        time_sec -= 1
        display.pen(15)
        display.rectangle(100, 45, 100, 30)
        display.pen(0)
        display.thickness(2)
        display.text(timeformat, 100, 60, TIME_TEXT_SIZE)
        display.update()
    print("stoppppp")
    display.pen(0)
    display.rectangle(100, 45, 100, 30)
    display.pen(15)
    display.text("KLAAR", 100, 60, TIME_TEXT_SIZE)
    display.update()

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
display.led(128)

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