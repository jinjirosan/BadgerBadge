import binascii

import badger2040
import badger_os

# Global Constants
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

ARROW_THICKNESS = 3
ARROW_WIDTH = 18
ARROW_HEIGHT = 14
ARROW_PADDING = 2



# Draw a upward arrow
def draw_up(x, y, width, height, thickness, padding):
    border = (thickness // 4) + padding
    display.line(x + border, y + height - border,
                 x + (width // 2), y + border)
    display.line(x + (width // 2), y + border,
                 x + width - border, y + height - border)


# Draw a downward arrow
def draw_down(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(x + border, y + border,
                 x + (width // 2), y + height - border)
    display.line(x + (width // 2), y + height - border,
                 x + width - border, y + border)


# Draw a left arrow
def draw_left(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(x + width - border, y + border,
                 x + border, y + (height // 2))
    display.line(x + border, y + (height // 2),
                 x + width - border, y + height - border)


# Draw a right arrow
def draw_right(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(x + border, y + border,
                 x + width - border, y + (height // 2))
    display.line(x + width - border, y + (height // 2),
                 x + border, y + height - border)


# Draw a tick
def draw_tick(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(x + border, y + ((height * 2) // 3),
                 x + (width // 2), y + height - border)
    display.line(x + (width // 2), y + height - border,
                 x + width - border, y + border)


# Draw a cross
def draw_cross(x, y, width, height, thickness, padding):
    border = (thickness // 2) + padding
    display.line(x + border, y + border, x + width - border, y + height - border)
    display.line(x + width - border, y + border, x + border, y + height - border)


# Draw a checkbox with or without a tick
def draw_checkbox(x, y, size, background, foreground, thickness, tick, padding):
    border = (thickness // 2) + padding
    display.pen(background)
    display.rectangle(x + border, y + border, size - (border * 2), size - (border * 2))
    display.pen(foreground)
    display.thickness(thickness)
    display.line(x + border, y + border, x + size - border, y + border)
    display.line(x + border, y + border, x + border, y + size - border)
    display.line(x + size - border, y + border, x + size - border, y + size - border)
    display.line(x + border, y + size - border, x + size - border, y + size - border)
    if tick:
        draw_tick(x, y, size, size, thickness, 2 + border)


# ------------------------------
#        Program setup
# ------------------------------

changed = not badger2040.woken_by_button()



# Global variables
items_per_page = 0

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
display.led(128)
if changed:
    display.update_speed(badger2040.UPDATE_FAST)
else:
    display.update_speed(badger2040.UPDATE_TURBO)

# ------------------------------
#       Main program loop
# ------------------------------

draw_up(WIDTH - ARROW_WIDTH, (HEIGHT // 4) - (ARROW_HEIGHT // 2), ARROW_WIDTH, ARROW_HEIGHT, ARROW_THICKNESS, ARROW_PADDING)

draw_down(WIDTH - ARROW_WIDTH, ((HEIGHT * 3) // 4) - (ARROW_HEIGHT // 2), ARROW_WIDTH, ARROW_HEIGHT, ARROW_THICKNESS, ARROW_PADDING)

draw_left((WIDTH // 7) - (ARROW_WIDTH // 2), HEIGHT - ARROW_HEIGHT, ARROW_WIDTH, ARROW_HEIGHT, ARROW_THICKNESS, ARROW_PADDING)

draw_right(((WIDTH * 6) // 7) - (ARROW_WIDTH // 2), HEIGHT - ARROW_HEIGHT, ARROW_WIDTH, ARROW_HEIGHT, ARROW_THICKNESS, ARROW_PADDING)

display.update()
display.update_speed(badger2040.UPDATE_TURBO)
changed = False

display.led(0)
display.halt()

