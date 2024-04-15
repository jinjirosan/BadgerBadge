# Badge Platform Eva - hardware platform v3.0
# (2022-2024) Voor m'n lieve guppie
#
# badge.py : v2.2-refactor 0.2

import time
import badger2040
import badger_os
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
BADGE_IMAGE_QR = load_image("badge-image-QR.bin") or None

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

# Function to toggle between badge images
def toggle_badge_image():
    global is_qr_image, CURRENT_BADGE_IMAGE
    is_qr_image = not is_qr_image
    CURRENT_BADGE_IMAGE = BADGE_IMAGE_QR if is_qr_image else BADGE_IMAGE
    # Explicitly call the draw function here might help to ensure that changes are immediately reflected.
    draw_badge()



# ------------------------------
#      Drawing functions
# ------------------------------

# Draw the badge, including user text
def draw_badge():
    display.pen(0)
    display.clear()

    # Draw badge image
#    if is_qr_image:
#        # Draw QR code image
#        display.image(BADGE_IMAGE_QR, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)
#    else:
#        # Draw badge image
#        display.image(BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)

    # Draw badge image
    display.image(CURRENT_BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)

    # Draw a border around the image
    display.pen(0)
    display.thickness(1)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

    # Uncomment this if a white background is wanted behind the company
    # display.pen(15)
    # display.rectangle(1, 1, TEXT_WIDTH, COMPANY_HEIGHT - 1)

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
    # Initiate a Transmission
    print("Init Transmission")
    time.sleep(1)
    lora.write("AT$RC\r\n") # Send Command to Reset Macro Channels
    time.sleep(2)
    data=lora.read(4)
    print(data)
    lora.write("AT$SF=AABBCCDD\r\n")  # sends a test string "AABBCCDD"
    time.sleep(6)
    data=lora.read(4)        # We should get a OK response
    print(data)


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


# ------------------------------
#       Main program
# ------------------------------

draw_badge()

while True:
    #if display.pressed(badger2040.BUTTON_A):
        #badger_os.warning(display, "je hebt op A gedrukt. Dit scherm gaat na 4 secs weg")
        #time.sleep(4)
        #draw_badge()

    #if display.pressed(badger2040.BUTTON_B):
        #badger_os.warning(display, "je hebt op B gedrukt. Dit scherm gaat na 4 secs weg")
        #time.sleep(4)
        #draw_badge()

    #if display.pressed(badger2040.BUTTON_C):
        #badger_os.warning(display, "je hebt op C gedrukt. Dit scherm gaat na 4 secs weg")
        #time.sleep(4)
        #draw_badge()

    if display.pressed(badger2040.BUTTON_UP):
        # Toggle between badge images
        toggle_badge_image()

        # Redraw the badge with the updated image
        draw_badge()        

        # Introduce a small delay to prevent consecutive button presses from being detected as one
        time.sleep(BUTTON_PRESS_DELAY)
        
    if display.pressed(badger2040.BUTTON_DOWN):
        # Toggle between badge images
        toggle_badge_image()

        # Redraw the badge with the updated image
        draw_badge()     

        # Introduce a small delay to prevent consecutive button presses from being detected as one
        time.sleep(BUTTON_PRESS_DELAY)
        
    display.update()

#	Sending an invisible ping to Sigfox everytime the badge is started.
    SigfoxSend()

    # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
    display.halt()
