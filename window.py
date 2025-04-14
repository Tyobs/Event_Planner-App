import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter import filedialog
import os
import shutil
import re
import time
import random
import string
import json
import base64
import threading
import subprocess
import sys
import ctypes
import platform

window = Tk()
window.title("Event Planner")
window.geometry("800x600")
window.resizable(True, True)
window.iconbitmap("D:\LineX Icon Pack\eventbrite.png")
window.configure(bg="#000300")
window.attributes("-topmost", True)
window.attributes("-alpha", 0.95)
window.overrideredirect(False)
window.wm_attributes("-toolwindow", True)
image = tk.PhotoImage(file="D:\LineX Icon Pack\eventbrite.png")
lab = Label(window, image = image)
lab.pack()

window.mainloop()