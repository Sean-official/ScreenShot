import subprocess
from tkinter import messagebox
from tkinter import *
import keyboard
import pyautogui


def shell(cmd):
    result = subprocess.getstatusoutput(cmd)
    if result[0] != 0:
        messagebox.showerror("警告", "在执行命令时出现问题")
    return result[1]


def ocr(name):
    def start_ocr():
        window.destroy()
        shell(f"python analyze.py output\\{name}.jpeg")

    def pack_center(_window: Tk, width, height):
        _window.geometry(
            f"{width}x{height}+{int((_window.winfo_screenwidth() - width) / 2)}+{int((_window.winfo_screenheight() - height) / 2)}")

    window = Tk()
    window.title("Ask")
    window.attributes("-topmost", True)
    pack_center(window, 200, 100)
    window.resizable(False, False)

    Label(window, text="Recognize the image?").grid(row=1, column=1, columnspan=2)
    Button(window, text="Yes", command=start_ocr).grid(row=2, column=1)
    Button(window, text="No", command=window.destroy).grid(row=2, column=2)
    window.mainloop()


def start():
    global times, x1, x2, y1, y2
    if times == 0:
        x1, y1 = pyautogui.position()
        times += 1
        return
    if times == 1:
        x2, y2 = pyautogui.position()
        name = 1
        while True:
            if shell(f"if exist output\\{name}.jpeg (echo 1) else (echo 0)") == "1":
                name += 1
            else:
                break
        img = pyautogui.screenshot(region=(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2)))
        print(x1, y1)
        print(x2, y2)
        print(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))
        img.save(f"output\\{name}.jpeg")
        times = 0
        ocr(name)
        return


def close():
    def pack_center(_window: Tk, width, height):
        _window.geometry(
            f"{width}x{height}+{int((_window.winfo_screenwidth() - width) / 2)}+{int((_window.winfo_screenheight() - height) / 2)}")

    window = Tk()
    window.title("Info")
    window.attributes("-topmost", True)
    pack_center(window, 250, 40)
    window.resizable(False, False)
    Label(window, text="Program Exited Successfully！").pack()
    window.mainloop()


x1, y1, x2, y2 = 0, 0, 0, 0
times = 0
keyboard.add_hotkey("ctrl+q", start)
keyboard.wait("ctrl+e")
close()
