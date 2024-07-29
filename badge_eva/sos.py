# Badge Platform papa - hardware platform v3.0
# (2022-2024)
#
# sos.py : v1.0-refactor 0.0.0

import badger2040
import badger_os
import time
import gfx

# Default title and key/value file
SOS_TITLE = "Noodnummers"
SOS_FILE = "sos.txt"

# Open the timer file
try:
    badge = open("sos.txt", "r")
except OSError:
    with open("sos.txt", "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open("sos.txt", "r")
    
# Read in the next 12 lines
person1 = badge.readline()  # 
number1 = badge.readline()      # 
person2 = badge.readline()  # 
number2 = badge.readline()      # 
person3 = badge.readline()  # 
number3 = badge.readline()      # 
person4 = badge.readline()  # 
number4 = badge.readline()      # 
person5 = badge.readline()  # 
number5 = badge.readline()      # 
person6 = badge.readline()  # 
number6 = badge.readline()      # 

# Global variables
ACTIVITY_DURATION = (
    (person1, number1),
    (person2, number2),
    (person3, number3),
    (person4, number4),
    (person5, number5),
    (person5, number6)
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
person1
number1
person2
number2
person3
number3
person4
number4
person5
number5
person6
number6"""


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