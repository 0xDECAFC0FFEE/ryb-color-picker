import tkinter as tk
from tkinter import ttk, Canvas
from utils import *
from PIL import ImageTk, Image
from collections import namedtuple

class ImageHandler():
    def __init__(self, root, frame, bg_updater):
        self.image_tk = None
        self.image = None
        self.w, self.h = None, None
        self.saved_x, self.saved_y = None, None
        self.prev_point = None
        self.root = root

        self.canvas = tk.Canvas(frame)
        self.canvas.pack()
        self.label = tk.Label(self.canvas, cursor="cross")
        self.label.place(x=0, y=0)

        self.label.bind('<Motion>', self.mouse_motion)
        self.label.bind('<Leave>', self.mouse_leave)
        self.label.bind('<Button-1>', self.mouse_left_click)
        self.bg_updater = bg_updater

        self.updateImage()

    def mouse_motion(self, event):
        x, y = event.x, event.y
        if x >= 0 and x < self.w and y >= 0 and y < self.h:
            r, g, b = self.image.getpixel((x, y))
            self.bg_updater.update_color((r, g, b))

    def mouse_leave(self, event):
        if self.saved_x != None and self.saved_y != None:
            r, g, b = self.image.getpixel((self.saved_x, self.saved_y))
            self.bg_updater.update_color((r, g, b))

    def update_saved_point(self, point):
        self.saved_x, self.saved_y = point
        # if self.canvas != None and point != (None, None):
        #     if self.prev_point != None:
        #         self.canvas.delete(self.prev_point)

            # self.line1_id = self.canvas.create_line(self.saved_x-3, self.saved_y, self.saved_x+3, self.saved_y, width=3)
            # self.line2_id = self.canvas.create_line(self.saved_x, self.saved_y-3, self.saved_x, self.saved_y+3, width=3)
            # self.prev_point = tk.Canvas(self.canvas, width=3, height=3)
            # self.prev_point.place(x=self.saved_x-3, y=self.saved_y-3)

    def mouse_left_click(self, event):
        self.update_saved_point((event.x, event.y))
        self.mouse_motion(event)

    def updateImage(self):
        self.update_saved_point((None, None))
        filename = request_filename()
        self.root.title(f"RYB color picker: {filename}")
        
        rgba_image = Image.open(filename)
        self.w, self.h = rgba_image.size

        max_width = int(self.root.winfo_screenwidth() * .9)
        max_height = int(self.root.winfo_screenheight() * .9)

        if self.w > max_width:
            rgba_image = rgba_image.resize((max_width, int(self.h/self.w*max_width)))
            self.w, self.h = rgba_image.size

        if self.h > max_height:
            rgba_image = rgba_image.resize((int(self.w/self.h*max_height), max_height))
            self.w, self.h = rgba_image.size

        self.image = rgba_image.convert('RGB')

        self.canvas.config(width=self.w, height=self.h)
        self.canvas.pack()
        
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.label.configure(image=self.image_tk)

class BackgroundUpdater:
    def __init__(self):
        self.callbacks = []

    def register_callback(self, func):
        self.callbacks.append(func)

    def update_color(self, color):
        for callback in self.callbacks:
            callback(color)

class RYBLabelHandler:
    def __init__(self, label):
        self.label = label

    def update_color(self, rgb_color):
        self.label.configure(bg=f"#%02x%02x%02x" % rgb_color)
        r, y, b = rgb2ryb(*rgb_color)
        sum_ryb = max(1, r+y+b)
        r_perc, y_perc, b_perc = f"{r/sum_ryb*100:.1f}%", f"{y/sum_ryb*100:.1f}%", f"{b/sum_ryb*100:.1f}%"
        self.label.configure(text=f"RYB: {r}, {y}, {b} ({r_perc}, {y_perc}, {b_perc})")
        if sum(rgb_color)/3 > 255/2:
            self.label.configure(fg=f"#%02x%02x%02x" % (0, 0, 0))
        else:
            self.label.configure(fg=f"#%02x%02x%02x" % (255, 255, 255))

class RGBLabelHandler:
    def __init__(self, label):
        self.label = label

    def update_color(self, rgb_color):
        self.label.configure(bg=f"#%02x%02x%02x" % rgb_color)
        r, g, b = rgb_color
        self.label.configure(text=f"RGB: {r}, {g}, {b}")
        if sum(rgb_color)/3 > 255/2:
            self.label.configure(fg=f"#%02x%02x%02x" % (0, 0, 0))
        else:
            self.label.configure(fg=f"#%02x%02x%02x" % (255, 255, 255))
