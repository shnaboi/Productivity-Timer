from tkinter import *
import math

BIG_FONT = ("Courier New", 23, "bold")
SMALL_FONT = ("Courier New", 10, "normal")

# UI

window = Tk()
window.title("Productive Timer")
window.minsize(width=420, height=420)
window.config(pady=25, padx=25)

# Label: (title) Productivity Timer (use your time efficiently)
title = Label(text="time it.", font=BIG_FONT)
title.grid(row=0, column=3)

# Timer: the 00:00 looking part
timer_text = "00:00"
timer_label = Label(text=timer_text, font=BIG_FONT)
timer_label.grid(row=1, column=3)

# Total Time spent (How many minutes do you have to work)
time_input_label = Label(text="Total Time\nAvailable:", font=SMALL_FONT)
time_input_label.grid(row=3, column=0, columnspan=3)
# Spinboxes
spinbox_hour = Spinbox(from_=0, to=10, width=3)
spinbox_hour.grid(row=4, column=0)
spinbox_and = Label(text="&", font=SMALL_FONT)
spinbox_and.grid(row=4, column=1, sticky="W")
spinbox_min = Spinbox(from_=0, to=59, width=3)
spinbox_min.grid(row=4, column=2)
# Spinbox Labels
spinbox_hour_label = Label(text="Hour", font=SMALL_FONT)
spinbox_hour_label.grid(row=5, column=0, sticky=N)
spinbox_min_label = Label(text="Min", font=SMALL_FONT)
spinbox_min_label.grid(row=5, column=2, sticky=N)

# Rest Time
def calculate_rest_time(value):
  hours = int(spinbox_hour.get())
  mins = int(spinbox_min.get())
  total_mins = int((hours * 60) + mins)
  final_calc = round(total_mins * (int(value)*.01), 1)
  rest_time_calc_label.config(text=f"{final_calc}\nrest mins")

resting_label = Label(text="Rest Time\n%", font=SMALL_FONT)
resting_label.grid(row=3, column=3)
rest_scale = Scale(orient=HORIZONTAL, to=50, tickinterval=25, command=calculate_rest_time)
rest_scale.grid(row=4, column=3)
# Label: {Convert % to mins to show user}
rest_time_calc_label = Label(text="0.0\nrest mins", font=SMALL_FONT)
rest_time_calc_label.grid(row=5, column=3)

# Input: How many breaks would you like?
breaks_label = Label(text="Break\nIntervals", font=SMALL_FONT)
breaks_label.grid(row=3, column=4)
breaks_scale = Scale(orient=HORIZONTAL, to=10, tickinterval=5)
breaks_scale.grid(row=4, column=4)

buttons_frame = LabelFrame(text="Control Buttons", width=100, height=100)
buttons_frame.grid(row=6, rowspan=2, column=3, sticky=S)
# buttons_frame.grid_propagate(1)
button = Button(text="Start", overrelief="groove", pady=2, width=7)
button.grid(row=6, column=3, sticky=S)
button2 = Button(text="Reset", overrelief="groove", pady=2, width=7, state=DISABLED)
button2.grid(row=7, column=3)


# Label: Calculate (for total time avail, rest time, and break amount)

# show: [2] 5min breaks after each 25min work period [60mins total])

# Start button
# Reset button



window.mainloop()
