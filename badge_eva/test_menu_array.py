import time
import machine
import badger2040

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
time1 = badge.readline()      # "15"
activity2 = badge.readline()  # "ontbijt"
time2 = badge.readline()      # "16"
activity3 = badge.readline()  # "schoenen"
time3 = badge.readline()      # "5"
activity4 = badge.readline()  # "douchen"
time4 = badge.readline()      # "20"
activity5 = badge.readline()  # "pootjes wassen"
time5 = badge.readline()      # "12"
activity6 = badge.readline()  # "pyama"
time6 = badge.readline()      # "7"

# List items taken from timer.txt 
activity_list_items = [activity1, activity2, activity3, activity4, activity5, activity6]
save_checklist = False

# Getting length of list
activity_list_length = len(activity_list_items)
i = 0

list_iter = iter(activity_list_items)
 
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))
print(next(list_iter))

print ("items in list ", activity_list_length)