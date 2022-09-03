# Badge Platform Eva - hardware platform v3.0
# (2022) Voor m'n lieve guppie
#
# focus.py : v3.0-refactor 0.2

import badger2040
import badger_os
import time
import math
import gfx

# Default title and key/value file
FOCUS_TITLE = "Focus stoplicht"
FOCUS_FILE = "focus.txt"

# Open the focus file
try:
    badge = open("focus.txt", "r")
except OSError:
    with open("focus.txt", "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open("focus.txt", "r")
    
# Read in the next 6 lines
focus_setting1 = badge.readline()  # "Focus 60 mins"
time1_red = badge.readline()       # "3600" : 60mins
time1_orange = badge.readline()    # "1800" : 30mins
focus_setting2 = badge.readline()  # "Focus 30 mins"
time2_red = badge.readline()       # "1800" : 30mins
time2_orange = badge.readline()    # "900" : 15mins
focus_setting3 = badge.readline()  # "Focus 10 mins"
time3_red = badge.readline()       # "600" : 10mins
time3_orange = badge.readline()    # "300" : 5mins

# Global variables
FOCUS_DURATION = (
    (focus_setting1, time1_red, time1_orange),
    (focus_setting2, time2_red, time2_orange),
    (focus_setting3, time3_red, time3_orange)
)

WIDTH = badger2040.WIDTH # 296
HEIGHT = badger2040.HEIGHT # 128

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
graphics = gfx.GFX(296, 128, display.pixel)
display.led(128)

ACTIVITY_TEXT_SIZE = 0.57
TITLE_SIZE = 0.56
MENU_TEXT_SIZE = 0.5

DEFAULT_TEXT="""
Focus 60 mins
3600
1800
Focus 30 mins
1800
900
Focus 10 mins
600
300"""

# Enable state for last activity selected
state = {"selected_focus": 0}
badger_os.state_load("focusstate", state)



# Number of slice positions
total_slices = 6

# State of draw_slices functions to enable the "run once"
draw_6slices_run_once = False
draw_5slices_run_once = False
draw_4slices_run_once = False
draw_3slices_run_once = False
draw_2slices_run_once = False
draw_1slice_run_once = False

# List items taken from focus.txt 
focus_list_items = [focus_setting1, focus_setting2, focus_setting3]
focus_list_times = [time1_red, time1_orange, time2_red, time2_orange, time3_red, time3_orange]
save_checklist = False
focus_iter = iter(focus_list_items)
focus_select = 0

# Temporary activity as placeholder for menu function
focus0 = 0
time0_red = 0
time0_orange = 0
updated_focus = 0
bar_length = 0
activity_duration = 0
updated_timer = 16

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
    display.rectangle(160, 0, 296, 22)
    display.pen(15)
    display.text(FOCUS_TITLE, 165, 10, TITLE_SIZE)
    display.pen(0)
    display.line(160, 39, 296, 39) # top
    display.line(182, 80, 296, 80) # bottom
    # selected focus parameters
    display.pen(0)
    display.thickness(1)
    display.font("bitmap8")
    #activity0, time0 = ACTIVITY_DURATION[state["selected_activity"]]
    #display.text(activity0, 5, 28, ACTIVITY_TEXT_SIZE)
    #time0_m = int(time0) / 60
    #time0_m_r= str(round(time0_m))
    #display.text(time0_m_r +" mins totaal", 165, 28, ACTIVITY_TEXT_SIZE)
    
    # duration indicator 60-30
    display.pen(0)
    graphics.fill_rect(160, 24, 13, 11)
    graphics.rect(171, 24, 13, 11)
    display.pen(15)
    display.thickness(1)
    display.font("bitmap8")
    display.text("60", 162, 26, 0.1)
    display.pen(0)
    display.text("30", 173, 26, 0.1)

    # duration indicator 30-15
    display.pen(0)
    graphics.fill_rect(187, 24, 13, 11)
    graphics.rect(198, 24, 13, 11)
    display.pen(15)
    display.thickness(1)
    display.font("bitmap8")
    display.text("30", 189, 26, 0.1)
    display.pen(0)
    display.text("15", 201, 26, 0.1)
    
    # duration indicator 10-5
    display.pen(0)
    graphics.fill_rect(214, 24, 13, 11)
    graphics.rect(225, 24, 13, 11)
    display.pen(15)
    display.thickness(1)
    display.font("bitmap8")
    display.text("10", 217, 26, 0.1)
    display.pen(0)
    display.text("5", 230, 26, 0.1)

    # duration indicator manual
    display.pen(0)
    graphics.rect(241, 24, 36, 11)
    display.thickness(1)
    display.font("bitmap8")
    display.pen(0)
    display.text("manual", 245, 26, 0.1)

    # bar length indicator section
    display.pen(0)
    display.thickness(1)
    display.font("bitmap8")
    display.text(str(round(bar_length) )+" s", 280, 120, MENU_TEXT_SIZE)
    # start button section
    display.rectangle(137, 116, 38, 12) # start button rectangle
    display.pen(15) # inverse pen to white
    display.thickness(1) # ensure thinkness of pen is 1
    display.font("bitmap8") # set font to bitmap for readability small size
    display.text("start", 144, 118, 0.7) # start button text
    display.font("sans") # return to default font, maybe change this to font selection at start of each function
    #display.update()

# Draw the menu on the righthand side
def draw_focus_menu():
    display.font("bitmap8")
    display.thickness(1)
    for i in range(len(FOCUS_DURATION)):
        focus0, time0_red, time0_orange = FOCUS_DURATION[i]
        display.pen(0)
        if i == state["selected_activity"]:
            display.rectangle((MENU_PADDING - 5), i * MENU_SPACING, MENU_WIDTH, MENU_SPACING)
            display.pen(15)

        display.text(focus0, MENU_PADDING, (i * MENU_SPACING) + int((MENU_SPACING - 8) / 2), MENU_TEXT_SIZE)
        focus0, time0_red, time0_orange = ACTIVITY_DURATION[state["selected_activity"]]
        time0_m = int(time0_red) / 60
        time0_m_r= str(round(time0_m))
        display.pen(15)
        display.rectangle(75, 45, 75, 25)
        display.pen(0)
        display.thickness(1)
        display.text(time0_m_r +" mins", 80, 50, 2)
    focus0, time0_red, time0_orange = ACTIVITY_DURATION[state["selected_activity"]]
    display.thickness(1)
    display.update()

# Convert time in timer.txt from seconds to minutes as string
def calculate_focus_time():
    time1_m = int(time1) / 60
    time1_m_r= str(round(time1_m))
    return focus_time


def draw_light_red():
    display.pen(0)
    display.thickness(2) # nice fat pie and lines
    graphics.circle(47, 22, 20) # red outline
    graphics.fill_circle(47, 22, 15) # red fill, enable to indicate RED LIGHT
    graphics.fill_triangle(15, 28, 15, 16, 20, 22) # arrow
    graphics.fill_rect(5, 20, 10, 5) # arrow
    display.pen(15)
    #graphics.triangle(10, 27, 10, 17, 20, 22)
    display.pen(15) # disable for non-fill letter
    display.font("sans")
    display.thickness(1)
    display.text("R", 40, 22, 0.7)

def draw_light_orange():
    display.pen(0)
    display.thickness(2) # nice fat pie and lines
    graphics.circle(47, 64, 20) # orange outline
    #graphics.fill_circle(47, 64, 15) # orange fill, enable to indicate ORANGE LIGHT
    #display.pen(15) # disable for non-fill letter
    display.font("sans")
    display.thickness(1)
    display.text("O", 40, 64, 0.7)

def draw_light_green():
    display.pen(0)
    display.thickness(2) # nice fat pie and lines
    graphics.circle(47, 106, 20) # green outline
    #graphics.fill_circle(47, 106, 15) # green fill
    #display.pen(15) # disable for non-fill letter
    display.font("sans")
    display.thickness(1)
    display.text("G", 40, 105, 0.7)


# slices

display.pen(0)

def draw_6slices():
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 93, 266, 83, 266, 103) # 6 fill
    display.pen(15)
    graphics.triangle(246, 93, 266, 83, 266, 103) # 6 outline +200x

def draw_5slices():
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    display.thickness(2) # nice fat pie and lines
    graphics.fill_triangle(246, 113, 246, 93, 266, 103) # 5 fill +200x
    display.pen(15)
    graphics.triangle(246, 113, 246, 93, 266, 103) # 5 outline +200x

def draw_4slices():
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    display.thickness(2) # nice fat pie and lines
    graphics.fill_triangle(266, 123, 246, 113, 266, 103) # 4 fill +200x
    display.pen(15)
    graphics.triangle(266, 123, 246, 113, 266, 103) # 4 outline

def draw_3slices():
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    display.thickness(2) # nice fat pie and lines
    graphics.fill_triangle(286, 113, 266, 123, 266, 103) # 3 fill +200x
    display.pen(15)
    graphics.triangle(286, 113, 266, 123, 266, 103) # 3 outline +200x

def draw_2slices():
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    display.thickness(2) # nice fat pie and lines
    graphics.fill_triangle(286, 93, 286, 113, 266, 103) # 2 fill
    display.pen(15)
    graphics.triangle(286, 93, 286, 113, 266, 103) # 2 outline +200x

def draw_1slice():
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    display.thickness(2) # nice fat pie and lines
    graphics.fill_triangle(266, 83, 286, 93, 266, 103) # 1 fill +200x
    display.pen(15)
    graphics.triangle(266, 83, 286, 93, 266, 103) # 1 outline +200x






draw_focus_framework()
draw_light_red()
draw_light_orange()
draw_light_green()

draw_6slices()
draw_5slices()
draw_4slices()
draw_3slices()
draw_2slices()
draw_1slice()

# remaining time
display.pen(0)
display.text(str(updated_timer), 190, 102, 1)
display.thickness(1)
display.font("bitmap8")
display.text("mins nog", 192, 120, 0.55)


display.update()
display.led(0)

