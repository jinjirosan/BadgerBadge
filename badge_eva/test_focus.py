# Badge Platform Eva - hardware platform v3.0
# (2022) Voor m'n lieve guppie
#
# focus.py : v3.0-refactor 0.1

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


# State of draw_slices functions to enable the "run once"
draw_6slices_run_once = False
draw_5slices_run_once = False
draw_4slices_run_once = False
draw_3slices_run_once = False
draw_2slices_run_once = False
draw_1slice_run_once = False

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
    graphics.fill_rect(100, 24, 13, 11)
    graphics.rect(111, 24, 13, 11)
    display.pen(15)
    display.thickness(1)
    display.font("bitmap8")
    display.text("60", 102, 26, 0.1)
    display.pen(0)
    display.text("30", 113, 26, 0.1)

    # duration indicator 30-15
    display.pen(0)
    graphics.fill_rect(127, 24, 13, 11)
    graphics.rect(138, 24, 13, 11)
    display.pen(15)
    display.thickness(1)
    display.font("bitmap8")
    display.text("30", 129, 26, 0.1)
    display.pen(0)
    display.text("15", 141, 26, 0.1)
    
    # duration indicator 10-5
    display.pen(0)
    graphics.fill_rect(154, 24, 13, 11)
    graphics.rect(165, 24, 13, 11)
    display.pen(15)
    display.thickness(1)
    display.font("bitmap8")
    display.text("10", 157, 26, 0.1)
    display.pen(0)
    display.text("5", 170, 26, 0.1)
    
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
display.text("mins over", 190, 120, 0.55)


display.update()
display.led(0)

