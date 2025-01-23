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
    """Check if running on battery power."""
    return not os.uname().machine.startswith("USB")


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
            
            # Draw highlight if selected
            if i == highlighted_item:
                display.pen(12)  # Gray
                display.rectangle(
                    item_x,
                    current_y - 4,
                    width // columns,
                    13
                )
            
            # Draw text with consistent thickness
            display.pen(0)  # Black text
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
changed = not badger2040.woken_by_button()
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

# Calculate columns and pages
list_columns = 1
while longest_item + ITEM_SPACING < (LIST_WIDTH // (list_columns + 1)):
    list_columns += 1

items_per_page = ((LIST_HEIGHT // ITEM_SPACING) + 1) * list_columns
current_page = state["current_item"] // items_per_page  # Calculate current page based on selected item

# Do initial full draw
display.pen(15)
display.clear()

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
    # Calculate starting item for current page
    page_start_item = current_page * items_per_page
    
    # Initial list draw
    display.pen(0)
    display.thickness(1)  # Set consistent thin text for initial draw
    draw_list(
        list_items,
        state["checked"],
        page_start_item,  # Use page_start_item instead of page_item
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
    
    if state["checked"][state["current_item"]]:
        draw_cross(
            (WIDTH // 2) - (ARROW_WIDTH // 2),
            HEIGHT - ARROW_HEIGHT,
            ARROW_HEIGHT,
            ARROW_HEIGHT,
            ARROW_THICKNESS,
            ARROW_PADDING
        )
    else:
        draw_tick(
            (WIDTH // 2) - (ARROW_WIDTH // 2),
            HEIGHT - ARROW_HEIGHT,
            ARROW_HEIGHT,
            ARROW_HEIGHT,
            ARROW_THICKNESS,
            ARROW_PADDING
        )
else:
    empty_text = "Nothing Here"
    text_length = display.measure_text(empty_text, ITEM_TEXT_SIZE)
    display.text(
        empty_text,
        ((LIST_PADDING + LIST_WIDTH) - text_length) // 2,
        (LIST_HEIGHT // 2) + LIST_START - (ITEM_SPACING // 4),
        ITEM_TEXT_SIZE
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
                # Faster updates during navigation
                display.update_speed(badger2040.UPDATE_TURBO)
                time.sleep(BUTTON_PRESS_DELAY)
                
        elif display.pressed(badger2040.BUTTON_DOWN):
            if state["current_item"] < len(list_items) - 1:
                last_highlighted_item = state["current_item"]
                state["current_item"] += 1
                changed = True
                # Faster updates during navigation
                display.update_speed(badger2040.UPDATE_TURBO)
                time.sleep(BUTTON_PRESS_DELAY)
                
        elif display.pressed(badger2040.BUTTON_A):
            if state["current_item"] > 0:
                last_highlighted_item = state["current_item"]
                old_page = state["current_item"] // items_per_page
                state["current_item"] = max(
                    state["current_item"] - items_per_page // list_columns,
                    0
                )
                current_page = state["current_item"] // items_per_page
                if old_page != current_page:
                    changed = True
                    display.update_speed(badger2040.UPDATE_TURBO)
                time.sleep(BUTTON_PRESS_DELAY)
                
        elif display.pressed(badger2040.BUTTON_B):
            state["checked"][state["current_item"]] = not state["checked"][state["current_item"]]
            changed = True
            time.sleep(BUTTON_PRESS_DELAY)
            
        elif display.pressed(badger2040.BUTTON_C):
            if state["current_item"] < len(list_items) - 1:
                last_highlighted_item = state["current_item"]
                old_page = state["current_item"] // items_per_page
                state["current_item"] = min(
                    state["current_item"] + items_per_page // list_columns,
                    len(list_items) - 1
                )
                current_page = state["current_item"] // items_per_page
                if old_page != current_page:
                    changed = True
                    display.update_speed(badger2040.UPDATE_TURBO)
                time.sleep(BUTTON_PRESS_DELAY)

    if changed:
        badger_os.state_save("list", state)
        
        if len(list_items) > 0:
            # Calculate positions for old and new items
            if last_highlighted_item is not None:
                old_y = (last_highlighted_item % (LIST_HEIGHT // ITEM_SPACING)) * ITEM_SPACING
                old_x = (last_highlighted_item // (LIST_HEIGHT // ITEM_SPACING)) * (LIST_WIDTH // list_columns)
                
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
            new_y = (state["current_item"] % (LIST_HEIGHT // ITEM_SPACING)) * ITEM_SPACING
            new_x = (state["current_item"] // (LIST_HEIGHT // ITEM_SPACING)) * (LIST_WIDTH // list_columns)
            
            # Draw highlight bar
            display.pen(12)  # Gray
            display.rectangle(
                new_x,
                LIST_START + new_y - 4,
                LIST_WIDTH // list_columns,
                13
            )
            
            # Draw new item
            display.pen(0)
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
            
            # Draw navigation bar and arrows
            display.pen(12)  # Gray
            display.rectangle(WIDTH - ARROW_WIDTH, 0, ARROW_WIDTH, HEIGHT)
            
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
            
            # Only redraw the center checkbox if it changed
            if display.pressed(badger2040.BUTTON_B):
                if state["checked"][state["current_item"]]:
                    draw_cross(
                        (WIDTH // 2) - (ARROW_WIDTH // 2),
                        HEIGHT - ARROW_HEIGHT,
                        ARROW_HEIGHT,
                        ARROW_HEIGHT,
                        ARROW_THICKNESS,
                        ARROW_PADDING
                    )
                else:
                    draw_tick(
                        (WIDTH // 2) - (ARROW_WIDTH // 2),
                        HEIGHT - ARROW_HEIGHT,
                        ARROW_HEIGHT,
                        ARROW_HEIGHT,
                        ARROW_THICKNESS,
                        ARROW_PADDING
                    )
            
            display.update()
            
            # Reset to normal speed after update
            if is_on_battery():
                display.update_speed(badger2040.UPDATE_NORMAL)
            
        changed = False
        
    display.halt()
