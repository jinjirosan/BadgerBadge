# Badge Platform Eva - hardware platform v3.0
# (2022-2024) Voor m'n lieve guppie
#
# comms.py : v1.0-refactor 0.0.0

import time
import badger2040
import badger_os
import os
from machine import UART
from machine import Pin

# Initialize serial Port
lora = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

LEFT_PADDING = 5
BUTTON_PRESS_DELAY = 0.2
MENU_FONT_SIZE = 0.5  # Fixed font size for menu

# Global Variables for messages
messages = []
message_identifiers = ["AA", "BB", "CC", "DD", "EE"]  # Two-letter identifiers for each message
current_message_index = 0
current_downlink_message = None
selected_message_index = 0
is_menu_active = False
is_downlink_displayed = False  # Track if downlink message is being displayed
selected_message = None  # Variable to store the selected message
selected_identifier = None  # Variable to store the identifier to be sent

# ------------------------------
#      Utility functions
# ------------------------------

def is_on_battery():
    return not os.uname().machine.startswith("USB")

def turn_on_led():
    display.led(128)  # Set LED brightness to mid-level

def turn_off_led():
    display.led(0)    # Turn off the LED

def fit_text(text, max_width, min_size=0.5, max_size=2.0):
    """Adjusts the font size so the text fits within max_width."""
    size = max_size
    while size >= min_size:
        if display.measure_text(text, size) <= max_width:
            return size
        size -= 0.1
    return min_size

# ------------------------------
#      Display Functions
# ------------------------------

def display_message(message):
    display.pen(15)
    display.clear()
    display.pen(0)
    display.font("sans")
    display.thickness(2)
    size = fit_text(message, WIDTH - 2 * LEFT_PADDING)
    display.text(message, LEFT_PADDING, HEIGHT // 2, size)
    display.update()

def display_main_screen():
    display.pen(15)
    display.clear()
    display.pen(0)
    display.font("sans")
    display.thickness(4)
    display.text("COMMS", LEFT_PADDING, HEIGHT // 2 - 40, 2.0)

    # Display currently selected message in smaller font
    display.thickness(2)
    if selected_message:
        message_text = f"Selected: {selected_message}"
    else:
        message_text = "No message selected"
    size = fit_text(message_text, WIDTH - 2 * LEFT_PADDING)
    display.text(message_text, LEFT_PADDING, HEIGHT // 2, size)
    
    # Draw button labels
    display.thickness(1)
    display.text("Transmit", LEFT_PADDING, HEIGHT - 15, 0.5)
    display.text("Fetch", WIDTH // 2 - 20, HEIGHT - 15, 0.5)
    display.text("Pick", WIDTH - 50, HEIGHT - 15, 0.5)
    
    display.update()
    turn_off_led()  # Turn off LED when main screen is shown

def show_message_menu():
    display.pen(15)
    display.clear()
    display.pen(0)
    display.font("sans")
    display.thickness(2)

    # Consistent font size for menu items
    y_position = 20
    for i, message in enumerate(messages):
        msg_number = f"{i + 1}. "  # Message number
        full_message = msg_number + message
        if i == selected_message_index:
            # Highlight selected message
            display.pen(0)
            display.rectangle(LEFT_PADDING, y_position - 5, WIDTH - 2 * LEFT_PADDING, 15)
            display.pen(15)
        else:
            display.pen(0)
        display.text(full_message, LEFT_PADDING + 5, y_position, MENU_FONT_SIZE)
        y_position += 20  # Move to the next line

    # Draw "Select" label for C-button
    display.pen(0)
    display.text("Select", WIDTH - 50, HEIGHT - 15, 0.5)
    
    display.update()
    turn_off_led()  # Turn off LED when selection menu is shown

def display_downlink_message(message):
    # Display the downlink message
    display.pen(15)
    display.clear()
    display.pen(0)
    display.font("sans")
    display.thickness(2)
    size = fit_text(message, WIDTH - 2 * LEFT_PADDING)
    display.text(message, LEFT_PADDING, HEIGHT // 2, size)
    display.text("Clear", WIDTH // 2 - 20, HEIGHT - 15, 0.5)
    display.update()

def update_fetch_label(status):
    """Update the Fetch button label based on the current status."""
    if status == "checking":
        display.pen(15)
        display.rectangle(WIDTH // 2 - 20, HEIGHT - 15, 50, 10)  # Clear existing label area
        display.pen(0)
        display.text("Checking", WIDTH // 2 - 20, HEIGHT - 15, 0.5)
    elif status == "fetch":
        display.pen(15)
        display.rectangle(WIDTH // 2 - 20, HEIGHT - 15, 50, 10)  # Clear existing label area
        display.pen(0)
        display.text("Fetch", WIDTH // 2 - 20, HEIGHT - 15, 0.5)
    display.update()

# ------------------------------
#        Sigfox functions
# ------------------------------

def send_predefined_message():
    global selected_identifier
    try:
        turn_on_led()
        if selected_identifier is None:
            print("No message selected to send.")
            display_message("No Message Selected")
            return

        print(f"Preparing to send Sigfox message with identifier: {selected_identifier}")

        # Reset macro channels
        print("Resetting macro channels...")
        lora.write("AT$RC\r\n")
        time.sleep(2)
        response = lora.read(64)
        print(f"Response after resetting macro channels: {response}")

        # Send the two-letter identifier via Sigfox
        command = f"AT$SF={selected_identifier}\r\n"
        print(f"Sending command: {command}")
        lora.write(command)
        time.sleep(6)
        response = lora.read(64)  # Read response with enough buffer size
        print(f"Sigfox response: {response}")

        # Check if the message was sent based on response or lack of response
        if response is None or b"OK" not in response:
            print("Message sent, but no confirmation response received from Sigfox.")
            display_message("Message Sent (No Confirm)")
        else:
            print("Sigfox message sent successfully:", response)
            display_message("Message Sent")
    except Exception as e:
        print("Error sending message:", str(e))
        display_message("Error Sending")
    finally:
        turn_off_led()  # Ensure LED is turned off after sending

def check_downlink_message():
    global current_downlink_message, is_downlink_displayed
    try:
        turn_on_led()
        update_fetch_label("checking")
        print("Checking for downlink message...")
        lora.write("AT$DR=1\r\n")  # Command to initiate downlink
        time.sleep(6)
        downlink_message = lora.read(64)  # Adjust size based on expected message length
        print(f"Downlink response: {downlink_message}")

        if downlink_message:
            current_downlink_message = downlink_message.decode().strip()
            print("Downlink message received:", current_downlink_message)
            if current_downlink_message == "OK" or current_downlink_message == "OK OK":
                display_message("No New Messages")
                time.sleep(2)  # Show the "No New Messages" status for 2 seconds
                display_main_screen()
            else:
                display_downlink_message(current_downlink_message)
                is_downlink_displayed = True  # Set flag to indicate that downlink message is displayed
        else:
            print("No response or error checking downlink.")
            display_message("Error Checking")
            time.sleep(2)
            display_main_screen()
        
    except Exception as e:
        print("Error checking downlink:", str(e))
        display_message("Error Checking")
        time.sleep(2)
        display_main_screen()
    finally:
        update_fetch_label("fetch")
        turn_off_led()  # Ensure LED is turned off after checking

def select_message():
    global is_menu_active, selected_message, selected_identifier
    selected_message = messages[selected_message_index]
    selected_identifier = message_identifiers[selected_message_index]  # Store corresponding identifier
    print(f"Selected message: {selected_message} with identifier {selected_identifier}")
    display_message(f"Selected: {selected_message}")
    time.sleep(1)  # Pause to show the selected message
    is_menu_active = False
    display_main_screen()

# ------------------------------
#        Program setup
# ------------------------------

# Create a new Badger and set it to update NORMAL
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_NORMAL)

# Load messages from comms.txt
try:
    with open("comms.txt", "r") as f:
        messages = [line.strip() for line in f.readlines() if line.strip()]
except OSError:
    print("Failed to read comms.txt file")
    messages = ["Message 1", "Message 2", "Message 3", "Message 4", "Message 5"]  # Default messages

# Ensure the number of identifiers matches the number of messages
message_identifiers = message_identifiers[:len(messages)]

# Draw the main screen initially
display_main_screen()

# ------------------------------
#       Main program
# ------------------------------

while True:
    if is_downlink_displayed:
        if display.pressed(badger2040.BUTTON_B):
            print("Button B pressed. Clearing downlink message and returning to main menu...")
            is_downlink_displayed = False
            display_main_screen()
            time.sleep(BUTTON_PRESS_DELAY)
    elif not is_menu_active:
        if display.pressed(badger2040.BUTTON_A):
            print("Button A pressed. Sending message...")
            send_predefined_message()
            display_main_screen()
            time.sleep(BUTTON_PRESS_DELAY)

        if display.pressed(badger2040.BUTTON_B):
            print("Button B pressed. Checking downlink...")
            check_downlink_message()
            time.sleep(BUTTON_PRESS_DELAY)  # Wait for button debounce

        if display.pressed(badger2040.BUTTON_C):
            print("Button C pressed. Showing selection menu...")
            is_menu_active = True
            show_message_menu()
            time.sleep(BUTTON_PRESS_DELAY)

    else:
        if display.pressed(badger2040.BUTTON_C):
            print("Button C pressed in menu. Selecting message...")
            select_message()

        if display.pressed(badger2040.BUTTON_UP):
            selected_message_index = (selected_message_index - 1) % len(messages)
            print(f"Button UP pressed. Selected message index: {selected_message_index}")
            show_message_menu()
            time.sleep(BUTTON_PRESS_DELAY)

        if display.pressed(badger2040.BUTTON_DOWN):
            selected_message_index = (selected_message_index + 1) % len(messages)
            print(f"Button DOWN pressed. Selected message index: {selected_message_index}")
            show_message_menu()
            time.sleep(BUTTON_PRESS_DELAY)

    if not is_on_battery():
        display.halt()  # Power management
