import badger2040
import badger_os

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
time1 = badge.readline()      # "900" : 15mins
activity2 = badge.readline()  # "ontbijt"
time2 = badge.readline()      # "960" : 16mins
activity3 = badge.readline()  # "schoenen"
time3 = badge.readline()      # "300" : 5mins
activity4 = badge.readline()  # "douchen"
time4 = badge.readline()      # "1200" : 20mins
activity5 = badge.readline()  # "pootjes wassen"
time5 = badge.readline()      # "720" : 12mins
activity6 = badge.readline()  # "pyama"
time6 = badge.readline()      # "420" : 7mins


ACTIVITY_DURATION = (
    (activity1, time1),
    (activity2, time2),
    (activity3, time3),
    (activity4, time4),
    (activity5, time5),
    (activity6, time6)
)

WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

MENU_TEXT_SIZE = 0.5
MENU_SPACING = 16
MENU_WIDTH = 84
MENU_PADDING = 220  # number of pixels between lefthandside and menu

TEXT_INDENT = MENU_WIDTH + 10

ARROW_THICKNESS = 3
ARROW_WIDTH = 18
ARROW_HEIGHT = 14
ARROW_PADDING = 2

ACTIVITY_TEXT_SIZE = 0.57

# ------------------------------
#      Drawing functions
# ------------------------------

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


# Draw the frame of the reader
def draw_frame():
    display.pen(15)
    display.clear()
    display.pen(12)
#    display.rectangle(WIDTH - ARROW_WIDTH, 0, ARROW_WIDTH, HEIGHT)
    display.pen(0)
    display.thickness(ARROW_THICKNESS)



# Draw the fonts and menu
def draw_activity_menu():
    display.font("bitmap8")
    display.thickness(1)
    for i in range(len(ACTIVITY_DURATION)):
        activity0, time0 = ACTIVITY_DURATION[i]
        display.pen(0)
        if i == state["selected_activity"]:
            display.rectangle((MENU_PADDING - 5), i * MENU_SPACING, MENU_WIDTH, MENU_SPACING)
            display.pen(15)

        display.text(activity0, MENU_PADDING, (i * MENU_SPACING) + int((MENU_SPACING - 8) / 2), MENU_TEXT_SIZE)
        time0_m = int(time0) / 60
        time0_m_r= str(round(time0_m))
        display.text(time0_m_r +" mins", 180, 28, ACTIVITY_TEXT_SIZE)
    activity0, time0 = ACTIVITY_DURATION[state["selected_activity"]]
    #display.font(activity0)
    display.thickness(1)

    display.update()


# ------------------------------
#        Program setup
# ------------------------------

# Global variables
state = {"selected_activity": 0}
badger_os.state_load("timerstate", state)

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_FAST)

changed = not badger2040.woken_by_button()

# ------------------------------
#       Main program loop
# ------------------------------

while True:
    if display.pressed(badger2040.BUTTON_UP):
        state["selected_activity"] -= 1
        if state["selected_activity"] < 0:
            state["selected_activity"] = len(ACTIVITY_DURATION) - 1
        changed = True
    if display.pressed(badger2040.BUTTON_DOWN):
        state["selected_activity"] += 1
        if state["selected_activity"] >= len(ACTIVITY_DURATION):
            state["selected_activity"] = 0
        changed = True

    if changed:
        draw_frame()
        draw_activity_menu()
        badger_os.state_save("timerstate", state)
        print(state["selected_activity"])
        changed = False

    display.halt()

