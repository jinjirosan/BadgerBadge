# Badge Platform papa - hardware platform v3.0
# (2022-2024)
#
# help.py : v1.0-refactor 0.0.0

import badger2040
import time
import gfx

# Default title and key/value file
HELP_FILE = "help.txt"

# Open the help file
try:
    badge = open(HELP_FILE, "r")
except OSError:
    with open(HELP_FILE, "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open(HELP_FILE, "r")

# Read in the next 12 lines
contacts = [badge.readline().strip() for _ in range(12)]

# Pair names and numbers
contacts_pairs = [(contacts[i], contacts[i + 1]) for i in range(0, len(contacts), 2)]

# Global variables
WIDTH = badger2040.WIDTH # 296
HEIGHT = badger2040.HEIGHT # 128

MENU_TEXT_SIZE = 0.5
LEFT_PADDING = 5
PERSON_PADDING = 20  # Adjust this value to align person names properly
NUMBER_PADDING = 100  # Adjust this value to align numbers properly
TOP_PADDING = 15  # Adjust this value to align text vertically

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

# Draw the dashed line around the edges of the display
def draw_dashed_frame():
    display.pen(0)
    display.thickness(2)
    gap = 4
    length = 8
    for x in range(0, WIDTH, length + gap):
        display.line(x, 0, x + length, 0)  # Top border
        display.line(x, HEIGHT - 1, x + length, HEIGHT - 1)  # Bottom border
    for y in range(0, HEIGHT, length + gap):
        display.line(0, y, 0, y + length)  # Left border
        display.line(WIDTH - 1, y, WIDTH - 1, y + length)  # Right border

# Draw emergency contacts
def draw_contacts():
    display.pen(0)
    display.thickness(2)
    y_position = TOP_PADDING
    for person, number in contacts_pairs:
        display.text(person, PERSON_PADDING, y_position, MENU_TEXT_SIZE)
        display.text(number, NUMBER_PADDING, y_position, MENU_TEXT_SIZE)
        y_position += 20

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

# Main program loop
while True:
    if display.pressed(badger2040.BUTTON_UP):
        changed = True
        
    if display.pressed(badger2040.BUTTON_DOWN):
        changed = True

    if display.pressed(badger2040.BUTTON_C):    
        print("Button C pressed")

    if changed:
        display.pen(15)
        display.clear()
        draw_dashed_frame()
        draw_contacts()
        display.update()
        changed = False
        display.led(0)

    display.halt()
