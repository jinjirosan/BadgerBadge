# Badge Platform papa - hardware platform v3.0
# (2022-2024)
#
# badge.py : v2.6.4-refactor 0.0.2

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

# Load the badge images
#BADGE_IMAGE = bytearray(int(IMAGE_WIDTH * HEIGHT / 8))
#BADGE_IMAGE_QR = bytearray(int(IMAGE_WIDTH * HEIGHT / 8))
def load_image(filename):
    try:
        with open(filename, "rb") as file:
            data = file.read()
            expected_size = int(IMAGE_WIDTH * HEIGHT / 8)
            actual_size = len(data)
            if actual_size != expected_size:
                raise ValueError(f"Expected image size {expected_size} bytes, but got {actual_size} bytes")
            return bytearray(data)
    except OSError as e:
        print(f"Failed to read {filename}: {e}")
        return None

current_image_file = "badge-personal-image.bin"  # Adjust as necessary based on your starting badge

BADGE_IMAGE = load_image("badge-personal-image.bin") or bytearray(int(IMAGE_WIDTH * HEIGHT / 8))
BADGE_IMAGE_QR = load_image("badge-personal-image_qr.bin") or None

# Load the initial badge image
CURRENT_BADGE_IMAGE = BADGE_IMAGE


# Add a state variable to manage badge type
current_badge_type = 0  # 0: Personal, 1: Work, 2: Event

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
def toggle_qr_image():
    global CURRENT_BADGE_IMAGE, current_image_file
    print(f"Current image before toggle: {current_image_file}")
    
    if "_qr" in current_image_file:
        new_image_file = current_image_file.replace("_qr.bin", ".bin")
    else:
        new_image_file = current_image_file.replace(".bin", "_qr.bin")

    print(f"Attempting to load image from: {new_image_file}")
    new_image = load_image(new_image_file)
    if new_image:
        CURRENT_BADGE_IMAGE = new_image
        current_image_file = new_image_file
        print(f"Switched to image: {new_image_file}")
    else:
        print("Failed to load image:", new_image_file)

    draw_badge()
    
#Function to cycle through badge types
def cycle_badge_type(direction):
    global current_badge_type, current_image_file, CURRENT_BADGE_IMAGE
    max_badge_types = 3  # Total number of badge types

    if direction == "up":
        current_badge_type = (current_badge_type + 1) % max_badge_types
    elif direction == "down":
        current_badge_type = (current_badge_type - 1 + max_badge_types) % max_badge_types

    if current_badge_type == 0:
        current_image_file = "badge-personal-image.bin"
    elif current_badge_type == 1:
        current_image_file = "badge-work-image.bin"
    elif current_badge_type == 2:
        current_image_file = "badge-event-image.bin"

    CURRENT_BADGE_IMAGE = load_image(current_image_file) or bytearray(int(IMAGE_WIDTH * HEIGHT / 8))
    print(f"Switching to: {current_image_file} with badge type {current_badge_type}")

    draw_badge()  # Redraw immediately after state change



# Redesigned draw_badge function to handle multiple badge types
def draw_badge():
    display.led(128)  # Optionally turn on or adjust the LED when drawing a badge for feedback
    if current_badge_type == 0:
        draw_personal_badge()
    elif current_badge_type == 1:
        draw_work_badge()
    elif current_badge_type == 2:
        draw_event_badge()
    display.update()  # Make sure to update the display to reflect changes
    turn_off_led()    # Turn off the LED after the badge is drawn

# Function to check button states and manage debouncing
def check_buttons():
    global last_button_state_up, last_button_state_down, last_button_state_c
    current_up = display.pressed(badger2040.BUTTON_UP)
    current_down = display.pressed(badger2040.BUTTON_DOWN)
    current_c = display.pressed(badger2040.BUTTON_C)

    # Handle UP button
    if current_up and not last_button_state_up:
        cycle_badge_type("up")
        time.sleep(BUTTON_PRESS_DELAY)

    # Handle DOWN button
    if current_down and not last_button_state_down:
        cycle_badge_type("down")
        time.sleep(BUTTON_PRESS_DELAY)

    # Handle C button
    if current_c and not last_button_state_c:
        toggle_qr_image()
        time.sleep(BUTTON_PRESS_DELAY)

    # Update last known states
    last_button_state_up = current_up
    last_button_state_down = current_down
    last_button_state_c = current_c


# Detect if running on battery
def is_on_battery():
    # This is a placeholder function. You'll need to replace it with the actual method to detect power source if available.
    return not os.uname().machine.startswith("USB")

# Function to turn off the LED explicitly
def turn_off_led():
    display.led(0)

# ------------------------------
#      Drawing functions
# ------------------------------

def draw_cissp_logo(display, x, y, scale):
    line_width = max(1, scale // 10)  # Basic width for line drawing

    def draw_rect(x1, y1, width, height):
        for i in range(width):
            for j in range(height):
                display.pixel(x1 + i, y1 + j)

    letter_spacing = scale // 2  # Standard spacing between letters
    letter_width = scale * 2     # Width used for most letters

    # Draw C
    draw_rect(x, y, line_width, scale)  # Vertical line
    draw_rect(x, y, letter_width, line_width)  # Top horizontal line
    draw_rect(x, y + scale - line_width, letter_width, line_width)  # Bottom horizontal line

    # Draw I
    next_x = x + letter_width + letter_spacing
    draw_rect(next_x, y, line_width, scale)

    # Draw S - calculate next_x considering I's actual width (line_width) + spacing
    next_x += line_width + letter_spacing
    draw_rect(next_x, y, letter_width, line_width)  # Top horizontal line
    draw_rect(next_x, y + (scale // 2) - (line_width // 2), letter_width, line_width)  # Middle horizontal line
    draw_rect(next_x, y + scale - line_width, letter_width, line_width)  # Bottom horizontal line
    draw_rect(next_x, y, line_width, scale // 2)  # Top-left vertical line
    draw_rect(next_x + letter_width - line_width, y + (scale // 2), line_width, scale // 2)  # Bottom-right vertical line

    # Second S
    next_x += letter_width + letter_spacing
    draw_rect(next_x, y, letter_width, line_width)
    draw_rect(next_x, y + (scale // 2) - (line_width // 2), letter_width, line_width)
    draw_rect(next_x, y + scale - line_width, letter_width, line_width)
    draw_rect(next_x, y, line_width, scale // 2)
    draw_rect(next_x + letter_width - line_width, y + (scale // 2), line_width, scale // 2)

    # P
    next_x += letter_width + letter_spacing
    draw_rect(next_x, y, line_width, scale)
    draw_rect(next_x, y, letter_width, line_width)
    draw_rect(next_x + letter_width - line_width, y, line_width, scale // 2)
    draw_rect(next_x, y + (scale // 2) - (line_width // 2), letter_width, line_width)




# Draw the personal badge, including user text
def draw_personal_badge():
    display.pen(0)
    display.clear()
    
    print(f"Buffer size: {len(CURRENT_BADGE_IMAGE)}, Expected: {IMAGE_WIDTH * HEIGHT // 8}")


    # Draw badge image
    print(f"Displaying at: {WIDTH - IMAGE_WIDTH}, 0 with size {IMAGE_WIDTH}x{HEIGHT}")
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

    # Draw button C QR label
    display.pen(15)
    display.font("sans")
    display.thickness(1)
    display.rectangle(271, 118, 19, 9)
    display.pen(0)
    display.text("QR", 273, 122, 0.4)
    display.pen(15)

# Function to draw the work badge with dynamic text sizing
def draw_work_badge():
    display.pen(15)
    display.clear()

    # Draw badge image
    display.image(CURRENT_BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, 0, 0)

    work_text = "MDG InfoSec"
    work_name_text = "Ray Flinkerbusch"
    work_role_text = "Security Architect"
    work_slogan_text = "SED'QUIS CUSTODIET IPSOS CUSTODES"

    # Start with a reasonable size for the main text and decrease until it fits
    text_size = 2
    while display.measure_text(work_text, text_size) > WIDTH - IMAGE_WIDTH and text_size > 0:
        text_size -= 0.1  # Decrease the text size incrementally

    # Set the text color and font
    display.pen(0)  # Black text for readability
    display.font("sans")
    display.thickness(3)

    # Calculate text position to fit it next to the image
    text_width = display.measure_text(work_text, text_size)
    text_x = IMAGE_WIDTH + (WIDTH - IMAGE_WIDTH - text_width) // 2  # Center text between the image and the right side
    text_y = 30  # Small padding from the top
    display.text(work_text, text_x, text_y, text_size)

    # Settings for the name text
    name_text_size = text_size - 0.4  # Slightly smaller text size
    display.thickness(2)

    # Calculate position for the name text to align it with the right end of the work_text
    name_text_width = display.measure_text(work_name_text, name_text_size)
    name_text_x = text_x + text_width - name_text_width  # Align to the right end of the work_text
    name_text_y = text_y + 30  # Positioned 20 pixels below the work_text
    display.text(work_name_text, name_text_x, name_text_y, name_text_size)

    # Draw the role text with a black background
    role_text_size = name_text_size  # Same size as name text
    role_text_width = display.measure_text(work_role_text, role_text_size)
    role_text_x = name_text_x  # Align with the name text
    role_text_y = name_text_y + 15  # Positioned 15 pixels below the name text

    # Black background for role text
    display.pen(0)  # Set pen to black for background
    display.rectangle(role_text_x, role_text_y - 5, WIDTH - role_text_x, 12)  # Rectangle height approx to text size

    # White text for the role
    display.pen(15)  # Set pen to white for text
    display.thickness(1)  # Less thickness
    display.text(work_role_text, role_text_x, role_text_y, role_text_size)

    # Settings for the slogan text
    slogan_text_size = name_text_size  # Same size as name text
    display.thickness(1)  # Less thickness

    # Fit slogan text across the full width of the display
    while display.measure_text(work_slogan_text, slogan_text_size) > WIDTH and slogan_text_size > 0:
        slogan_text_size -= 0.1  # Decrease the text size incrementally if it doesn't fit

    slogan_text_width = display.measure_text(work_slogan_text, slogan_text_size)
    slogan_text_x = (WIDTH - slogan_text_width) // 2  # Center slogan text horizontally
    slogan_text_y = HEIGHT - 6  # Positioned 20 pixels above the bottom of the display

    display.pen(0)  # Set pen to black
    display.text(work_slogan_text, slogan_text_x, slogan_text_y, slogan_text_size)
    
    draw_cissp_logo(display, 230, 85, 6)  # Starts at (10,10), with each letter 40 pixels high
    
    #display.update()
    
# Function to draw the event badge with dynamic text sizing
def draw_event_badge():
    display.pen(0)
    display.clear()

    #event_text = "EVENTBADGE"
    ## Start with a reasonable size and decrease until it fits
    #text_size = 2
    #while display.measure_text(event_text, text_size) > WIDTH and text_size > 0:
    #    text_size -= 0.1  # Decrease the text size incrementally

    ## Set the text color and font
    #display.pen(15)  # White text
    #display.font("sans")
    #display.thickness(2)

    ## Calculate text position to center it
    #text_width = display.measure_text(event_text, text_size)
    #display.text(event_text, (WIDTH - text_width) // 2, HEIGHT // 2, text_size)

    #display.update()

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

# Draw the initial badge on startup
draw_badge()

# Sending an invisible ping to Sigfox everytime the badge is started.
#SigfoxSend()

#display.update()

try:
#    draw_badge()  # Draw the initial badge on startup
    
    # Initialize last button states
    last_button_state_up = False
    last_button_state_down = False
    last_button_state_b = False
    
    while True:
        check_buttons()  # Continuously check and handle button inputs
            
        # Reset LED after operations -- redundant here as it's handled in draw_badge but good for safety
        turn_off_led()  
        
        # Use halt only if not on battery or ensure wake-up on button press is configured correctly
        # If on battery, halt the Badger to save power, it will wake up if any of the front buttons are pressed
        if not is_on_battery():
            display.halt()

except KeyboardInterrupt:
    print("Program terminated by user.")





