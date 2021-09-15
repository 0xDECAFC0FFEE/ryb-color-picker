from handlers import *
import tkinter as tk
from tkinter import Tk, PhotoImage, BOTTOM

root = Tk()
root.iconphoto(False, PhotoImage(file = "ryb.png"))
root.resizable(False, False) 

root.title("RYB color picker")
bg_updater = BackgroundUpdater()
bg_updater.register_callback(lambda color: root.configure(background=f"#%02x%02x%02x" % color))

frame = tk.Frame(root)
bg_updater.register_callback(lambda color: frame.configure(background=f"#%02x%02x%02x" % color))
frame.pack()

taskbar = tk.Frame(frame)
taskbar.pack(side=BOTTOM)
bg_updater.register_callback(lambda color: taskbar.configure(background=f"#%02x%02x%02x" % color))

btn = tk.Button(taskbar, text="load image", bg="Black")
btn.grid(column=1, row=0)

rgb = tk.Label(taskbar, text="")
rgb.grid(column=0, row=0)
rgb_handler = RGBLabelHandler(rgb)
bg_updater.register_callback(rgb_handler.update_color)

ryb = tk.Label(taskbar, text="")
ryb.grid(column=2, row=0)
ryb_handler = RYBLabelHandler(ryb)
bg_updater.register_callback(ryb_handler.update_color)

image_handler = ImageHandler(root, frame, bg_updater)

btn.config(command=image_handler.updateImage)
bg_updater.register_callback(lambda color: btn.configure(highlightbackground=f"#%02x%02x%02x" % color))

root.mainloop()
