import tkinter as tk
from tkinter import Button, OptionMenu, Frame
from photobooth import PhotoBooth

root = tk.Tk()
root.title("PhotoBooth")
root.configure(bg="#a3c8ff")

# ------------------- PILIH MODE LAYOUT -------------------
# app = PhotoBooth(root, use_grid=False)   # default pack
app = PhotoBooth(root, use_grid=True)      # aktifkan grid
# ----------------------------------------------------------

# ---------- Top Menu ----------
top_frame = Frame(root, bg="#e3b6ee")
if app.use_grid:
    top_frame.grid(row=2, column=0, pady=10)
else:
    top_frame.pack(pady=10)

# Filter Menu
filter_menu = OptionMenu(top_frame, app.filter_var,
                         "Normal", "Grayscale", "Sepia")
filter_menu.grid(row=0, column=0, padx=5) if app.use_grid else filter_menu.pack(side="left", padx=5)

# Timer Dropdown
timer_var = tk.StringVar(root)
timer_var.set("3")

timer_menu = OptionMenu(top_frame, timer_var, "10", "5", "3", "0")
timer_menu.grid(row=0, column=1, padx=5) if app.use_grid else timer_menu.pack(side="left", padx=5)

# Capture Button
capture_btn = Button(
    top_frame,
    text="Capture",
    command=lambda: (setattr(app, "timer", timer_var.get()), app.start_timer_capture())
)
capture_btn.grid(row=0, column=2, padx=5) if app.use_grid else capture_btn.pack(side="left", padx=5)

# Clear Photos
clear_btn = Button(top_frame, text="Clear Photos", command=app.clear_photos)
clear_btn.grid(row=0, column=3, padx=5) if app.use_grid else clear_btn.pack(side="left", padx=5)

root.mainloop()
