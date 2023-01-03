import tkinter
import time
import winsound
from customtkinter import *

timer = time.perf_counter()
passed = 0
paused = False
duration = 50 * 60
text_area = False


def start():
    global timer, paused, passed
    winsound.PlaySound('40hz.wav', winsound.SND_LOOP + winsound.SND_ASYNC)
    if paused:
        timer = time.perf_counter() - passed
        paused = False
    else:
        timer = time.perf_counter()

    refresh()


def pause():
    global paused
    winsound.PlaySound(None, winsound.SND_PURGE)
    paused = True


def stop():
    global paused, timer
    winsound.PlaySound(None, winsound.SND_PURGE)
    timer = time.perf_counter()
    refresh()
    paused = True


def draw():
    global text_area, timer, duration
    total_seconds = round(duration - time.perf_counter() + timer)
    minutes = "{:02d}".format(total_seconds // 60)
    seconds = "{:02d}".format(total_seconds - (total_seconds // 60) * 60)

    start_button = CTkButton(master=root, text="Start", command=start, width=110, height=60)
    pause_button = CTkButton(master=root, text="Pause", command=pause, width=110, height=60)
    stop_button = CTkButton(master=root, text="Stop", command=stop, width=110, height=60)
    text_area = CTkLabel(master=root, text=f"{minutes}:{seconds}", font=("Arial", 25), height=130)

    # place widgets into window container using a layout
    start_button.grid(row=0, column=0)
    pause_button.grid(row=0, column=1)
    stop_button.grid(row=0, column=2)
    text_area.grid(row=3, column=0, columnspan=3, rowspan=3)


def refresh():
    global text_area, paused, passed, duration
    if paused:
        passed = time.perf_counter() - timer
    else:
        total_seconds = round(duration - time.perf_counter() + timer)
        minutes = "{:02d}".format(total_seconds // 60)
        seconds = "{:02d}".format(total_seconds - (total_seconds // 60) * 60)
        text_area.configure(text=f"{minutes}:{seconds}")
        if minutes == seconds == "00":
            winsound.PlaySound(None, winsound.SND_PURGE)
            winsound.PlaySound('done.wav', winsound.SND_ASYNC)
            return
        root.after(1000, refresh)


set_appearance_mode("System")
root = CTk()
root.title("Pomodoro")
root.geometry("330x200")
root.configure()
root.iconbitmap("pomodoro.ico")
draw()
root.mainloop()
