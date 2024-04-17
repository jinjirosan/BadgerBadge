# Badge Platform papa - hardware platform v3.0
# (2022-2024) 
#
# launcher.py : v1.1-refactor 0.0.0

import badger2040
from machine import Pin, ADC
import time

# Constants for Battery and Display Configuration
MAX_BATTERY_VOLTAGE = 4.05
MIN_BATTERY_VOLTAGE = 3.2
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT
BATT_WIDTH = 50
BATT_HEIGHT = 25
BATT_BORDER = 2
BATT_TERM_WIDTH = 5
BATT_TERM_HEIGHT = 12
BATT_BAR_PADDING = 2
BATT_BAR_HEIGHT = BATT_HEIGHT - (BATT_BORDER * 2) - (BATT_BAR_PADDING * 2)
NUM_BATT_BARS = 4
measurement_count = 0  # Initialize measurement count
prev_voltage = None  # For storing previous voltage

# Setup display
display = badger2040.Badger2040()
display.update_speed(badger2040.UPDATE_FAST)

# Setup battery voltage measurement
vbat_adc = ADC(badger2040.PIN_BATTERY)
vref_adc = ADC(badger2040.PIN_1V2_REF)
vref_en = Pin(badger2040.PIN_VREF_POWER, Pin.OUT)
vref_en.value(0)

def draw_battery(level):
    x_offset, y_offset = 10, 10  # Adjusted to top left corner
    display.pen(0)  # Black for the outline and filled levels
    display.rectangle(x_offset, y_offset, BATT_WIDTH, BATT_HEIGHT)
    display.rectangle(x_offset + BATT_WIDTH, y_offset + (BATT_HEIGHT - BATT_TERM_HEIGHT) // 2, BATT_TERM_WIDTH, BATT_TERM_HEIGHT)
    display.pen(15)  # White inside the battery area
    display.rectangle(x_offset + BATT_BORDER, y_offset + BATT_BORDER, BATT_WIDTH - BATT_BORDER * 2, BATT_HEIGHT - BATT_BORDER * 2)
    if level > 0:
        display.pen(0)  # Black filled battery level
        length = (BATT_WIDTH - 2 * BATT_BORDER - (NUM_BATT_BARS - 1) * BATT_BAR_PADDING) // NUM_BATT_BARS
        for i in range(NUM_BATT_BARS):
            if level > i:
                pos = i * (length + BATT_BAR_PADDING)
                display.rectangle(x_offset + BATT_BORDER + BATT_BAR_PADDING + pos, y_offset + BATT_BORDER + BATT_BAR_PADDING, length, BATT_BAR_HEIGHT)

def display_metrics(voltage, percentage, voltage_diff, percentage_diff):
    display.pen(0)  # Black text for visibility
    x_pos = 70  # Right of the battery graphic
    y_pos = 10  # Top position, adjusted below the battery graphic
    scale = 0.4  # Adjust scale for better fit
    display.text(f'Voltage: {voltage:.5f}V', x_pos, y_pos, scale=scale)
    display.text(f'Battery: {percentage}%', x_pos, y_pos + 15, scale=scale)
    display.text(f'Measure: {measurement_count}', x_pos, y_pos + 30, scale=scale)
    display.text(f'V Diff: {voltage_diff:.5f}V', x_pos, y_pos + 45, scale=scale)
    display.text(f'% Diff: {percentage_diff:.2f}%', x_pos, y_pos + 60, scale=scale)
    display.update()

def display_debug_info():
    display.pen(0)  # Black text for high contrast on a white background
    y_start = 10 + 78  # Adjust this value as needed to position below other text
    scale = 0.4  # Smaller scale to fit more information
    display.text("Bar 1: 3.2 V - 3.4 V (25%)", 10, y_start, scale=scale)
    display.text("Bar 2: 3.4 V - 3.6 V (50%)", 10, y_start + 10, scale=scale)
    display.text("Bar 3: 3.6 V - 3.8 V (75%)", 10, y_start + 20, scale=scale)
    display.text("Bar 4: 3.8 V - 4.0 V (100%)", 10, y_start + 30, scale=scale)
    display.update()

# Initialize a list to store voltage measurements
voltage_measurements = []

def plot_voltage_graph():
    max_measurements = 15  # Set maximum measurements to display at once
    graph_width = 100  # Width of the graph
    graph_height = 80  # Height of the graph
    graph_x = WIDTH - graph_width  # Position the graph right at the edge of the display
    graph_y = HEIGHT - graph_height - 10  # Position the graph near the bottom with a small margin

    display.pen(15)  # White background for the graph area
    display.rectangle(graph_x, graph_y, graph_width, graph_height)

    # Draw axes for clarity
    display.pen(0)  # Black for axes
    display.line(graph_x, graph_y, graph_x, graph_y + graph_height)  # Y-axis
    display.line(graph_x, graph_y + graph_height, graph_x + graph_width, graph_y + graph_height)  # X-axis

    # Calculate space between each dot horizontally
    space_between_dots = graph_width / (max_measurements - 1) if max_measurements > 1 else 0

    last_x, last_y = None, None  # Variables to store the last point coordinates

    if len(voltage_measurements) > 0:
        pixel_per_volt = graph_width / (MAX_BATTERY_VOLTAGE - MIN_BATTERY_VOLTAGE)

        # Plot the voltage measurements evenly across the width
        for i, voltage in enumerate(voltage_measurements[-max_measurements:]):
            x = graph_x + int(i * space_between_dots)
            y = graph_y + graph_height - int((voltage - MIN_BATTERY_VOLTAGE) * (graph_height / (MAX_BATTERY_VOLTAGE - MIN_BATTERY_VOLTAGE)))
            
            # Plot larger dot (3x3 pixels)
            display.pen(0)  # Black dot for each measurement
            display.rectangle(x - 1, y - 1, 3, 3)  # Draw a small square to represent the dot

            # Connect this dot with the last one if it exists
            if last_x is not None and last_y is not None:
                display.line(last_x, last_y, x, y)

            last_x, last_y = x, y  # Update last point coordinates

            # Log the measurement value and its coordinates
            print(f"Measurement {i}: Voltage = {voltage:.2f}V, Coordinates = ({x}, {y})")

    display.update()







def test_plot_dots():
    graph_width = 100  # Width of the graph
    graph_height = 80  # Height of the graph
    graph_x = WIDTH - graph_width - 10  # Position the graph on the right
    graph_y = HEIGHT - graph_height - 10

    # Clear the graph area with a white background
    display.pen(15)
    display.rectangle(graph_x, graph_y, graph_width, graph_height)

    # Draw axes for reference
    display.pen(0)  # Black for axes
    display.line(graph_x, graph_y, graph_x, graph_y + graph_height)  # Y-axis
    display.line(graph_x, graph_y + graph_height, graph_x + graph_width, graph_y + graph_height)  # X-axis

    # Plot 20 dots along the x-axis within the graph range
    display.pen(0)  # Black dot for each measurement
    for i in range(20):
        x = graph_x + int(i * (graph_width / 19))  # Evenly space 20 dots across the width
        y = graph_y + graph_height // 2  # Place all dots in the middle of the graph's height
        display.pixel(x, y)

    display.update()


while True:
    vref_en.value(1)
    vdd = 1.24 * (65535 / vref_adc.read_u16())
    vbat = (vbat_adc.read_u16() / 65535) * 3 * vdd
    vref_en.value(0)
    voltage_percentage = int((vbat - MIN_BATTERY_VOLTAGE) / (MAX_BATTERY_VOLTAGE - MIN_BATTERY_VOLTAGE) * 100)
    level = int((vbat - MIN_BATTERY_VOLTAGE) / (MAX_BATTERY_VOLTAGE - MIN_BATTERY_VOLTAGE) * NUM_BATT_BARS)

    if prev_voltage is not None:
        voltage_diff = vbat - prev_voltage
        percentage_diff = (voltage_diff / prev_voltage) * 100 if prev_voltage != 0 else 0
    else:
        voltage_diff = 0.0
        percentage_diff = 0.0

    voltage_measurements.append(vbat)  # Append new measurement
    if len(voltage_measurements) > 50:  # Keep the list size manageable
        voltage_measurements.pop(0)


    display.pen(15)  # Set pen to white before clearing for a white background
    display.clear()
    draw_battery(level)
    # Call this function when you want to show the debug info on your display
    display_debug_info()
    display_metrics(vbat, voltage_percentage, voltage_diff, percentage_diff)
    plot_voltage_graph()  # Plot the graph with updated measurements
    #test_plot_dots()
    prev_voltage = vbat  # Update previous voltage
    measurement_count += 1

    time.sleep(60)  # Adjust the timing as needed

