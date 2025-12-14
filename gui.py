import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

from pipeline import run_pipeline


# --------------------------------------------
# Helper functions
# --------------------------------------------

def resize_for_display(img, max_w=600, max_h=500):
    h, w = img.shape[:2]
    scale = min(max_w / w, max_h / h)
    return cv2.resize(img, (int(w * scale), int(h * scale)))


def create_overlay(img_rgb, masks):
    overlay = img_rgb.copy()
    masks_i = masks.astype(np.int32)
    gy, gx = np.gradient(masks_i)
    edges = (gy != 0) | (gx != 0)
    overlay[edges] = [255, 0, 255]
    return overlay


# --------------------------------------------
# Root window
# --------------------------------------------

root = tk.Tk()
root.title("Tezak Cell Counter")
root.geometry("1400x900")
root.configure(bg="#151515")

# --------------------------------------------
# Styles
# --------------------------------------------

style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Primary.TButton",
    font=("Helvetica", 15, "bold"),
    background="#6366f1",
    foreground="white",
    padding=12,
)
style.map("Primary.TButton", background=[("active", "#4f46e5")])

style.configure(
    "Nav.TButton",
    font=("Helvetica", 14, "bold"),
    background="#374151",
    foreground="#e5e7eb",
    padding=10,
)
style.map("Nav.TButton", background=[("active", "#4b5563")])

# --------------------------------------------
# Title + Status
# --------------------------------------------

title = tk.Label(root, text="Tezak Cell Counter",
                 font=("Helvetica", 32, "bold"),
                 fg="white", bg="#151515")
title.pack(pady=10)

status = tk.Label(root,
                  text="Preparing interface...",
                  font=("Helvetica", 15),
                  fg="#e5e7eb", bg="#151515")
status.pack(pady=5)

# --------------------------------------------
# Image Display Area
# --------------------------------------------

image_frame = tk.Frame(root, bg="#151515")
image_frame.pack(pady=10)

left_frame = tk.Frame(image_frame, bg="#151515")
left_frame.grid(row=0, column=0, padx=20)

right_frame = tk.Frame(image_frame, bg="#151515")
right_frame.grid(row=0, column=1, padx=20)

original_label = tk.Label(left_frame, bg="#151515")
original_label.pack()

segmented_label = tk.Label(right_frame, bg="#151515")
segmented_label.pack()

# --------------------------------------------
# Counts
# --------------------------------------------

counts_label = tk.Label(
    root, text="", font=("Helvetica", 16),
    fg="#e5e7eb", bg="#151515", justify="center")
counts_label.pack(pady=10)

# --------------------------------------------
# Global state
# --------------------------------------------

image_records = []
current_index = -1


# --------------------------------------------
# Display logic
# --------------------------------------------

def show_current_image():
    global current_index

    rec = image_records[current_index]

    # ORIGINAL
    disp = resize_for_display(rec["img"])
    disp_tk = ImageTk.PhotoImage(Image.fromarray(disp))
    original_label.config(image=disp_tk)
    original_label.image = disp_tk

    # SEGMENTED
    if rec["masks"] is not None:
        overlay = create_overlay(rec["img"], rec["masks"])
        ov = resize_for_display(overlay)
        ov_tk = ImageTk.PhotoImage(Image.fromarray(ov))
        segmented_label.config(image=ov_tk)
        segmented_label.image = ov_tk
    else:
        segmented_label.config(image="")
        segmented_label.image = None

    # COUNTS
    filename = rec["path"].split("/")[-1]
    if rec["masks"] is not None:
        c = rec["counts"]
        counts_label.config(
            text=(
                f"Image {current_index+1} of {len(image_records)} — {filename}\n\n"
                f"Total: {rec['total']}\n"
                f"🔴 {c['red']}    🟢 {c['green']}    🔵 {c['blue']}"
            )
        )
    else:
        counts_label.config(
            text=f"Image {current_index+1} of {len(image_records)} — {filename}\n(Not processed yet)"
        )


# --------------------------------------------
# Processing logic
# --------------------------------------------

def upload_images():
    global image_records, current_index

    paths = filedialog.askopenfilenames(
        filetypes=[("Images", "*.png *.jpg *.jpeg")]
    )
    if not paths:
        return

    image_records = []
    for p in paths:
        img_bgr = cv2.imread(p)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        image_records.append(
            {"path": p, "img": img_rgb,
             "masks": None, "counts": None, "total": None}
        )

    current_index = 0
    status.config(text=f"Loaded {len(image_records)} images.", fg="#a3e635")
    show_current_image()


def run_all():
    if not image_records:
        status.config(text="No images loaded.", fg="#f97373")
        return

    status.config(text="Processing images...", fg="#fde68a")
    root.update_idletasks()

    for rec in image_records:
        masks, flows, counts, total = run_pipeline(rec["img"])
        rec["masks"] = masks
        rec["counts"] = counts
        rec["total"] = total

    status.config(text="Done! Use Previous/Next.", fg="#4ade80")
    show_current_image()


def go_prev():
    global current_index
    if current_index > 0:
        current_index -= 1
        show_current_image()


def go_next():
    global current_index
    if current_index < len(image_records) - 1:
        current_index += 1
        show_current_image()


# --------------------------------------------
# BUTTONS ADDED *AFTER* TK INITIALIZES (NO LAG)
# --------------------------------------------

def create_buttons_after_load():
    """
    This runs AFTER the Tk event loop initializes.
    This is the ONLY reliable way to eliminate button lag on macOS.
    """
    global upload_btn, run_btn, prev_btn, next_btn

    button_frame = tk.Frame(root, bg="#151515")
    button_frame.pack(pady=20)

    upload_btn = ttk.Button(button_frame, text="Upload Images",
                            style="Primary.TButton",
                            command=upload_images)
    upload_btn.grid(row=0, column=0, padx=20)

    run_btn = ttk.Button(button_frame, text="Run Cell Counter",
                         style="Primary.TButton",
                         command=run_all)
    run_btn.grid(row=0, column=1, padx=20)

    nav_frame = tk.Frame(root, bg="#151515")
    nav_frame.pack(pady=10)

    prev_btn = ttk.Button(nav_frame, text="← Previous",
                          style="Nav.TButton", command=go_prev)
    prev_btn.grid(row=0, column=0, padx=15)

    next_btn = ttk.Button(nav_frame, text="Next →",
                          style="Nav.TButton", command=go_next)
    next_btn.grid(row=0, column=1, padx=15)

    status.config(text="Ready!", fg="#4ade80")


# Run this AFTER the first frame renders
root.after(50, create_buttons_after_load)

# --------------------------------------------
# Main loop
# --------------------------------------------

root.mainloop()
