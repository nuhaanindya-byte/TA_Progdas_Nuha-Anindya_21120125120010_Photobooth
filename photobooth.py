import cv2 #mengaktifkan dan mengendalikan kamera, serta memproses gambar/video di Python.
from PIL import Image, ImageTk #mengubah frame kamera OpenCV menjadi gambar yang bisa ditampilkan di Tkinter.
import numpy as np #untuk operasi matematika pada gambar (karena frame kamera = array).
import tkinter as tk #Membuat window (tk.Tk())
from tkinter import Label, Frame, messagebox #mengambil widget Tkinter spesifik yang sering kamu gunakan.
import os #untuk mengelola file dan folder.

class PhotoBooth:
    def __init__(self, window):
        self.window = window
        self._timer = 0
        self.photos = []
        self.filter_var = tk.StringVar(window)
        self.filter_var.set("Normal")

        # initialize webcam capture
        self.video = cv2.VideoCapture(0)
        if not self.video.isOpened():
            messagebox.showerror("Webcam Error", "Cannot open webcam. Check camera and permissions.")
            window.destroy()
            return

        self.save_folder = r"C:\Users\ANINDYA\TugasAkhir\CapturedPhotos"
        os.makedirs(self.save_folder, exist_ok=True)

        # ---------------- GUI TIMER LABEL ----------------
        self.timer_label = Label(window, text="", font=("Arial", 26, "bold"), fg="purple", bg="#e8cdf7")
        self.timer_label.pack()

        # Webcam display
        self.label = Label(window, bg="#a5c9fe")
        self.label.pack(pady=10)
    
        # Gallery frame
        self.gallery_frame = Frame(window, bg="#e3b6ee")
        self.gallery_frame.pack(pady=10)

        # ensure webcam is released when window closes
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.update_frame()

    # ---------------- Timer Property ----------------
    @property
    def timer(self):
        return self._timer

    @timer.setter
    def timer(self, value):
        try:
            self._timer = int(value)
        except:
            self._timer = 0

    # ---------------- Webcam Loop ----------------
    def update_frame(self):
        if not hasattr(self, "video") or self.video is None:
            return

        ret, frame = self.video.read()
        if ret:
            frame = self.apply_filter(frame, self.filter_var.get())

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(img)
            self.label.imgtk = imgtk
            self.label.configure(image=imgtk)

        # schedule next frame
        self.window.after(10, self.update_frame)

    # ---------------- START TIMER ----------------
    def start_timer_capture(self):
        t = self.timer

        def countdown(sec):
            if sec > 0:
                self.timer_label.config(text=f"{sec}")
                self.window.after(1000, countdown, sec - 1)
            else:
                self.timer_label.config(text="")
                self.capture_photo()

        countdown(t)

    # ---------------- CAPTURE PHOTO ----------------
    def capture_photo(self):
        if not hasattr(self, "video") or self.video is None:
            return

        ret, frame = self.video.read()
        if ret:
            frame = self.apply_filter(frame, self.filter_var.get())
            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.photos.append(img)

            # Save image
            file_count = len(os.listdir(self.save_folder)) + 1
            save_path = os.path.join(self.save_folder, f"photo_{file_count}.png")
            img.save(save_path)
            print(f"Foto tersimpan otomatis: {save_path}")

            self.display_photos()

    # ---------------- FILTERS ----------------
    def apply_filter(self, frame, filter_name):
        if filter_name == "Grayscale":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        elif filter_name == "Sepia":
            frame = np.array(frame, dtype=np.float32)
            sepia = np.array([
                [0.272, 0.534, 0.131],
                [0.349, 0.686, 0.168],
                [0.393, 0.769, 0.189]
            ])
            frame = cv2.transform(frame, sepia)
            frame = np.clip(frame, 0, 255).astype(np.uint8)

        return frame

    # ---------------- GALLERY ----------------
    def display_photos(self):
        for widget in self.gallery_frame.winfo_children():
            widget.destroy()

        for idx, img in enumerate(self.photos):
            thumb = img.copy()
            thumb.thumbnail((160, 120))
            imgtk = ImageTk.PhotoImage(thumb)

            frame = Frame(self.gallery_frame, bg="#ccc")
            frame.grid(row=idx // 4, column=idx % 4, padx=5, pady=5)

            lbl = Label(frame, image=imgtk)
            lbl.imgtk = imgtk
            lbl.pack()

    # ---------------- CLEAR PHOTOS ----------------
    def clear_photos(self):
        self.photos = []
        self.display_photos()

    # ---------------- CLEANUP ----------------
    def on_close(self):
        try:
            if hasattr(self, "video") and self.video is not None:
                self.video.release()
        except Exception:
            pass
        try:
            self.window.destroy()
        except Exception:
            pass