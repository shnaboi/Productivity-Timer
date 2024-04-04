from tkinter import *
import math
import pygame

BIG_FONT = ("Arial", 23, "bold")
TIMER_FONT = ("Courier New", 23, "bold")
SMALL_FONT = ("Courier New", 10, "normal")
intervals = None
timer = None


def start_timer(*args):
  global intervals, timer
  # calculate work & rest time in seconds
  work_int, rest_int = update_final_calc()
  work_sec = math.floor(work_int * 60)
  rest_sec = math.floor(rest_int * 60)
  # determine if timer is on a work interval or break interval
  # inside each if/else block, countdown(work_int) OR countdown(rest_int) is called
  if intervals == None:
    break_amount = (int(breaks_scale.get()))
    intervals = (break_amount * 2) + 1
  print(f"intervals = {intervals}")
  button_reset.config(state=ACTIVE)
  button_start.config(state=DISABLED)
  manage_controls(True)
  if intervals == 0:
    window.after_cancel(timer)
    timer_label.config(text=timer_text)
    manage_controls(False)
    return
  elif intervals % 2 == 0:
    #   rest interval
    bring_to_front(intervals)
    countdown(rest_sec)
  else:
    #   work interval
    bring_to_front(intervals)
    countdown(work_sec)

  print(work_sec, rest_sec)


def countdown(time_in_sec):
  global intervals, timer
  min = math.floor(time_in_sec / 60)
  sec = (time_in_sec % 60)
  if sec < 10:
    timer_label.config(text=f"{min}:0{sec}")
  else:
    timer_label.config(text=f"{min}:{sec}")
  if time_in_sec >= 0:
    timer = window.after(999, countdown, time_in_sec - 1)
  else:
    intervals -= 1
    start_timer()


def reset_timer():
  global intervals, timer
  window.after_cancel(timer)
  intervals = None
  timer_label.config(text="00:00")
  button_start.config(state=ACTIVE)
  button_reset.config(state=DISABLED)


def check_start():
  #   Start button not pushable until total time is defined
  if calc_total_time() == 0:
    button_start.config(state=DISABLED)
  else:
    button_start.config(state=ACTIVE)


def time_adjusted():
  update_final_calc()
  calculate_rest_time(int(rest_scale.get()))


def breaks_adjusted(value):
  update_final_calc()
  return value


def rest_adjusted(value):
  calculate_rest_time(value)
  update_final_calc()


def calc_total_time():
  hours = int(spinbox_hour.get())
  mins = int(spinbox_min.get())
  total_mins = int((hours * 60) + mins)
  return total_mins


def calculate_rest_time(value):
  total_mins = calc_total_time()
  final_calc = round(total_mins * (int(value) * .01), 2)
  rest_time_calc_label.config(text=f"{final_calc}\nrest mins")
  return final_calc


def update_final_calc():
  global intervals
  total_rest_mins = calculate_rest_time(int(rest_scale.get()))
  total_work_mins = calc_total_time() - total_rest_mins
  break_amount = (int(breaks_scale.get()))
  try:
    rest_int = round(total_rest_mins / break_amount, 2)
    work_int = round(total_work_mins / (break_amount + 1), 2)
    if rest_int == 0:
      final_label.config(text=f"{calc_total_time()} min\nwork interval\n\n"
                              f"0.0 min\nrest interval")
    else:
      final_label.config(text=f"{work_int} min\nwork interval\n\n"
                              f"{rest_int} min\nrest interval")
    check_start()
    return work_int, rest_int
  except ZeroDivisionError:
    if int(breaks_scale.get()) == 0:
      final_label.config(text=f"{calc_total_time()} min\nwork interval\n\n"
                              f"0.0 min\nrest interval")
      check_start()
      return total_work_mins, 0


def bring_to_front(int):
  window.lift()
  window.attributes('-topmost', True)
  window.attributes('-topmost', False)

#   play sound
  if int % 2 == 0:
  #   rest int started
    pygame.mixer.init()
    pygame.mixer.music.load("./audio/timer_end.mp3")
    pygame.mixer.music.play()
  else:
    #   work int started
    pygame.mixer.init()
    pygame.mixer.music.load("./audio/timer_start.mp3")
    pygame.mixer.music.play()

def manage_controls(bool):
  if bool == True:
    spinbox_hour.config(state=DISABLED)
    spinbox_min.config(state=DISABLED)
    rest_scale.config(state=DISABLED)
    breaks_scale.config(state=DISABLED)
  else:
    spinbox_hour.config(state=NORMAL)
    spinbox_min.config(state=NORMAL)
    rest_scale.config(state=NORMAL)
    breaks_scale.config(state=NORMAL)

# UI

window = Tk()
window.title("Productive Timer")
window.minsize(width=467, height=407)
window.maxsize(width=467, height=407)
window.config(pady=25, padx=25)

# Label: (title) Productivity Timer (use your time efficiently)
title = Label(text="time it.", font=BIG_FONT)
title.grid(row=0, column=3)

# Timer: the 00:00 looking part
timer_text = "00:00"
timer_label = Label(text=timer_text, font=TIMER_FONT)
timer_label.grid(row=1, column=3)

control_frame = LabelFrame(text="Controls", width=420, height=150)
control_frame.grid(row=2, rowspan=4, column=0, columnspan=5)

# Total Time spent (How many minutes do you have to work)
time_input_label = Label(text="Total Time", font=SMALL_FONT)
time_input_label.grid(row=3, column=0, columnspan=3, sticky=S)
# Spinboxes
spinbox_hour = Spinbox(from_=0, to=10, width=3, command=time_adjusted)
spinbox_hour.grid(row=4, column=0, sticky=E)
spinbox_and = Label(text="&", font=SMALL_FONT)
spinbox_and.grid(row=4, column=1)
spinbox_min = Spinbox(from_=0, to=59, width=3, command=time_adjusted)
spinbox_min.grid(row=4, column=2, sticky=W)
# Spinbox Labels
spinbox_hour_label = Label(text="Hour", font=SMALL_FONT)
spinbox_hour_label.grid(row=4, column=0, sticky=SE)
spinbox_min_label = Label(text="Min", font=SMALL_FONT)
spinbox_min_label.grid(row=4, column=2, sticky=SW)

# Rest Time
resting_label = Label(text="Rest Time %", font=SMALL_FONT)
resting_label.grid(row=3, column=3, sticky=S)
rest_scale = Scale(orient=HORIZONTAL, to=50, tickinterval=25, command=rest_adjusted)
rest_scale.grid(row=4, column=3, sticky=N)
# Label: {Convert % to mins to show user}
rest_time_calc_label = Label(text="0.0\nrest mins", font=SMALL_FONT)
rest_time_calc_label.grid(row=5, column=3, sticky=N)

# Input: How many breaks would you like?
breaks_label = Label(text="Break Amount", font=SMALL_FONT)
breaks_label.grid(row=3, column=4, sticky=S)
breaks_scale = Scale(orient=HORIZONTAL, to=10, tickinterval=5, command=breaks_adjusted)
breaks_scale.grid(row=4, column=4, sticky=N)

# Buttons
buttons_frame = LabelFrame(text="Start/Reset", width=100, height=125)
buttons_frame.grid(row=6, rowspan=2, column=3)
button_start = Button(text="Start", overrelief="groove", pady=2, width=7, command=start_timer, state=DISABLED)
button_start.grid(row=6, column=3, sticky=S)
button_reset = Button(text="Reset", overrelief="groove", pady=2, width=7, state=DISABLED, command=reset_timer)
button_reset.grid(row=7, column=3)

# Label: Calculate (for total time avail, rest time, and break amount)
final_frame = LabelFrame(text="Final Calc", width=100, height=125)
final_frame.grid(row=6, rowspan=2, column=4)
final_label = Label(text="0 min\nwork interval\n\n0.0 min\nrest interval")
final_label.grid(row=6, column=4, rowspan=2)

# Directions
directions_frame = LabelFrame(text="Directions", width=120, height=127)
directions_frame.grid(row=6, rowspan=2, column=0, columnspan=3)
directions = Label(text="- Select total time\n- Choose % of time to spend resting\n- Select break interval amount")
directions.config(wraplength=100, justify=LEFT, anchor=S)
directions.grid(row=6, rowspan=3, column=0, columnspan=3)

window.mainloop()
