import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Label, Frame, Button, messagebox

class PhotoBooth:
    def __init__(self, window):
        self.window = window
        self._timer = 0
        self.photos = []
        self.photo_paths = []
        self.filter_var = tk.StringVar(window)
        self.filter_var.set("Normal")

        # Webcam start
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            messagebox.showerror("Error", "Webcam tidak ditemukan!")
            window.destroy()
            return

        # Folder save
        self.save_folder = r"C:\Users\ANINDYA\TugasAkhir\CapturedPhotos"
        os.makedirs(self.save_folder, exist_ok=True)

        # UI
        self.timer_label = Label(window, text="", font=("Arial", 26, "bold"),
                                 fg="purple", bg="#e8cdf7")
        self.timer_label.pack()

        self.label = Label(window, bg="#a5c9fe")
        self.label.pack(pady=10)

        self.gallery_frame = Frame(window, bg="#e3b6ee")
        self.gallery_frame.pack(pady=10)

        self.window.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_frame()

    # Timer
    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value):
        try:
            self._timer = int(value)
        except:
            self._timer = 0

    # Webcam Loop
    def update_frame(self):
        ret, frame = self.video.read()
        if ret:
            frame = self.apply_filter(frame, self.filter_var.get())
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        self.window.after(10, self.update_frame)

    # Start countdown
    def start_timer_capture(self):
        def countdown(sec):
            if sec > 0:
                self.timer_label.config(text=str(sec))
                self.window.after(1000, countdown, sec - 1)
            else:
                self.timer_label.config(text="")
                self.capture_photo()

        countdown(self.timer)

    # Capture and SAVE
    def capture_photo(self):
        ret, frame = self.video.read()
        if not ret:
            print("Frame not captured.")
            return

        frame = self.apply_filter(frame, self.filter_var.get())
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # AUTO-NUMBER FIX
        existing = [
            int(f.split("_")[1].split(".")[0])
            for f in os.listdir(self.save_folder)
            if f.startswith("photo_") and f.endswith(".png")
        ]

        next_id = max(existing) + 1 if existing else 1
        save_path = os.path.join(self.save_folder, f"photo_{next_id}.png")

        img.save(save_path)
        print("Saved:", save_path)

        # Memory
        self.photos.append(img)
        self.photo_paths.append(save_path)

        self.display_photos()

    # Filters
    def apply_filter(self, frame, name):
        if name == "Grayscale":
            g = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            return cv2.cvtColor(g, cv2.COLOR_GRAY2BGR)

        elif name == "Sepia":
            kernel = np.array([
                [0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189]
            ])
            sepia = cv2.transform(frame.astype(np.float32), kernel)
            return np.clip(sepia, 0, 255).astype(np.uint8)

        return frame

    # Gallery display
    def display_photos(self):
        for w in self.gallery_frame.winfo_children():
            w.destroy()

        for idx, img in enumerate(self.photos):
            thumb = img.copy()
            thumb.thumbnail((160, 120))
            imgtk = ImageTk.PhotoImage(thumb)

            frame = Frame(self.gallery_frame, bg="#ccc", width=160, height=120)
            frame.grid(row=idx // 4, column=idx % 4, padx=5, pady=5)
            frame.grid_propagate(False)

            lbl = Label(frame, image=imgtk)
            lbl.imgtk = imgtk
            lbl.pack()

            del_btn = Button(
                frame, text="✕", fg="white", bg="#d9534f",
                font=("Arial", 10, "bold"),
                command=lambda i=idx: self.delete_photo(i),
                bd=0
            )
            del_btn.place(relx=1, rely=0, anchor="ne")

    # Delete photo
    def delete_photo(self, index):
        try:
            self.photos.pop(index)
            file_path = self.photo_paths.pop(index)
            if os.path.exists(file_path):
                os.remove(file_path)
                print("Deleted:", file_path)
        except Exception as e:
            print("Delete error:", e)

        self.display_photos()

    # Cleanup
    def on_close(self):
        self.video.release()
        self.window.destroy()
