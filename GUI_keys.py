from key_press import start_keys, stop_keys
import tkinter as tk
from tkinter import ttk
import multiprocessing as mp

def button_1():
    global var1
    if var1.get() == 1:
        start_keys()
    else:
        stop_keys()
def button_2():
    global var2
    if var2.get() == 1:
        new_process_start_auto_worker()
    else:
        stop_process(p1)

def check_process(p):
    if p.is_alive():
        root.after(500, check_process, p)
def stop_process(p):
    if p.is_alive():
        p.terminate()
        p.join()

def new_process_ttt():
    global p2
    p2 = mp.Process(target=process_ttt)
    p2.start()
    check_process(p2)
def process_ttt():
    from ttt import ttt_main
    ttt_main()

def new_process_start_auto_worker():
    global p1
    p1 = mp.Process(target=process_start_auto_worker)
    p1.start()
    check_process(p1)
def process_start_auto_worker():
    from tgbot import start_auto_worker
    start_auto_worker()

def on_closing():
    if var2.get() == 1:
        stop_process(p1)
    stop_process(p2)
    root.destroy()
    exit()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width - width) // 2 - 25
    y = (screen_height - height) // 2 - 25

    window.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    mp.freeze_support()

    root = tk.Tk()
    root.title("Tg Keys")
    center_window(root, 220, 110)
    root.resizable(False, False)

    var1 = tk.IntVar()
    var2 = tk.IntVar()

    # Створення контейнера для розміщення перемикачів з лівого боку
    style = ttk.Style()
    style.configure("TCheckbutton", font=("Helvetica", 16), indicatoron=True, padding=5)
    style.map("TCheckbutton",
            indicatorcolor=[("selected", "black"), ("!selected", "white")],
            indicatordiameter=[("selected", 20), ("!selected", 20)])

    # Створення контейнера для розміщення перемикачів з лівого боку
    frame = ttk.Frame(root)
    frame.pack(side=tk.TOP, padx=0, pady=0)

    # Створення перемикачів
    button1 = ttk.Checkbutton(frame, text="Клавіші", variable=var1, command=button_1, style="TCheckbutton").pack(anchor=tk.W)
    button2 = ttk.Checkbutton(frame, text="Перебиралка", variable=var2, command=button_2, style="TCheckbutton").pack(anchor=tk.W)

    var1.set(1)
    button_1()

    # var2.set(1)
    # button_2()

    new_process_ttt()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


