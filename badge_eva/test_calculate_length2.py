import time

time_sec = 16
total_bars = 6

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

bar_length, total_time = calculate_bar_length(total_bars,time_sec)

print(bar_length, type(bar_length)) # type added for testing only
print(round(total_time), type(total_time)) # type added for testing only


time0_red = 1800
total_slices = 6


# Calculate the duration each slice needs to represent
def calculate_slice_length(total_slices, focus_time):
    slice_duration = focus_time / total_slices
    d0 = [(i * slice_duration, (i + 1) * slice_duration) for i in range(total_slices)]
    #print("total bars (d0): ", d0) #debug
    d1 = (d0[0])
    #print("first bar size(d1): ", d0[0]) #debug
    d2 = [item[0] for item in d0]
    #print("get every second bar time (d2): ", d2) #debug
    d3 = d2[1]
    #print("bar duration unit (d3): ", d3) #debug
    d4 = d3 * 6
    #print("verification back to total time0 (d4): ", round(d4)) #debug
    d5 = round(d3,2)
    #print("rounded d3 to two digits (d5): ", d5) #keep this as function output only
    return d5, d4



slice_duration, focus_time = calculate_slice_length(total_slices,int(time0_red))

print(slice_duration, type(slice_duration)) # type added for testing only
print(round(focus_time), type(focus_time)) # type added for testing only