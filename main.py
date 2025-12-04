import tkinter as tk
from tkinter import Frame, Button, Entry, OptionMenu
from photobooth import PhotoBooth

root = tk.Tk()
root.title("PhotoBooth")
root.configure(bg="#a3c8ff")

app = PhotoBooth(root)

top = Frame(root, bg="#c4dcff")
top.pack(pady=8)

# Filter Dropdown
filter_menu = OptionMenu(top, app.filter_var, "Normal", "Grayscale", "Sepia")
filter_menu.pack(side="left", padx=5)

# Timer input
timer_input = Entry(top, width=5)
timer_input.insert(0, "0")
timer_input.pack(side="left", padx=5)

# Capture
Button(
    top, text="Capture",
    command=lambda: setattr(app, "timer", timer_input.get()) or app.start_timer_capture()
).pack(side="left", padx=5)

# Clear all
Button(top, text="Clear Photos", command=app.clear_photos).pack(side="left", padx=5)

root.mainloop()
