import time
from ctypes import windll

import winsound
from BlurWindow.blurWindow import blur
from customtkinter import *

from helper import *

timer = time.perf_counter()
passed = 0
paused = False
duration = 50 * 60
text_area = pomo_count = False
playing = False


def start():
    global timer, paused, passed, playing

    start_playing()
    if paused:
        timer = time.perf_counter() - passed
        paused = False
    else:
        timer = time.perf_counter()

    refresh()


def pause():
    global paused, playing
    stop_playing()
    paused = True


def stop():
    global paused, timer
    counter = get_counter()

    stop_playing()
    timer = time.perf_counter()
    increment_counter(counter)
    refresh()
    paused = True


def draw():
    global text_area, pomo_count, timer, duration
    counter = get_counter()
    counter = init_counter(counter)

    total_seconds = round(duration - time.perf_counter() + timer)
    minutes = "{:02d}".format(total_seconds // 60)
    seconds = "{:02d}".format(total_seconds - (total_seconds // 60) * 60)

    start_button = CTkButton(master=root, text="Start", command=start, width=110, height=60, font=("Lato", 16))
    pause_button = CTkButton(master=root, text="Pause", command=pause, width=110, height=60, font=("Lato", 16))
    stop_button = CTkButton(master=root, text="Stop", command=stop, width=110, height=60, font=("Lato", 16))
    text_area = CTkLabel(master=root, text=f"{minutes}:{seconds}", font=("Arial", 25), height=130, bg_color="darkgreen")

    pomo_count = CTkLabel(master=root, text=f"Pomos: {counter[str(date.today())]}",
                          font=("Arial", 18), text_color="darkgrey", height=10, bg_color="darkgreen")
    mute_sound = CTkLabel(master=root, text="🔇", font=("Arial", 25), bg_color="darkgreen")

    # place widgets into window container using a layout
    start_button.grid(row=0, column=0)
    pause_button.grid(row=0, column=1)
    stop_button.grid(row=0, column=2)
    text_area.grid(row=3, column=0, columnspan=3, rowspan=3)
    pomo_count.grid(row=5, column=2, rowspan=3)
    mute_sound.grid(row=5, column=0, rowspan=3)
    mute_sound.bind("<Button-1>", lambda _: switch_playing())


def start_playing():
    global playing
    playing = True
    winsound.PlaySound('40hz.wav', winsound.SND_LOOP + winsound.SND_ASYNC)


def stop_playing():
    global playing
    playing = False
    winsound.PlaySound(None, winsound.SND_PURGE)


def switch_playing():
    global playing
    if playing:
        playing = False
        winsound.PlaySound(None, winsound.SND_PURGE)
    else:
        playing = True
        winsound.PlaySound('40hz.wav', winsound.SND_LOOP + winsound.SND_ASYNC)


def refresh():
    global text_area, pomo_count, paused, passed, duration
    counter = get_counter()

    if paused:
        passed = time.perf_counter() - timer
    else:
        total_seconds = round(duration - time.perf_counter() + timer)
        minutes = "{:02d}".format(total_seconds // 60)
        seconds = "{:02d}".format(total_seconds - (total_seconds // 60) * 60)
        text_area.configure(text=f"{minutes}:{seconds}")
        pomo_count.configure(text=f"Pomos: {counter[str(date.today())]}")
        if minutes == seconds == "00" or total_seconds < 0:
            stop_playing()
            winsound.PlaySound('done.wav', winsound.SND_ASYNC)
            increment_counter(counter)
            return
        root.after(1000, refresh)


set_appearance_mode("System")
root = CTk()
root.title("Pomodoro")
root.iconbitmap("pomodoro.ico")
root.resizable(False, False)
root.geometry("330x200")

# Add blur
root.config(bg='darkgreen')
root.wm_attributes("-transparent", 'darkgreen')
root.update()
hWnd = windll.user32.GetForegroundWindow()
blur(hWnd)

# Draw buttons and labels
draw()
root.mainloop()
