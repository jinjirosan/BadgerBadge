import time
import machine
import badger2040

# We're going to keep the badger on, so slow down the system clock if on battery
badger2040.system_speed(badger2040.SYSTEM_SLOW)

rtc = machine.RTC()
display = badger2040.Badger2040()
display.led(128)
display.update_speed(badger2040.UPDATE_TURBO)
display.font("sans")

def draw_clock():
    hms = "{:02}:{:02}:{:02}".format(hour, minute, second)

    hms_width = display.measure_text(hms, 1.8)
    hms_offset = int((badger2040.WIDTH / 2) - (hms_width / 2))

    display.pen(15)
    display.clear()
    display.pen(0)
    display.thickness(5)
    display.text(hms, hms_offset, 40, 1.8)

    display.update()


year, month, day, wd, hour, minute, second, _ = rtc.datetime()

if (year, month, day) == (2021, 1, 1):
    rtc.datetime((2022, 2, 28, 0, 12, 0, 0, 0))

last_second = second

while True:
    year, month, day, wd, hour, minute, second, _ = rtc.datetime()
    if second != last_second:
          draw_clock()
          last_second = second
    time.sleep(0.01)
