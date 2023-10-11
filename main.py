import time
from ctypes import windll

import winsound
from BlurWindow.blurWindow import blur
from customtkinter import CTk, CTkLabel, CTkButton, set_appearance_mode

from helper import increment_counter, date, get_counter, init_counter

timer = None
passed = 0
paused = False
duration = 90 * 60
# noinspection PyTypeChecker
text_area: CTkLabel = None
# noinspection PyTypeChecker
pomo_count: CTkLabel = None
playing = False
# noinspection PyTypeChecker
root: CTk = None


def start():
    global timer, passed, playing, paused
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


def draw():
    global text_area, pomo_count, timer, duration, root
    counter = get_counter()
    counter = init_counter(counter)

    root = CTk()
    root.title("Pomodoro")
    root.iconbitmap("pomodoro.ico")
    root.resizable(False, False)
    root.geometry("330x200")

    root.config(bg='darkgreen')
    root.wm_attributes("-transparent", 'darkgreen')
    root.update()
    window = windll.user32.GetForegroundWindow()
    blur(window)

    start_button = CTkButton(master=root, text="Start", command=start, width=110, height=60, font=("Lato", 16))
    pause_button = CTkButton(master=root, text="Pause", command=pause, width=110, height=60, font=("Lato", 16))
    stop_button = CTkButton(master=root, text="Stop", command=stop, width=110, height=60, font=("Lato", 16))
    text_area = CTkLabel(master=root, text="00:00", font=("Arial", 25), height=130, bg_color="darkgreen")
    pomo_count = CTkLabel(master=root, text=f"Count: {counter[str(date.today())]}", font=("Arial", 18),
                          text_color="darkgrey", height=10, bg_color="darkgreen")

    start_button.grid(row=0, column=0)
    pause_button.grid(row=0, column=1)
    stop_button.grid(row=0, column=2)
    text_area.grid(row=3, column=0, columnspan=3, rowspan=3)
    pomo_count.grid(row=5, column=2, rowspan=3)

    root.mainloop()


def start_playing():
    global playing
    playing = True
    winsound.PlaySound('40hz.wav', winsound.SND_LOOP + winsound.SND_ASYNC)


def stop_playing():
    global playing
    playing = False
    winsound.PlaySound(None, winsound.SND_PURGE)


# noinspection PyTypeChecker
def refresh():
    global text_area, pomo_count, paused, passed, duration, root
    counter = get_counter()

    if paused:
        passed = time.perf_counter() - timer
    else:
        total_seconds = round(duration - time.perf_counter() + timer)
        minutes = "{:02d}".format(total_seconds // 60)
        seconds = "{:02d}".format(total_seconds - (total_seconds // 60) * 60)
        text_area.configure(text=f"{minutes}:{seconds}")
        pomo_count.configure(text=f"Count: {counter[str(date.today())]}")
        if minutes == seconds == "00" or total_seconds < 0:
            stop_playing()
            winsound.PlaySound('done.wav', winsound.SND_ASYNC)
            increment_counter(counter)
            return
        root.after(1000, refresh)


set_appearance_mode("System")
draw()
