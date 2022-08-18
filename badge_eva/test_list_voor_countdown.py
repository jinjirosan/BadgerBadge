# Badge Platform Eva - hardware platform v3.0
# (2022) Voor m'n lieve guppie
#
# test_countdown.py : v3.0-refactor 0.4 (cleanup)

import binascii
import badger2040
import badger_os
import time
import machine

# Default title and key/value file
TIMER_TITLE = "Wat moet ik doen?"
TIMER_FILE = "timer.txt"

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

ARROW_THICKNESS = 3
ARROW_WIDTH = 18
ARROW_HEIGHT = 14
ARROW_PADDING = 2

MAX_ITEM_CHARS = 26
TITLE_TEXT_SIZE = 0.7
ITEM_TEXT_SIZE = 0.6
ITEM_SPACING = 20

LIST_START = 40
LIST_PADDING = 2
LIST_WIDTH = WIDTH - LIST_PADDING - LIST_PADDING - ARROW_WIDTH
LIST_HEIGHT = HEIGHT - LIST_START - LIST_PADDING - ARROW_HEIGHT

TITLE_SIZE = 0.68
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

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_TURBO)
display.font("sans")

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

# List items taken from timer.txt 
activity_list_items = [activity1, activity2, activity3, activity4, activity5, activity6]
activity_list_times = [time1, time2, time3, time4, time5, time6]
save_checklist = False
activity_iter = iter(activity_list_items)
activity_select = 0

# temporary activity as placeholder for menu function
activity0 = 0
time0 = 0

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
    time1_m = int(time1) / 6
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
    display.text(activity_select, 5, 28, ACTIVITY_TEXT_SIZE)
    time0_m = int(time0) / 60
    time0_m_r= str(round(time0_m))
    display.text(time0_m_r +" mins", 180, 28, ACTIVITY_TEXT_SIZE)
    #display.text(str(round(time1_m)), 180, 50, TIME_TEXT_SIZE)
    display.thickness(2)
    display.update()

# Draw the timer, including user text
def draw_timer():
    display.pen(0)
    display.clear()

    # Draw activity image
    #display.image(BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)

    # Draw a border around the image
    #display.pen(0)
    #display.thickness(1)
    #display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    #display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    #display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    #display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    # Draw the company
    display.pen(15)  # Change this to 0 if a white background is used
    display.font("sans")
    display.thickness(2)
    display.text(activity1, LEFT_PADDING, (COMPANY_HEIGHT // 2) + 1, COMPANY_TEXT_SIZE)

    # Draw a white background behind the name
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)

    # Draw the name, scaling it based on the available width
    display.pen(0)
    display.font("sans")
    display.thickness(3)
    name_size = 2.0  # A sensible starting scale
    while True:
        name_length = display.measure_text(name, name_size)
        if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(name, (TEXT_WIDTH - name_length) // 2, (NAME_HEIGHT // 2) + COMPANY_HEIGHT + 1, name_size)
            break

    # Draw a white backgrounds behind the details
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT * 2, TEXT_WIDTH, DETAILS_HEIGHT - 1)
    display.rectangle(1, HEIGHT - DETAILS_HEIGHT, TEXT_WIDTH, DETAILS_HEIGHT - 1)

    # Draw the first detail's title and text
    display.pen(0)
    display.font("sans")
    display.thickness(3)
    name_length = display.measure_text(detail1_title, DETAILS_TEXT_SIZE)
    display.text(detail1_title, LEFT_PADDING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)
    display.thickness(2)
    display.text(detail1_text, 5 + name_length + DETAIL_SPACING, HEIGHT - ((DETAILS_HEIGHT * 3) // 2), DETAILS_TEXT_SIZE)

    # Draw the second detail's title and text
    display.thickness(3)
    name_length = display.measure_text(detail2_title, DETAILS_TEXT_SIZE)
    display.text(detail2_title, LEFT_PADDING, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)
    display.thickness(2)
    display.text(detail2_text, LEFT_PADDING + name_length + DETAIL_SPACING, HEIGHT - (DETAILS_HEIGHT // 2), DETAILS_TEXT_SIZE)


def countdown(time_sec):
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
#        display.partial_update(100,40,100,40)
        display.update()
    print("stoppppp")
    display.pen(0)
    display.rectangle(100, 45, 100, 30)
    display.pen(15)
    display.text("KLAAR", 100, 60, TIME_TEXT_SIZE)
    display.update()

# Draw upward arrow
def draw_up(x, y, width, height, thickness, padding):
    border = (thickness // 4) + padding
    display.line(x + border, y + height - border,
                 x + (width // 2), y + border)
    display.line(x + (width // 2), y + border,
                 x + width - border, y + height - border)


# Draw downward arrow
def draw_down(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(x + border, y + border,
                 x + (width // 2), y + height - border)
    display.line(x + (width // 2), y + height - border,
                 x + width - border, y + border)



# ------------------------------
#        Program setup
# ------------------------------

changed = not badger2040.woken_by_button()
state = {
    "current_item": 0,
}
badger_os.state_load("list", state)
state["current_item"] = 0

# Global variables
items_per_page = 0

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
display.led(128)
if changed:
    display.update_speed(badger2040.UPDATE_FAST)
else:
    display.update_speed(badger2040.UPDATE_TURBO)

## Find out what the longest item is
#longest_item = 0
#for i in range(len(activity_list_items)):
#    while True:
#        item = activity_list_items[i]
#        item_length = display.measure_text(item, ITEM_TEXT_SIZE)
#        if item_length > 0 and item_length > LIST_WIDTH - ITEM_SPACING:
#            activity_list_items[i] = item[:-1]
#        else:
#            break
#    longest_item = max(longest_item, display.measure_text(activity_list_items[i], ITEM_TEXT_SIZE))
#
#
## And use that to calculate the number of columns we can fit onscreen and how many items that would give
#list_columns = 1
#while longest_item + ITEM_SPACING < (LIST_WIDTH // (list_columns + 1)):
#    list_columns += 1
#
#items_per_page = ((LIST_HEIGHT // ITEM_SPACING) + 1) * list_columns


# ------------------------------
#       Main program loop
# ------------------------------

while True:
    if len(activity_list_items) > 0:
        if display.pressed(badger2040.BUTTON_A):
            display.pen(15)
            display.text("button A", 30, 50, 0.4)
            changed = True
            
        if display.pressed(badger2040.BUTTON_B):
            display.pen(15)
            display.text("button A", 30, 50, 0.4)
            changed = True
            
        if display.pressed(badger2040.BUTTON_C):    
            print(activity_list_items.index(activity_select))
            activity_list_times_pos = activity_list_items.index(activity_select)
            print(activity_list_times_pos)
            print(time0)
            time0 = activity_list_times[activity_list_times_pos]
            print(time0)
            draw_timer_framework()
            display.led(0)
            countdown(int(time0))
            
        if display.pressed(badger2040.BUTTON_UP):
            if state["current_item"] > 0:
                state["current_item"] -= 1
                changed = True

                
        if display.pressed(badger2040.BUTTON_DOWN):
            if state["current_item"] < len(activity_list_items) - 1:
                state["current_item"] += 1
                changed = True

                activity_select = next(activity_iter)
                

    if changed:
        badger_os.state_save("list", state)

        display.pen(15)
        display.clear()

        display.pen(12)
        display.rectangle(WIDTH - ARROW_WIDTH, 0, ARROW_WIDTH, HEIGHT)
        display.rectangle(0, HEIGHT - ARROW_HEIGHT, WIDTH, ARROW_HEIGHT)

        y = LIST_PADDING + 12
        display.pen(0)
        display.thickness(3)
        display.text(TIMER_TITLE, LIST_PADDING, y, TITLE_TEXT_SIZE)

        y += 12
        display.pen(0)
        display.thickness(2)
        display.line(LIST_PADDING, y, WIDTH - LIST_PADDING - ARROW_WIDTH, y)

        if len(activity_list_items) > 0:
            page_item = 0
            if items_per_page > 0:
                page_item = (state["current_item"] // items_per_page) * items_per_page

            # Draw the interaction button icons
            display.pen(0)
            display.thickness(ARROW_THICKNESS)

            # Previous item
            if state["current_item"] > 0:
                draw_up(WIDTH - ARROW_WIDTH, (HEIGHT // 4) - (ARROW_HEIGHT // 2),
                        ARROW_WIDTH, ARROW_HEIGHT, ARROW_THICKNESS, ARROW_PADDING)
                display.pen(15)
                display.rectangle(50, 45, 180, 30)
                display.pen(0)
                display.thickness(2)
                display.text(str(activity_select), 50, 60, 0.5)
                #display.update() 

            # Next item
            if state["current_item"] < (len(activity_list_items) - 1):
                draw_down(WIDTH - ARROW_WIDTH, ((HEIGHT * 3) // 4) - (ARROW_HEIGHT // 2),
                          ARROW_WIDTH, ARROW_HEIGHT, ARROW_THICKNESS, ARROW_PADDING)
                display.pen(15)
                display.rectangle(50, 45, 180, 30)
                display.pen(0)
                display.thickness(2)
                display.text(str(activity_select), 50, 60, 0.5)
                #display.update()              
                

        else:
            # Say that the list is empty
            empty_text = "Nothing Here"
            text_length = display.measure_text(empty_text, ITEM_TEXT_SIZE)
            display.text(empty_text, ((LIST_PADDING + LIST_WIDTH) - text_length) // 2, (LIST_HEIGHT // 2) + LIST_START - (ITEM_SPACING // 4), ITEM_TEXT_SIZE)

        display.update()
        display.update_speed(badger2040.UPDATE_TURBO)
        changed = False
        display.led(0)
        print(activity_select)

    display.halt()

