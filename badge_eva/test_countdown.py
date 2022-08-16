# Badge Platform Eva - hardware platform v3.0
# (2022) Voor m'n lieve guppie
#
# test_countdown.py : v3.0-refactor 0.1

import time
import machine
import badger2040


TITLE_SIZE = 0.68
ACTIVITY_HEIGHT = 30
TIME_HEIGHT = 20
ACTIVITY_TEXT_SIZE = 0.57
TIME_TEXT_SIZE = 1.0
LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

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
time1 = badge.readline()      # "15"
activity2 = badge.readline()  # "ontbijt"
time2 = badge.readline()      # "16"
activity3 = badge.readline()  # "schoenen"
time3 = badge.readline()      # "5"
activity4 = badge.readline()  # "douchen"
time4 = badge.readline()      # "20"
activity5 = badge.readline()  # "pootjes wassen"
time5 = badge.readline()      # "12"
activity6 = badge.readline()  # "pyama"
time6 = badge.readline()      # "7"

# List items taken from timer.txt 
activity_list_items = [activity1, activity2, activity3, activity4, activity5, activity6]
save_checklist = False

# temporary activity as placeholder for menu function
activity0 = activity1
time0 = time1

# time is in secs
DEFAULT_TEXT = """aankleden
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

# Slow down the system while badge is using the countdown function
badger2040.system_speed(badger2040.SYSTEM_SLOW)

rtc = machine.RTC()

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_TURBO)
display.font("sans")

# Buttons
button_down = machine.Pin(badger2040.BUTTON_DOWN, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_up = machine.Pin(badger2040.BUTTON_UP, machine.Pin.IN, machine.Pin.PULL_DOWN)

button_a = machine.Pin(badger2040.BUTTON_A, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_b = machine.Pin(badger2040.BUTTON_B, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_c = machine.Pin(badger2040.BUTTON_C, machine.Pin.IN, machine.Pin.PULL_DOWN)

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
    display.text(activity0, 5, 28, ACTIVITY_TEXT_SIZE)
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



# Truncate all of the text (except for the name as that is scaled)
#company = truncatestring(company, COMPANY_TEXT_SIZE, TEXT_WIDTH)

#detail1_title = truncatestring(detail1_title, DETAILS_TEXT_SIZE, TEXT_WIDTH)
#detail1_text = truncatestring(detail1_text, DETAILS_TEXT_SIZE,
#                              TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail1_title, DETAILS_TEXT_SIZE))

#detail2_title = truncatestring(detail2_title, DETAILS_TEXT_SIZE, TEXT_WIDTH)
#detail2_text = truncatestring(detail2_text, DETAILS_TEXT_SIZE,
#                              TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail2_title, DETAILS_TEXT_SIZE))


draw_timer_framework()

display.led(0)
# display.halt()
countdown(int(time1))


#while True:
#    countdown()
#    time.sleep(10)

