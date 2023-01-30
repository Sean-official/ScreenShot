import subprocess
import sys
from tkinter import *
from tkinter import messagebox
from PIL import Image

import pytesseract


def shell(cmd):
    result = subprocess.getstatusoutput(cmd)
    if result[0] != 0:
        messagebox.showerror("警告", "在执行命令时出现问题")
    return result[1]


def select_all():
    flag = True
    for j in Vars:
        if j.var.get() == 0:
            flag = False
            break
    if flag:
        for j in Vars:
            j.var.set(0)
    else:
        for j in Vars:
            j.var.set(1)


def search(_lang: str):
    for j in Vars:
        if j.lang == _lang:
            return j
    raise RuntimeError("Language Not Found!")


class Var:
    def __init__(self, _obj: Checkbutton, _lang: None | str = None):
        self.button = _obj
        self.var = IntVar()
        self.button.config(variable=self.var)
        self.button.config(command=self.check)
        if _lang is None:
            self.lang = ""
        else:
            self.lang = _lang

    def check(self):
        if self.var.get() == 0:
            var.set(0)
        for j in Vars:
            if j.var.get() == 0:
                return
        var.set(1)

    def value(self):
        if self.var.get() == 1:
            return self.lang
        else:
            return ""


def start():
    option = ""
    flag = False
    for j in Vars:
        if j.var.get() == 1:
            if not flag:
                option += j.value()
            else:
                option += "+" + j.value()
            flag = True
    if not flag:
        messagebox.showerror("Error", "未选中语言！")
    print(f"Running pytesseract @ {option}")
    global data
    data = pytesseract.image_to_string(Image.open(path))
    print(data)
    root.destroy()


class ResultWindow:
    def __init__(self, _txt):
        self.window = Tk()
        self.window.title("OCR:Result")
        self.window.resizable(False, False)
        self.menu = Menu(self.window, tearoff=False)
        self.menu.add_command(label="Copy", command=self.copy)
        self.menu.add_command(label="Paste",command=self.paste)
        self.window.bind("<Button-3>",self.show_menu)
        self.txt = Text(self.window)
        self.txt.pack()
        try:
            self.txt.insert(END, _txt)
        except TypeError:
            for j in _txt:
                self.txt.insert(END, j)
        self.window.mainloop()

    def show_menu(self,event):
        self.menu.post(event.x_root,event.y_root)

    def copy(self):
        try:
            self.txt.clipboard_clear()
            copytext = self.txt.get(SEL_FIRST, SEL_LAST)
            self.txt.clipboard_append(copytext)
        except TclError:
            messagebox.showerror("Error", f"Error info:{SEL_FIRST},{SEL_LAST}")

    def paste(self):
        try:
            copyText = self.txt.selection_get(selection="CLIPBOARD")
            self.txt.insert(INSERT, copyText)
        except TclError:
            messagebox.showerror("Error","Nothing to paste")


data = ""
supported_languages = pytesseract.get_languages()
Vars: list[Var] = []
try:
    path = sys.argv[1]
except IndexError:
    path = input("Path:")
if shell(f"if exist {path} (echo 1) else (echo 0)") == "0":
    messagebox.showerror("Error", "File Not Found！")
    exit(0)
root = Tk()
root.title("OCR:Console")
root.resizable(False, False)
Label(root, text="识别选项", font=('微软雅黑', 15, 'bold')).grid(column=1, row=1)
column = 1
row = 2
for i in supported_languages:
    Vars.append(Var(_obj=Checkbutton(root, text=i, onvalue=1, offvalue=0, font=("consolas", 15)), _lang=i))
    search(i).button.grid(row=row, column=column)
    column += 1
    if column == 5:
        column = 1
        row += 1
var = IntVar()
whole = Checkbutton(root, text="All Languages", variable=var, onvalue=1, offvalue=0, font=("consolas", 15, "bold"),
                    command=select_all)
whole.grid(row=row + 1, column=1)
Button(root, text="开始", command=start).grid(row=row + 1, column=2, columnspan=3)
root.mainloop()
rw = ResultWindow(data)
