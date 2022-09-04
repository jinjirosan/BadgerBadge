# Badge Platform Eva - hardware platform v3.0
# (2022) Voor m'n lieve guppie
#
# focus.py : v3.0-refactor 0.6

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
focus_setting4 = badge.readline()  # "Manual"
time4_red = badge.readline()       # "600" : 10mins
time4_orange = badge.readline()    # "300" : 5mins

# Global variables
FOCUS_DURATION = (
    (focus_setting1, time1_red, time1_orange),
    (focus_setting2, time2_red, time2_orange),
    (focus_setting3, time3_red, time3_orange),
    (focus_setting4, time4_red, time4_orange)
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

# state of the traffic light
draw_light_red_fill = False
draw_light_orange_fill = False
draw_light_green_fill = False

# List items taken from focus.txt 
focus_list_items = [focus_setting1, focus_setting2, focus_setting3, focus_setting4]
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
time0 = 0 # remove this one from functions or use for single timer code
slice_duration = 600


MENU_TEXT_SIZE = 0.5
MENU_SPACING = 10
MENU_WIDTH = 84
MENU_PADDING = 220  # Number of pixels between lefthandside and menu

display.update_speed(badger2040.UPDATE_FAST) # first draw is normal to get everything nice and sharp

# Draw the focus framework
def draw_focus_framework():
#     display.update_speed(badger2040.UPDATE_FAST)
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
    
    # Draw the trafficlight
    draw_light_red()
    draw_light_orange()
    draw_light_green()

    display.update()

# Draw the menu
def draw_focus_menu():
    display.font("bitmap8")
    display.thickness(1)
    for i in range(len(FOCUS_DURATION)):
        focus0, time0_red, time0_orange = FOCUS_DURATION[i]
        display.pen(0)
        if i == state["selected_focus"]:
            display.rectangle((MENU_PADDING - 5), (i * MENU_SPACING) + 40, MENU_WIDTH, MENU_SPACING)
            display.pen(15)

        display.text(focus0, MENU_PADDING, ((i * MENU_SPACING) + int((MENU_SPACING - 8) / 2)) + 40, MENU_TEXT_SIZE)
        focus0, time0_red, time0_orange = FOCUS_DURATION[state["selected_focus"]]
        
        print(focus0)
        print(time0_red)
        print(time0_orange)
        
        if state["selected_focus"] == 0:
            draw_focus_setting1()        
        if state["selected_focus"] == 1:
            draw_focus_setting2()
        if state["selected_focus"] == 2:
            draw_focus_setting3()            
        if state["selected_focus"] == 3:
            draw_focus_setting4()
    
    focus0, time0_red, time0_orange = FOCUS_DURATION[state["selected_focus"]]
    
    display.thickness(1)

    # start button section
    display.rectangle(242, 116, 38, 12) # start button rectangle
    display.pen(15) # inverse pen to white
    display.thickness(1) # ensure thinkness of pen is 1
    display.font("bitmap8") # set font to bitmap for readability small size
    display.text("start", 249, 118, 0.7) # start button text +7px
    display.font("sans") # return to default font, maybe change this to font selection at start of each function

    display.update()  # enable later when all functions are defined

# Convert time in focus.txt from seconds to minutes as string
def calculate_focus_time():
    time1_m = int(time1) / 60
    time1_m_r= str(round(time1_m))
    return focus_time


def draw_light_red():
    if draw_light_red_fill:
        display.pen(0)
        display.thickness(2) # nice fat pie and lines
        graphics.fill_triangle(15, 28, 15, 16, 20, 22) # arrow
        graphics.fill_rect(5, 20, 10, 5) # arrow
        graphics.circle(47, 22, 20) # red outline
        graphics.fill_circle(47, 22, 15) # red fill, enable to indicate RED LIGHT
        display.pen(15)
        display.font("sans")
        display.thickness(1)
        display.text("R", 40, 22, 0.7)
        return
    display.pen(0)
    display.thickness(2) # nice fat pie and lines
    graphics.circle(47, 22, 20) # red outline
    display.font("sans")
    display.thickness(1)
    display.text("R", 40, 22, 0.7)

def draw_light_orange():
    if draw_light_orange_fill:
        display.pen(0)
        display.thickness(2) # nice fat pie and lines
        graphics.fill_triangle(15, 68, 15, 56, 20, 62) # arrow
        graphics.fill_rect(5, 60, 10, 5) # arrow
        graphics.circle(47, 64, 20) # orange outline
        graphics.fill_circle(47, 64, 15) # orange fill, enable to indicate ORANGE LIGHT
        display.pen(15) # disable for non-fill letter
        display.font("sans")
        display.thickness(1)
        display.text("O", 40, 64, 0.7)
        return
    display.pen(0)
    display.thickness(2) # nice fat pie and lines
    graphics.circle(47, 64, 20) # orange outline
    #graphics.fill_circle(47, 64, 15) # orange fill, enable to indicate ORANGE LIGHT
    #display.pen(15) # disable for non-fill letter
    display.font("sans")
    display.thickness(1)
    display.text("O", 40, 64, 0.7)
        
def draw_light_green():
    if draw_light_green_fill:
        display.pen(0)
        display.thickness(2) # nice fat pie and lines
        graphics.fill_triangle(15, 113, 15, 101, 20, 107) # arrow
        graphics.fill_rect(5, 105, 10, 5) # arrow rectangle
        graphics.circle(47, 106, 20) # green outline
        graphics.fill_circle(47, 106, 15) # green fill
        display.pen(15) # disable for non-fill letter
        display.font("sans")
        display.thickness(1)
        display.text("G", 40, 105, 0.7)
        return
    display.pen(0)
    display.thickness(2) # nice fat pie and lines
    graphics.circle(47, 106, 20) # green outline
    display.font("sans")
    display.thickness(1)
    display.text("G", 40, 105, 0.7)

def draw_focus_setting1():
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

def draw_focus_setting2():
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

def draw_focus_setting3():
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
    
def draw_focus_setting4():
    # duration indicator manual
    display.pen(0)
    graphics.rect(241, 24, 36, 11)
    display.thickness(1)
    display.font("bitmap8")
    display.pen(0)
    display.text("manual", 245, 26, 0.1)

# Calculate the duration each slice needs to represent
def calculate_slice_length(total_slices, focus_time):
    slice_duration = focus_time / total_slices
    d0 = [(i * slice_duration, (i + 1) * slice_duration) for i in range(total_slices)]
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


# slices

def draw_6slices():
    global draw_6slices_run_once
    if draw_6slices_run_once:
        return
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 93, 266, 83, 266, 103) # 6 fill
    display.pen(15)
    graphics.triangle(246, 93, 266, 83, 266, 103) # 6 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice

    graphics.fill_triangle(246, 113, 246, 93, 266, 103) # 5 fill
    display.pen(15)
    graphics.triangle(246, 113, 246, 93, 266, 103) # 5 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice

    graphics.fill_triangle(266, 123, 246, 113, 266, 103) # 4 fill
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
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice

    graphics.fill_triangle(266, 83, 286, 93, 266, 103) # 1 fill +200x
    display.pen(15)
    graphics.triangle(266, 83, 286, 93, 266, 103) # 1 outline +200x 

    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(185, 86, 52, 30)
    display.pen(0)

    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("6slices_time0", time0)
    print("updated_timer", updated_timer)
    # remaining time
    display.pen(0)
    display.font("sans")
    display.text(str(updated_timer), 190, 102, 1)
    display.thickness(1)
    display.font("bitmap8")
    display.text("mins nog", 192, 120, 0.55)
    
    # bar length indicator section
    display.pen(0)
    display.thickness(1)
    display.font("bitmap8")
    display.text(str(round(slice_duration) )+" s", 273, 120, MENU_TEXT_SIZE)
    
    #display.update()   # enable when function while loop is active
    draw_6slices_run_once = True

def draw_5slices():
    global draw_5slices_run_once
    if draw_5slices_run_once:
        return
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 93, 266, 83, 266, 103) # 6 fill
    display.pen(15)
    graphics.triangle(246, 93, 266, 83, 266, 103) # 6 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 113, 246, 93, 266, 103) # 5 fill
    display.pen(15)
    graphics.triangle(246, 113, 246, 93, 266, 103) # 5 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(266, 123, 246, 113, 266, 103) # 4 fill
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

    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(185, 86, 52, 30)
    display.pen(0)

    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("6slices_time0", time0)
    print("updated_timer", updated_timer)
    # remaining time
    display.pen(0)
    display.font("sans")
    display.text(str(updated_timer), 190, 102, 1)
    display.thickness(1)
    display.font("bitmap8")
    display.text("mins nog", 192, 120, 0.55)
    
    # bar length indicator section
    display.pen(0)
    display.thickness(1)
    display.font("bitmap8")
    display.text(str(round(slice_duration) )+" s", 273, 120, MENU_TEXT_SIZE)
    
    #display.update()   # enable when function while loop is active
    draw_5slices_run_once = True

def draw_4slices():
    global draw_4slices_run_once
    if draw_4slices_run_once:
        return
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 93, 266, 83, 266, 103) # 6 fill
    display.pen(15)
    graphics.triangle(246, 93, 266, 83, 266, 103) # 6 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 113, 246, 93, 266, 103) # 5 fill
    display.pen(15)
    graphics.triangle(246, 113, 246, 93, 266, 103) # 5 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(266, 123, 246, 113, 266, 103) # 4 fill
    display.pen(15)
    graphics.triangle(266, 123, 246, 113, 266, 103) # 4 outline 
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(286, 113, 266, 123, 266, 103) # 3 fill +200x
    display.pen(15)
    graphics.triangle(286, 113, 266, 123, 266, 103) # 3 outline +200x
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(286, 93, 286, 113, 266, 103) # 2 fill
    display.pen(15)
    graphics.triangle(286, 93, 286, 113, 266, 103) # 2 outline +200x
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(266, 83, 286, 93, 266, 103) # 1 fill +200x
    display.pen(15)
    graphics.triangle(266, 83, 286, 93, 266, 103) # 1 outline +200x 
    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(185, 86, 52, 30)
    display.pen(0)

    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("6slices_time0", time0)
    print("updated_timer", updated_timer)
    # remaining time
    display.pen(0)
    display.font("sans")
    display.text(str(updated_timer), 190, 102, 1)
    display.thickness(1)
    display.font("bitmap8")
    display.text("mins nog", 192, 120, 0.55)
    
    # bar length indicator section
    display.pen(0)
    display.thickness(1)
    display.font("bitmap8")
    display.text(str(round(slice_duration) )+" s", 273, 120, MENU_TEXT_SIZE)
    
    #display.update()   # enable when function while loop is active
    draw_4slices_run_once = True

def draw_3slices():
    global draw_3slices_run_once
    if draw_3slices_run_once:
        return
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 93, 266, 83, 266, 103) # 6 fill
    display.pen(15)
    graphics.triangle(246, 93, 266, 83, 266, 103) # 6 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 113, 246, 93, 266, 103) # 5 fill
    display.pen(15)
    graphics.triangle(246, 113, 246, 93, 266, 103) # 5 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(266, 123, 246, 113, 266, 103) # 4 fill
    display.pen(15)
    graphics.triangle(266, 123, 246, 113, 266, 103) # 4 outline 
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(286, 113, 266, 123, 266, 103) # 3 fill +200x
    display.pen(15)
    graphics.triangle(286, 113, 266, 123, 266, 103) # 3 outline +200x
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(286, 93, 286, 113, 266, 103) # 2 fill
    display.pen(15)
    graphics.triangle(286, 93, 286, 113, 266, 103) # 2 outline +200x
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(266, 83, 286, 93, 266, 103) # 1 fill +200x
    display.pen(15)
    graphics.triangle(266, 83, 286, 93, 266, 103) # 1 outline +200x 
    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(185, 86, 52, 30)
    display.pen(0)

    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("6slices_time0", time0)
    print("updated_timer", updated_timer)
    # remaining time
    display.pen(0)
    display.font("sans")
    display.text(str(updated_timer), 190, 102, 1)
    display.thickness(1)
    display.font("bitmap8")
    display.text("mins nog", 192, 120, 0.55)
    
    # bar length indicator section
    display.pen(0)
    display.thickness(1)
    display.font("bitmap8")
    display.text(str(round(slice_duration) )+" s", 273, 120, MENU_TEXT_SIZE)
    
    #display.update()   # enable when function while loop is active
    draw_3slices_run_once = True

def draw_2slices():
    global draw_2slices_run_once
    if draw_2slices_run_once:
        return
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 93, 266, 83, 266, 103) # 6 fill
    display.pen(15)
    graphics.triangle(246, 93, 266, 83, 266, 103) # 6 outline
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 113, 246, 93, 266, 103) # 5 fill
    display.pen(15)
    graphics.triangle(246, 113, 246, 93, 266, 103) # 5 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(266, 123, 246, 113, 266, 103) # 4 fill
    display.pen(15)
    graphics.triangle(266, 123, 246, 113, 266, 103) # 4 outline 
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(286, 113, 266, 123, 266, 103) # 3 fill +200x
    display.pen(15)
    graphics.triangle(286, 113, 266, 123, 266, 103) # 3 outline +200x
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(286, 93, 286, 113, 266, 103) # 2 fill
    display.pen(15)
    graphics.triangle(286, 93, 286, 113, 266, 103) # 2 outline +200x
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(266, 83, 286, 93, 266, 103) # 1 fill +200x
    display.pen(15)
    graphics.triangle(266, 83, 286, 93, 266, 103) # 1 outline +200x 
    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(185, 86, 52, 30)
    display.pen(0)

    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("6slices_time0", time0)
    print("updated_timer", updated_timer)
    # remaining time
    display.pen(0)
    display.font("sans")
    display.text(str(updated_timer), 190, 102, 1)
    display.thickness(1)
    display.font("bitmap8")
    display.text("mins nog", 192, 120, 0.55)
    
    # bar length indicator section
    display.pen(0)
    display.thickness(1)
    display.font("bitmap8")
    display.text(str(round(slice_duration) )+" s", 273, 120, MENU_TEXT_SIZE)
    
    #display.update()   # enable when function while loop is active
    draw_2slices_run_once = True

def draw_1slice():
    global draw_1slice_run_once
    if draw_1slice_run_once:
        return
    display.thickness(2) # nice fat pie and lines
    display.pen(0) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 93, 266, 83, 266, 103) # 6 fill
    display.pen(15)
    graphics.triangle(246, 93, 266, 83, 266, 103) # 6 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(246, 113, 246, 93, 266, 103) # 5 fill
    display.pen(15)
    graphics.triangle(246, 113, 246, 93, 266, 103) # 5 outline
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(266, 123, 246, 113, 266, 103) # 4 fill
    display.pen(15)
    graphics.triangle(266, 123, 246, 113, 266, 103) # 4 outline 
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(286, 113, 266, 123, 266, 103) # 3 fill +200x
    display.pen(15)
    graphics.triangle(286, 113, 266, 123, 266, 103) # 3 outline +200x
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(286, 93, 286, 113, 266, 103) # 2 fill
    display.pen(15)
    graphics.triangle(286, 93, 286, 113, 266, 103) # 2 outline +200x
    display.pen(12) # use pen(12) for spent slice, pen(0) for full slice
    graphics.fill_triangle(266, 83, 286, 93, 266, 103) # 1 fill +200x
    display.pen(15)
    graphics.triangle(266, 83, 286, 93, 266, 103) # 1 outline +200x 
    # rectangle background for clear visibility of number
    display.pen(15)
    display.rectangle(185, 86, 52, 30)
    display.pen(0)

    time0_m = int(updated_timer) / 60
    time0_m_r= str(round(time0_m))
    print("6slices_time0", time0)
    print("updated_timer", updated_timer)
    # remaining time
    display.pen(0)
    display.font("sans")
    display.text(str(updated_timer), 190, 102, 1)
    display.thickness(1)
    display.font("bitmap8")
    display.text("mins nog", 192, 120, 0.55)
    
    # bar length indicator section
    display.pen(0)
    display.thickness(1)
    display.font("bitmap8")
    display.text(str(round(slice_duration) )+" s", 273, 120, MENU_TEXT_SIZE)
    
    #display.update()   # enable when function while loop is active
    draw_1slice_run_once = True



    ## <menu> button 'B' section
    #display.rectangle(137, 116, 38, 12) # start button rectangle
    #display.pen(15) # inverse pen to white
    #display.thickness(1) # ensure thinkness of pen is 1
    #display.font("bitmap8") # set font to bitmap for readability small size
    #display.text("menu", 144, 118, 0.7) # start button text
    #display.font("sans") # return to default font, maybe change this to font selection at start of each function
    #display.thickness(1)
    #display.update()

# The meat of the timer :-)
def countdown(time0):
    badger2040.system_speed(badger2040.SYSTEM_NORMAL)
    if state["selected_focus"] == 0:
        draw_focus_setting1()   
    if state["selected_focus"] == 1:
        draw_focus_setting2()
    if state["selected_focus"] == 2:
        draw_focus_setting3()   
    if state["selected_focus"] == 3:
        draw_focus_setting4()
    while time0:
        mins, secs = divmod(time0, 60)
        timeformat = '{:02d}:{:02d}'.format(mins,secs)
        print(timeformat, end='\r')
        #print("bar_length", bar_length)
        #print("time0", time0)
        display.led(255)
        if time0 > slice_duration * 5:
            global updated_timer
            updated_timer = mins
            draw_6slices()
        if time0 > slice_duration * 4 and time0 < bar_length * 5:
            global updated_timer
            updated_timer = mins
            draw_5slices()
        if time0 > slice_duration * 3 and time0 < bar_length * 4:
            updated_timer = mins
            draw_4slices()
        if time0 > slice_duration * 2 and time0 < bar_length * 3:
            updated_timer = mins
            draw_3slices()
        if time0 > slice_duration * 1 and time0 < bar_length * 2:
            updated_timer = mins
            draw_2slices()
        if time0  < slice_duration * 1:
            updated_timer = mins
            draw_1slice()        
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
        display.update()
    print("stoppppp")
    display.update_speed(badger2040.UPDATE_FAST)

    ## clear the minutes righthand side
    #display.pen(15)
    #display.rectangle(0, 45, 296, 83)
    #display.pen(0)
    #display.rectangle(100, 55, 112, 30)
    #display.pen(15)
    #display.thickness(2)
    #display.text("KLAAR", 100, 70, 1.2)
    display.update()


# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
graphics = gfx.GFX(296, 128, display.pixel)
display.led(128)

# Variable e-INK screen update speeds
changed = not badger2040.woken_by_button()

if changed:
    display.update_speed(badger2040.UPDATE_TURBO)
    badger2040.system_speed(badger2040.SYSTEM_TURBO)
else:
    display.update_speed(badger2040.UPDATE_FAST)
    badger2040.system_speed(badger2040.SYSTEM_NORMAL)

# system speed increased for activity menu. Slow down on countdown
#display.system_speed(badger2040.SYSTEM_FAST)
#badger2040.system_speed(badger2040.SYSTEM_FAST)

#display.pen(15)
#display.clear()
#display.update()

# ------------------------------
#       Main program loop
# ------------------------------


while True:
    if display.pressed(badger2040.BUTTON_UP):
        state["selected_focus"] -= 1
        if state["selected_focus"] < 0:
            state["selected_focus"] = len(FOCUS_DURATION) - 1
        changed = True
        
    if display.pressed(badger2040.BUTTON_DOWN):
        state["selected_focus"] += 1
        if state["selected_focus"] >= len(FOCUS_DURATION):
            state["selected_focus"] = 0
        changed = True

    if display.pressed(badger2040.BUTTON_C):    
        focus0, time0_red, time0_orange = FOCUS_DURATION[state["selected_focus"]]
        #time0_m = int(time0_red) / 60
        #time0_m_r= str(round(time0_m))
        #print(time0_m_r)
        print("time0_red " +time0_red)
        slice_duration, focus_time = calculate_slice_length(slice_duration,int(time0_red))
        draw_focus_framework()
        display.led(0)
        draw_light_red_fill = True
        draw_light_red()
        countdown(int(time0_red))
        draw_light_red_fill = False
        draw_light_orange_fill = True
        draw_light_orange()
        countdown(int(time0_orange))
        draw_light_green()

    if changed:
        draw_focus_framework()
        draw_focus_menu()
        badger_os.state_save("focusstate", state)
        print(state["selected_focus"])
        print(changed)
        changed = False
        display.led(0)

    display.halt()