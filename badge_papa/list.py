# Badge Platform papa - hardware platform v3.0
# (2022-2024)
#
# list.py : v1.0.0-refactor 0.0.1

import binascii
import badger2040
import badger_os
import time
import os


# Configuration Constants
LIST_TITLE = "Heb ik alles?"  # Checklist title
LIST_FILE = "checklist.txt"   # Data file

# Display Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

# UI Constants
ARROW_THICKNESS = 3
ARROW_WIDTH = 18
ARROW_HEIGHT = 14
ARROW_PADDING = 2

MAX_ITEM_CHARS = 26
TITLE_TEXT_SIZE = 0.7
ITEM_TEXT_SIZE = 0.5  # Smaller text size for better performance
ITEM_SPACING = 17     # Tighter spacing like comms.py

LIST_START = 40
LIST_PADDING = 2
LIST_WIDTH = WIDTH - LIST_PADDING - LIST_PADDING - ARROW_WIDTH
LIST_HEIGHT = HEIGHT - LIST_START - LIST_PADDING - ARROW_HEIGHT

# Constants for UI responsiveness
BUTTON_PRESS_DELAY = 0.1  # Even shorter delay for better responsiveness

# Add constants for update regions
ITEM_HEIGHT = 13  # Fixed height for items
ITEM_Y_PADDING = 4  # Space above/below items

# Constants for update regions
SELECTION_HEIGHT = 13  # Height of selection bar
SELECTION_PADDING = 4  # Padding above/below selection


def is_on_battery():
    """Override battery detection to always return False for maximum performance."""
    return False


def draw_up(x, y, width, height, thickness, padding):
    border = (thickness // 4) + padding
    display.line(
        x + border,
        y + height - border,
        x + (width // 2),
        y + border
    )
    display.line(
        x + (width // 2),
        y + border,
        x + width - border,
        y + height - border
    )


def draw_down(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(
        x + border,
        y + border,
        x + (width // 2),
        y + height - border
    )
    display.line(
        x + (width // 2),
        y + height - border,
        x + width - border,
        y + border
    )


def draw_left(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(
        x + width - border,
        y + border,
        x + border,
        y + (height // 2)
    )
    display.line(
        x + border,
        y + (height // 2),
        x + width - border,
        y + height - border
    )


def draw_right(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(
        x + border,
        y + border,
        x + width - border,
        y + (height // 2)
    )
    display.line(
        x + width - border,
        y + (height // 2),
        x + border,
        y + height - border
    )


def draw_tick(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(
        x + border,
        y + ((height * 2) // 3),
        x + (width // 2),
        y + height - border
    )
    display.line(
        x + (width // 2),
        y + height - border,
        x + width - border,
        y + border
    )


def draw_cross(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(
        x + border,
        y + border,
        x + width - border,
        y + height - border
    )
    display.line(
        x + width - border,
        y + border,
        x + border,
        y + height - border
    )


def draw_checkbox(x, y, size, background, foreground, thickness, tick, padding):
    border = (thickness // 2) + padding
    display.pen(background)
    display.rectangle(
        x + border,
        y + border,
        size - (border * 2),
        size - (border * 2)
    )
    
    display.pen(foreground)
    display.thickness(thickness)
    
    # Draw box
    display.line(
        x + border,
        y + border,
        x + size - border,
        y + border
    )
    display.line(
        x + border,
        y + border,
        x + border,
        y + size - border
    )
    display.line(
        x + size - border,
        y + border,
        x + size - border,
        y + size - border
    )
    display.line(
        x + border,
        y + size - border,
        x + size - border,
        y + size - border
    )
    
    if tick:
        draw_tick(x, y, size, size, thickness, 2 + border)


def draw_list(items, item_states, start_item, highlighted_item, x, y, width, height, item_height, columns, full_redraw=False):
    """Draw the list of items with efficient highlighting."""
    item_x = 0
    item_y = 0
    current_col = 0
    
    if full_redraw:
        # Clear entire list area on full redraw
        display.pen(15)  # White
        display.rectangle(0, y - (item_height // 2), WIDTH, height)
    
    for i in range(start_item, len(items)):
        current_y = item_y + y
        
        # Only redraw items that need updating
        if full_redraw or i == highlighted_item or i == last_highlighted_item:
            # Clear background for this item
            display.pen(15)  # White
            display.rectangle(
                item_x,
                current_y - 4,  # Adjusted for tighter spacing
                width // columns,
                13  # Fixed height like comms.py
            )
            
            # Draw highlight if selected - using darker gray (0 is black, 15 is white)
            if i == highlighted_item:
                display.pen(0)  # Use black for stronger contrast
                display.rectangle(
                    item_x,
                    current_y - 4,
                    width // columns,
                    13
                )
                display.pen(15)  # White text for highlighted items
            else:
                display.pen(0)  # Black text for non-highlighted items
            
            # Draw text with consistent thickness
            display.thickness(1)  # Always use thin text
            display.text(
                items[i],
                item_x + x + item_height,
                current_y,
                ITEM_TEXT_SIZE
            )
            
            # Draw checkbox
            draw_checkbox(
                item_x,
                current_y - (item_height // 2),
                item_height,
                15,  # White background
                0,   # Black foreground
                2,
                item_states[i],
                2
            )
        
        item_y += item_height
        if item_y >= height - (item_height // 2):
            item_x += width // columns
            item_y = 0
            current_col += 1
            if current_col >= columns:
                return

# Initialize display
display = badger2040.Badger2040()
display.led(128)

# Set initial speed based on power source
if is_on_battery():
    display.update_speed(badger2040.UPDATE_TURBO)
    badger2040.system_speed(badger2040.SYSTEM_NORMAL)
else:
    display.update_speed(badger2040.UPDATE_TURBO)
    badger2040.system_speed(badger2040.SYSTEM_TURBO)

# Initialize state
changed = False
state = {"current_item": 0}
list_items = []
last_highlighted_item = None  # Track last highlighted item for partial redraw
navigation_active = False     # Track if we're in navigation mode

# Load items and state
try:
    with open(LIST_FILE, "r") as f:
        raw_list_items = f.read()
        
    if raw_list_items.find(" X\n") != -1:
        # Convert old format
        list_items = []
        state = {
            "current_item": 0,
            "checked": []
        }
        for item in raw_list_items.strip().split("\n"):
            if item.endswith(" X"):
                state["checked"].append(True)
                item = item[:-2]
            else:
                state["checked"].append(False)
            list_items.append(item)
        state["items_hash"] = binascii.crc32("\n".join(list_items))
        badger_os.state_save("list", state)
        
        # Save in new format
        with open(LIST_FILE, "w") as f:
            for item in list_items:
                f.write(f"{item}\n")
    else:
        list_items = [
            item.strip()
            for item in raw_list_items.strip().split("\n")
        ]
        
except OSError:
    # Use defaults if file doesn't exist
    list_items = [
        "iPhone", "Sleutels", "Multitool", "Labello",
        "Menthol", "Rugzak", "Zonnebril"
    ]
    with open(LIST_FILE, "w") as f:
        for item in list_items:
            f.write(f"{item}\n")

# Load or initialize state
badger_os.state_load("list", state)
items_hash = binascii.crc32("\n".join(list_items))
if "items_hash" not in state or state["items_hash"] != items_hash:
    state["current_item"] = 0
    state["items_hash"] = items_hash
    state["checked"] = [False] * len(list_items)
    changed = True

# Calculate layout
longest_item = 0
for i, item in enumerate(list_items):
    while True:
        item_length = display.measure_text(item, ITEM_TEXT_SIZE)
        if item_length > LIST_WIDTH - ITEM_SPACING:
            item = item[:-1]
            list_items[i] = item
        else:
            break
    longest_item = max(longest_item, item_length)

# Calculate columns and items per column
list_columns = 1
while longest_item + ITEM_SPACING < (LIST_WIDTH // (list_columns + 1)):
    list_columns += 1

items_per_column = (LIST_HEIGHT // ITEM_SPACING) + 1

# Do initial full draw with complete screen refresh
display.pen(15)
display.clear()
display.update()  # Force a full refresh to clear any previous content

# Draw continuous vertical bar for arrows
display.pen(12)  # Gray
display.rectangle(WIDTH - ARROW_WIDTH, 0, ARROW_WIDTH, HEIGHT)

# Draw bottom bar
display.rectangle(0, HEIGHT - ARROW_HEIGHT, WIDTH, ARROW_HEIGHT)

y = LIST_PADDING + 12
display.pen(0)
display.thickness(3)
display.text(LIST_TITLE, LIST_PADDING, y, TITLE_TEXT_SIZE)

y += 12
display.pen(0)
display.thickness(2)
display.line(LIST_PADDING, y, WIDTH - LIST_PADDING - ARROW_WIDTH, y)

if len(list_items) > 0:
    # Initial list draw with full refresh
    display.pen(0)
    display.thickness(1)
    draw_list(
        list_items,
        state["checked"],
        0,  # Start from first item
        state["current_item"],
        LIST_PADDING,
        LIST_START,
        LIST_WIDTH,
        LIST_HEIGHT,
        ITEM_SPACING,
        list_columns,
        full_redraw=True
    )
    
    # Draw initial buttons
    display.pen(0)
    display.thickness(ARROW_THICKNESS)
    
    if state["current_item"] > 0:
        draw_up(
            WIDTH - ARROW_WIDTH,
            (HEIGHT // 4) - (ARROW_HEIGHT // 2),
            ARROW_WIDTH,
            ARROW_HEIGHT,
            ARROW_THICKNESS,
            ARROW_PADDING
        )
        draw_left(
            (WIDTH // 7) - (ARROW_WIDTH // 2),
            HEIGHT - ARROW_HEIGHT,
            ARROW_WIDTH,
            ARROW_HEIGHT,
            ARROW_THICKNESS,
            ARROW_PADDING
        )
    
    if state["current_item"] < (len(list_items) - 1):
        draw_down(
            WIDTH - ARROW_WIDTH,
            ((HEIGHT * 3) // 4) - (ARROW_HEIGHT // 2),
            ARROW_WIDTH,
            ARROW_HEIGHT,
            ARROW_THICKNESS,
            ARROW_PADDING
        )
        draw_right(
            ((WIDTH * 6) // 7) - (ARROW_WIDTH // 2),
            HEIGHT - ARROW_HEIGHT,
            ARROW_WIDTH,
            ARROW_HEIGHT,
            ARROW_THICKNESS,
            ARROW_PADDING
        )

    display.update()

# Main program loop
while True:
    if len(list_items) > 0:
        if display.pressed(badger2040.BUTTON_UP):
            if state["current_item"] > 0:
                last_highlighted_item = state["current_item"]
                state["current_item"] -= 1
                changed = True
                time.sleep(BUTTON_PRESS_DELAY)
                
        elif display.pressed(badger2040.BUTTON_DOWN):
            if state["current_item"] < len(list_items) - 1:
                last_highlighted_item = state["current_item"]
                state["current_item"] += 1
                changed = True
                time.sleep(BUTTON_PRESS_DELAY)
                
        elif display.pressed(badger2040.BUTTON_A):  # Left button
            # Calculate current position
            current_row = state["current_item"] % items_per_column
            current_column = state["current_item"] // items_per_column
            
            # Only move left if we're not in the first column
            if current_column > 0:
                new_item = ((current_column - 1) * items_per_column) + current_row
                if new_item < len(list_items):
                    last_highlighted_item = state["current_item"]
                    state["current_item"] = new_item
                    changed = True
                    time.sleep(BUTTON_PRESS_DELAY)
                
        elif display.pressed(badger2040.BUTTON_C):  # Right button
            # Calculate current position
            current_row = state["current_item"] % items_per_column
            current_column = state["current_item"] // items_per_column
            
            # Calculate target position in next column
            new_item = ((current_column + 1) * items_per_column) + current_row
            
            # Only move right if target exists and we're not in the last column
            if new_item < len(list_items) and current_column < list_columns - 1:
                last_highlighted_item = state["current_item"]
                state["current_item"] = new_item
                changed = True
                time.sleep(BUTTON_PRESS_DELAY)
                
        elif display.pressed(badger2040.BUTTON_B):  # Middle button - toggle checkbox
            state["checked"][state["current_item"]] = not state["checked"][state["current_item"]]
            changed = True
            time.sleep(BUTTON_PRESS_DELAY)

    if changed:
        badger_os.state_save("list", state)
        
        if len(list_items) > 0:
            # Calculate positions for old and new items
            if last_highlighted_item is not None:
                old_y = (last_highlighted_item % items_per_column) * ITEM_SPACING
                old_x = (last_highlighted_item // items_per_column) * (LIST_WIDTH // list_columns)
                
                # Clear old highlight area
                display.pen(15)  # White
                display.rectangle(
                    old_x,
                    LIST_START + old_y - 4,
                    LIST_WIDTH // list_columns,
                    13
                )
                
                # Redraw old item
                display.pen(0)
                display.thickness(1)
                display.text(
                    list_items[last_highlighted_item],
                    old_x + ITEM_SPACING,
                    LIST_START + old_y,
                    ITEM_TEXT_SIZE
                )
                
                # Redraw old checkbox
                draw_checkbox(
                    old_x,
                    LIST_START + old_y - (ITEM_SPACING // 2),
                    ITEM_SPACING,
                    15,  # White background
                    0,   # Black foreground
                    2,
                    state["checked"][last_highlighted_item],
                    2
                )
            
            # Draw new highlight and item
            new_y = (state["current_item"] % items_per_column) * ITEM_SPACING
            new_x = (state["current_item"] // items_per_column) * (LIST_WIDTH // list_columns)
            
            # Draw highlight bar
            display.pen(0)  # Black
            display.rectangle(
                new_x,
                LIST_START + new_y - 4,
                LIST_WIDTH // list_columns,
                13
            )
            
            # Draw new item
            display.pen(15)  # White text for highlighted item
            display.thickness(1)
            display.text(
                list_items[state["current_item"]],
                new_x + ITEM_SPACING,
                LIST_START + new_y,
                ITEM_TEXT_SIZE
            )
            
            # Draw new checkbox
            draw_checkbox(
                new_x,
                LIST_START + new_y - (ITEM_SPACING // 2),
                ITEM_SPACING,
                15,  # White background
                0,   # Black foreground
                2,
                state["checked"][state["current_item"]],
                2
            )
            
            display.update()
            
        changed = False
        
    display.halt()
