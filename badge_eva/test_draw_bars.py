import badger2040
import badger_os
import time


WIDTH = badger2040.WIDTH # 296
HEIGHT = badger2040.HEIGHT # 128

TITLE_SIZE = 0.56
TIME_TEXT_SIZE = 1.0

time_sec = 16
total_bars = 6

draw_6bars_run_once = False
draw_5bars_run_once = False
draw_4bars_run_once = False
draw_3bars_run_once = False
draw_2bars_run_once = False
draw_1bars_run_once = False

def calculate_bar_length(total_bars, activity_time):
    bar_duration = activity_time / total_bars
    d0 = [(i * bar_duration, (i + 1) * bar_duration) for i in range(total_bars)]
    #print("total bars (d0): ", d0) #debug
    d1 = (d0[0])
    #print("first bar size(d1): ", d0[0]) #debug
    d2 = [item[0] for item in d0]
    #print("get every second bar time (d2): ", d2) #debug
    d3 = d2[1]
    #print("bar duration unit (d3): ", d3) #debug
    d4 = d3 * 6
    #print("verification back to total time_sec (d4): ", round(d4)) #debug
    d5 = round(d3,2)
    #print("rounded d3 to two digits (d5): ", d5) #keep this as function output only
    return d5, d4


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


# draw the timer framework
def draw_timer_framework():
    display.led(128)
    display.pen(15)
    display.clear()
    # Set display parameters
    display.pen(15)
    display.font("sans")
    display.thickness(2)
    # black box on top
    display.pen(0)
    display.rectangle(0, 0, 296, 22)
    display.pen(15)
    display.text("Hoelang heb ik de tijd ?", 30, 10, TITLE_SIZE)
    display.pen(0)
    display.line(0, 39, 296, 39)
    display.line(0, 101, 296, 101)
    display.pen(0)
    display.thickness(1)
    #activity0, time0 = ACTIVITY_DURATION[state["selected_activity"]]
    #display.text(activity0, 5, 28, ACTIVITY_TEXT_SIZE)
    #time0_m = int(time0) / 60
    #time0_m_r= str(round(time0_m))
    #display.text(time0_m_r +" mins", 220, 28, ACTIVITY_TEXT_SIZE)
    #display.text(str(round(time1_m)), 180, 50, TIME_TEXT_SIZE)
    display.thickness(2)
    display.update()

def draw_bars():
    display.update_speed(badger2040.UPDATE_TURBO)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    #display.update()


def draw_6bars():
    global draw_6bars_run_once
    if draw_6bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_TURBO)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    display.update()
    draw_6bars_run_once = True

def draw_5bars():
    global draw_5bars_run_once
    if draw_5bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_TURBO)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.pen(8)
    display.line(185, 92, 205, 92) # bar 6
    draw_5bars_run_once = True
    display.update()

def draw_4bars():
    global draw_4bars_run_once
    if draw_4bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_TURBO)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.pen(8)
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    draw_4bars_run_once = True
    display.update()

def draw_3bars():
    global draw_3bars_run_once
    if draw_3bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_TURBO)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.pen(8)
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    draw_3bars_run_once = True
    display.update()

def draw_2bars():
    global draw_2bars_run_once
    if draw_2bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_TURBO)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.pen(8)
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    draw_2bars_run_once = True
    display.update()

def draw_1bars():
    global draw_1bars_run_once
    if draw_1bars_run_once:
        return
    display.update_speed(badger2040.UPDATE_TURBO)
    display.pen(0)
    display.thickness(6)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.pen(8)
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    draw_1bars_run_once = True
    display.update()


def countdown(time_sec):
    #display.update_speed(badger2040.UPDATE_TURBO)
    while time_sec:
        mins, secs = divmod(time_sec, 60)
        timeformat = '{:02d}:{:02d}'.format(mins,secs)
        print(timeformat, end='\r')
        print("bar_length", bar_length)
        print("time_sec", time_sec)
        if time_sec > bar_length * 5:
            draw_6bars()
        if time_sec > bar_length * 4 and time_sec < bar_length * 5:
            draw_5bars()
        if time_sec > bar_length * 3 and time_sec < bar_length * 4:
            draw_4bars()
        if time_sec > bar_length * 2 and time_sec < bar_length * 3:
            draw_3bars()
        if time_sec > bar_length * 1 and time_sec < bar_length * 2:
            draw_2bars()
        if time_sec  < bar_length * 1:
            draw_1bars()
        display.led(128)
        time.sleep(1)
        time_sec -= 1
        display.led(0)
        #display.pen(15)
        #display.rectangle(100, 45, 100, 30)
        #display.pen(0)
        #display.thickness(2)
        #display.text(timeformat, 100, 60, TIME_TEXT_SIZE)
        #display.update()
    print("stoppppp")
    display.pen(8)
    display.line(10, 92, 30, 92) # bar 1 - 20px long, 15px break
    display.line(45, 92, 65, 92) # bar 2
    display.line(80, 92, 100, 92) # bar 3
    display.line(115, 92, 135, 92) # bar 4
    display.line(150, 92, 170, 92) # bar 5
    display.line(185, 92, 205, 92) # bar 6
    display.pen(0)
    display.rectangle(100, 45, 100, 30)
    display.pen(15)
    display.text("KLAAR", 100, 60, TIME_TEXT_SIZE)
    display.update()

# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
display.led(128)

draw_timer_framework()
#draw_5bars()
bar_length, total_time = calculate_bar_length(total_bars,time_sec)

countdown(time_sec)

print(bar_length, type(bar_length))
print(round(total_time), type(total_time))

display.led(0)