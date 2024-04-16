# Badge Platform Eva - hardware platform v3.0
# (2022-2024) Voor m'n lieve guppie
#
# badge.py : v2.4-refactor 0.0.1

import time
import badger2040
import badger_os
import os
from machine import UART
from machine import Pin

# Initialize serial Port
lora = UART(0,baudrate = 9600,tx = Pin(0),rx = Pin(1))

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

IMAGE_WIDTH = 104

COMPANY_HEIGHT = 30
DETAILS_HEIGHT = 20
NAME_HEIGHT = HEIGHT - COMPANY_HEIGHT - (DETAILS_HEIGHT * 2) - 2
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1

COMPANY_TEXT_SIZE = 0.6
DETAILS_TEXT_SIZE = 0.5

LEFT_PADDING = 5
NAME_PADDING = 20
DETAIL_SPACING = 10

DEFAULT_TEXT = """mustelid inc
H. Badger
RP2040
2MB Flash
E ink
296x128px"""

# Time delay in seconds between consecutive button press checks
BUTTON_PRESS_DELAY = 0.2

# Flag to keep track of which badge image to display
is_qr_image = False

# Global variable to keep track of the current image file
current_image_file = "badge-image.bin"

# Set needs_update to True initially to trigger the first draw
needs_update = True


# Load the badge images
#BADGE_IMAGE = bytearray(int(IMAGE_WIDTH * HEIGHT / 8))
#BADGE_IMAGE_QR = bytearray(int(IMAGE_WIDTH * HEIGHT / 8))
def load_image(filename):
    try:
        with open(filename, "rb") as file:
            return bytearray(file.read())
    except OSError:
        return None

BADGE_IMAGE = load_image("badge-image.bin") or bytearray(int(IMAGE_WIDTH * HEIGHT / 8))
BADGE_IMAGE_QR = load_image("badge-image_QR.bin") or None

# Load the initial badge image
CURRENT_BADGE_IMAGE = BADGE_IMAGE

# ------------------------------
#      Utility functions
# ------------------------------

# Reduce the size of a string until it fits within a given width
def truncatestring(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text

# Function to toggle between badge images, now improved to handle image switching correctly
def toggle_badge_image():
    global CURRENT_BADGE_IMAGE, current_image_file, needs_update

    print(f"Current image before toggle: {current_image_file}")
    if "_QR" in current_image_file:
        new_image_file = "badge-image.bin"
    else:
        new_image_file = "badge-image_QR.bin"

    print(f"Attempting to load image from: {new_image_file}")
    new_image = load_image(new_image_file)
    if new_image:
        CURRENT_BADGE_IMAGE = new_image
        current_image_file = new_image_file
        print(f"Switched to image: {new_image_file}")
        needs_update = True  # Set the flag indicating the display needs to be updated
    else:
        print("Failed to load image:", new_image_file)


def is_on_battery():
    # This needs to be replaced with your specific method to detect battery power.
    return not os.uname().machine.startswith("USB")

def turn_on_led():
    display.led(128)  # Set LED brightness to mid-level

def turn_off_led():
    display.led(0)    # Turn off the LED


# ------------------------------
#      Drawing functions
# ------------------------------

# Draw the badge, including user text
def draw_badge():
    try:
        display.pen(0)
        display.clear()
        display.image(CURRENT_BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)

        # Draw badge image
        display.image(CURRENT_BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)

        # Draw a border around the image
        display.pen(0)
        display.thickness(1)
        display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
        display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
        display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
        display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

        # Draw the company
        display.pen(15)  # Change this to 0 if a white background is used
        display.font("sans")
        display.thickness(2)
        display.text(company, LEFT_PADDING, (COMPANY_HEIGHT // 2) + 1, COMPANY_TEXT_SIZE)

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
 
        # Draw button C QR label
        display.pen(0)
        display.font("sans")
        display.thickness(1)
        display.rectangle(271, 118, 20, 10)
        display.pen(15)
        display.text("QR", 273, 122, 0.4)
        display.pen(0)
 
        display.update()  # Ensure initial update happens here
        print("Badge drawn successfully.")
    except Exception as e:
        print("Failed to draw badge:", str(e))

    finally:
        turn_off_led()  # Ensure the LED is turned off after drawing

# ------------------------------
#        Sigfox functions
# ------------------------------

def SigfoxInfo():        
    sf_info = dict();
    print("Get Status - should be OK")
    lora.write("AT\r\n")      # Write AT Command
    time.sleep(2)
    sf_status = lora.read(2)         # Response Should be OK
    sf_info['Status'] = sf_status
    print(sf_status)

    print("Get ID")
    lora.write("AT$I=10\r\n") # Send Command to Get ID
    time.sleep(2)
    sf_id = lora.read(10)
    sf_info['ID'] = sf_id
    print(sf_id)

    print("Get PAC")
    lora.write("AT$I=11\r\n") # Send Command to Get ID
    time.sleep(2)
    sf_pac = lora.read(18)
    sf_info['PAC'] = sf_pac
    print(sf_pac)
    
    return sf_info
    
def SigfoxSend():
    try:
        # Turn on LED to indicate that the Sigfox communication is starting
        display.led(128)
        print("Initiating Sigfox Transmission...")

        # Your existing Sigfox communication code
        lora.write("AT$RC\r\n")  # Example command to reset channels
        time.sleep(2)
        data = lora.read(4)
        print(data)

        lora.write("AT$SF=AABBCCDD\r\n")  # Example send command
        time.sleep(6)
        data = lora.read(4)
        print(data)

        print("Sigfox message sent successfully.")
    except Exception as e:
        print("Failed to send Sigfox message:", str(e))
    finally:
        # Turn off LED to indicate that the Sigfox communication has finished
        display.led(0)



# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# Open the badge file
try:
    badge = open("badge.txt", "r")
except OSError:
    with open("badge.txt", "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    badge = open("badge.txt", "r")

# Read in the next 6 lines
company = badge.readline()        # "mustelid inc"
name = badge.readline()           # "H. Badger"
detail1_title = badge.readline()  # "RP2040"
detail1_text = badge.readline()   # "2MB Flash"
detail2_title = badge.readline()  # "E ink"
detail2_text = badge.readline()   # "296x128px"

# Truncate all of the text (except for the name as that is scaled)
company = truncatestring(company, COMPANY_TEXT_SIZE, TEXT_WIDTH)

detail1_title = truncatestring(detail1_title, DETAILS_TEXT_SIZE, TEXT_WIDTH)
detail1_text = truncatestring(detail1_text, DETAILS_TEXT_SIZE,
                              TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail1_title, DETAILS_TEXT_SIZE))

detail2_title = truncatestring(detail2_title, DETAILS_TEXT_SIZE, TEXT_WIDTH)
detail2_text = truncatestring(detail2_text, DETAILS_TEXT_SIZE,
                              TEXT_WIDTH - DETAIL_SPACING - display.measure_text(detail2_title, DETAILS_TEXT_SIZE))

# Draw the badge initially and set up any necessary flags
try:
    if needs_update:
        draw_badge()  # Draw the badge initially
        needs_update = False  # Reset flag after initial draw
except Exception as e:
    print("Error during initial drawing:", str(e))

# initiate a hidden SigFox ping when the badge is started
SigfoxSend()

# ------------------------------
#       Main program
# ------------------------------

while True:
    if display.pressed(badger2040.BUTTON_C):
        toggle_badge_image()
        time.sleep(BUTTON_PRESS_DELAY)  # Prevent debouncing issues

    if needs_update:
        draw_badge()
        needs_update = False  # Reset update flag after drawing

    if not is_on_battery():
        display.halt()  # Power management


