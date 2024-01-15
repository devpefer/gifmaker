from time import sleep
import tkinter as tk
from PIL import Image, ImageTk
import pyautogui


class AreaSelection(tk.Toplevel):
    def __init__(self, master, callback, event):
        tk.Toplevel.__init__(self, master)
        self.inicializar()
        self.callback = callback
        self.event = event

    def inicializar(self):
        self.attributes("-alpha", 0.5)
        self.overrideredirect(True)
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}')

        screenshot = pyautogui.screenshot()
        screenshot = screenshot.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.BICUBIC)
        self.screenshot_img = ImageTk.PhotoImage(screenshot)

        self.canvas = tk.Canvas(self, width=self.winfo_screenwidth(), height=self.winfo_screenheight(), cursor="cross")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.screenshot_img)
        self.canvas.pack()

        self.start_x = None
        self.start_y = None

        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

    def on_press(self, event):
        self.start_x = event.x_root
        self.start_y = event.y_root

    def on_drag(self, event):
        cur_x = event.x_root
        cur_y = event.y_root

        self.canvas.delete("rect")

        self.canvas.create_rectangle(
            self.start_x - self.winfo_rootx(),
            self.start_y - self.winfo_rooty(),
            cur_x - self.winfo_rootx(),
            cur_y - self.winfo_rooty(),
            outline="red",
            width=2,
            tags="rect"
        )

    def on_release(self, event):
        cur_x = event.x_root
        cur_y = event.y_root
        self.destroy()
        sleep(0.5)

        self.callback(self.start_x, self.start_y, cur_x, cur_y)
        self.event.set()