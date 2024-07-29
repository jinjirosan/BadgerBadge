# Badge Platform papa - hardware platform v3.0
# (2022-2024)
#
# medical.py : v1.1-refactor 0.0.0

import badger2040
import gfx

# Default title and key/value file
MEDICAL_FILE = "medical.txt"

# Default medical information text
DEFAULT_TEXT = """Name: John Doe
Date of Birth: 01-01-1950
Blood Type: B+
Allergies: None
Medications: None
Length: 175 cm
Weight: 70 kg
Donor: No
Current year: 2024
"""

# Open the medical info file
try:
    badge = open(MEDICAL_FILE, "r")
    medical_info = badge.readlines()
    badge.close()
except OSError:
    with open(MEDICAL_FILE, "w") as f:
        f.write(DEFAULT_TEXT)
        f.flush()
    medical_info = DEFAULT_TEXT.splitlines()

# Ensure there are exactly 9 lines in the medical_info
while len(medical_info) < 9:
    medical_info.append("")

# Extract relevant information
name = medical_info[0].split(": ")[1].strip() if len(medical_info) > 0 else "John Doe"
dob = medical_info[1].split(": ")[1].strip() if len(medical_info) > 1 else "01-06-1974"
blood_type = medical_info[2].split(": ")[1].strip() if len(medical_info) > 2 else "B+"
allergies = medical_info[3].split(": ")[1].strip() if len(medical_info) > 3 else "None"
medications = medical_info[4].split(": ")[1].strip() if len(medical_info) > 4 else "None"
height = medical_info[5].split(": ")[1].strip() if len(medical_info) > 5 else "185 cm"
weight = medical_info[6].split(": ")[1].strip() if len(medical_info) > 6 else "81 kg"
donor = medical_info[7].split(": ")[1].strip() if len(medical_info) > 7 else "No"
current_year = int(medical_info[8].split(": ")[1].strip()) if len(medical_info) > 8 else 2024

# Global variables
WIDTH = badger2040.WIDTH  # 296
HEIGHT = badger2040.HEIGHT  # 128

MENU_TEXT_SIZE = 0.5
LEFT_PADDING = 5
SQUARE_PADDING = 5
TOP_PADDING = 15
DESCRIPTION_PADDING = 10  # Additional padding for descriptions
DESCRIPTION_FONT_SIZE = 0.5  # Font size for descriptions
BLOOD_TYPE_SQUARE_SIZE = 50  # Fixed size of the square for blood type
BLOOD_TYPE_FONT_SIZE = 1.0  # Fixed font size for the blood type
HEIGHT_FONT_SIZE = 0.85  # Fixed font size for the height
WEIGHT_FONT_SIZE = 0.9  # Fixed font size for the weight
INFO_TEXT_SIZE = 0.6  # Font size for the allergies and medications
AGE_FONT_SIZE = 1.0  # Fixed font size for the age
LINE_THICKNESS = 2  # Thickness of the vertical lines

# Function to draw a filled square
def draw_filled_square(x, y, size):
    display.pen(0)  # Black color for filling the square
    display.thickness(2)
    display.rectangle(x, y, size, size)  # Draw the filled square

# Draw text centered within a square
def draw_centered_text(text, x, y, square_size, font_size):
    display.pen(15)  # White color for the text
    text_width = int(display.measure_text(text, font_size))
    text_height = int(font_size * 10)  # Rough estimate of height based on font size
    text_x = x + (square_size - text_width) // 2 + 1
    text_y = y + (square_size - text_height) // 2 + 4  # Adjusted for better centering
    display.text(text, text_x, text_y, font_size)

# Draw height with units centered within a square
def draw_height(x, y, square_size):
    height_value = height.split()[0]  # Extract the height value
    height_unit = height.split()[1]  # Extract the height unit
    draw_centered_text(height_value, x, y, square_size, HEIGHT_FONT_SIZE)
    unit_y = y + BLOOD_TYPE_SQUARE_SIZE // 3  # Position the unit below the value
    draw_centered_text(height_unit, x, unit_y, square_size, HEIGHT_FONT_SIZE * 0.7)  # Smaller font size for the unit

# Draw weight with units centered within a square
def draw_weight(x, y, square_size):
    weight_value = weight.split()[0]  # Extract the weight value
    weight_unit = weight.split()[1]  # Extract the weight unit
    draw_centered_text(weight_value, x, y, square_size, WEIGHT_FONT_SIZE)
    unit_y = y + BLOOD_TYPE_SQUARE_SIZE // 3  # Position the unit below the value
    draw_centered_text(weight_unit, x, unit_y, square_size, WEIGHT_FONT_SIZE * 0.7)  # Smaller font size for the unit

# Calculate age based on date of birth
def calculate_age(dob, current_year):
    day, month, year = map(int, dob.split('-'))
    has_had_birthday = (month, day) <= (6, 1)  # Check if birthday has occurred this year
    age = current_year - year - (not has_had_birthday)
    return str(age)

# Draw the age with units centered within a square
def draw_age(x, y, square_size):
    age = calculate_age(dob, current_year)
    draw_centered_text(age, x, y, square_size, AGE_FONT_SIZE)
    unit_y = y + BLOOD_TYPE_SQUARE_SIZE // 3  # Position the unit below the value
    draw_centered_text("yr", x, unit_y, square_size, AGE_FONT_SIZE * 0.7)  # Smaller font size for the unit

# Draw the descriptions above the squares
def draw_descriptions():
    descriptions = ["Blood", "Height", "Weight", "Age", "Donor"]
    x_positions = [
        LEFT_PADDING,
        LEFT_PADDING + BLOOD_TYPE_SQUARE_SIZE + SQUARE_PADDING,
        LEFT_PADDING + 2 * (BLOOD_TYPE_SQUARE_SIZE + SQUARE_PADDING),
        LEFT_PADDING + 3 * (BLOOD_TYPE_SQUARE_SIZE + SQUARE_PADDING),
        LEFT_PADDING + 4 * (BLOOD_TYPE_SQUARE_SIZE + SQUARE_PADDING)
    ]
    y_position = TOP_PADDING

    display.pen(0)  # Set pen to black color for descriptions
    for i, description in enumerate(descriptions):
        text_width = int(display.measure_text(description, DESCRIPTION_FONT_SIZE))
        text_x = x_positions[i] + (BLOOD_TYPE_SQUARE_SIZE - text_width) // 2
        display.text(description, text_x, y_position, DESCRIPTION_FONT_SIZE)

# Draw the top row of squares
def draw_top_row():
    x_positions = [
        LEFT_PADDING,
        LEFT_PADDING + BLOOD_TYPE_SQUARE_SIZE + SQUARE_PADDING,
        LEFT_PADDING + 2 * (BLOOD_TYPE_SQUARE_SIZE + SQUARE_PADDING),
        LEFT_PADDING + 3 * (BLOOD_TYPE_SQUARE_SIZE + SQUARE_PADDING),
        LEFT_PADDING + 4 * (BLOOD_TYPE_SQUARE_SIZE + SQUARE_PADDING)
    ]
    y_position = TOP_PADDING + DESCRIPTION_PADDING
    
    # Draw the squares
    for x in x_positions:
        draw_filled_square(x, y_position, BLOOD_TYPE_SQUARE_SIZE)
    
    # Draw the text in the squares
    draw_centered_text(blood_type, x_positions[0], y_position, BLOOD_TYPE_SQUARE_SIZE, BLOOD_TYPE_FONT_SIZE)
    draw_height(x_positions[1], y_position, BLOOD_TYPE_SQUARE_SIZE)
    draw_weight(x_positions[2], y_position, BLOOD_TYPE_SQUARE_SIZE)
    draw_age(x_positions[3], y_position, BLOOD_TYPE_SQUARE_SIZE)
    draw_centered_text(donor, x_positions[4], y_position, BLOOD_TYPE_SQUARE_SIZE, BLOOD_TYPE_FONT_SIZE)

# Draw the medical information below the top row of squares
def draw_medical_info():
    y_position = TOP_PADDING + BLOOD_TYPE_SQUARE_SIZE + DESCRIPTION_PADDING + 20  # Adjust this value to place the text below the squares
    display.pen(0)
    display.thickness(2)
    display.text(f"Allergies: {allergies}", LEFT_PADDING, y_position, INFO_TEXT_SIZE)
    y_position += 20
    display.text(f"Medications: {medications}", LEFT_PADDING, y_position, INFO_TEXT_SIZE)

# Draw two vertical lines on the right side
def draw_vertical_lines():
    line_x_positions = [WIDTH - 9,WIDTH - 5, WIDTH - 1]  # Position 20 and 10 pixels from the right edge
    for x in line_x_positions:
        display.pen(0)  # Set pen to black color for lines
        display.thickness(LINE_THICKNESS)
        display.line(x, 0, x, HEIGHT)  # Draw vertical line

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
        draw_descriptions()
        draw_top_row()
        draw_medical_info()
        draw_vertical_lines()  # Add the vertical lines on the right side
        display.update()
        changed = False
        display.led(0)

    display.halt()
