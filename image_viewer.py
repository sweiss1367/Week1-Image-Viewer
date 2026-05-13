"""
Week 1 Assignment: Interactive Image Viewer
Uses Tkinter for the GUI, OpenCV for image processing,
and Pillow/ImageTk to display images inside Tkinter.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
from PIL import Image, ImageTk


# ── State ─────────────────────────────────────────────────────────────────────
# original_image: the BGR array loaded from disk, never modified
# current_image:  the working copy that all transforms are applied to
original_image = None
current_image = None


# ── Display ───────────────────────────────────────────────────────────────────
def display_image(img):
    """
    Convert an OpenCV BGR (or grayscale) array to a Tkinter-compatible photo
    image and render it on the canvas. Resizes the canvas to fit the image.
    """
    if img is None:
        return

    # OpenCV stores color images as BGR; Pillow expects RGB, so convert.
    if len(img.shape) == 2:
        # Grayscale: no channel axis — convert to RGB so Pillow handles it uniformly
        pil_img = Image.fromarray(img)
    else:
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb)

    photo = ImageTk.PhotoImage(pil_img)

    # Keep a reference on the canvas widget so Python's GC doesn't delete it
    canvas.image = photo
    canvas.config(width=pil_img.width, height=pil_img.height)
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

    # Update the status bar with current dimensions
    h, w = img.shape[:2]
    status_var.set(f"{filename_label}   |   {w} × {h} px")


# ── File I/O ──────────────────────────────────────────────────────────────────
def load_image():
    """
    Open a file dialog so the user can choose an image from disk.
    Reads the file with OpenCV (returns a BGR array) and stores it
    as both the original and the current working copy.
    """
    global original_image, current_image, filename_label

    path = filedialog.askopenfilename(
        title="Open Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"), ("All files", "*.*")]
    )
    if not path:
        return  # user cancelled

    img = cv2.imread(path)
    if img is None:
        messagebox.showerror("Load Error", f"Could not read image:\n{path}")
        return

    original_image = img.copy()
    current_image = img.copy()
    filename_label = path.split("/")[-1].split("\\")[-1]  # just the filename
    display_image(current_image)


def save_image():
    """
    Open a save dialog and write the current working image to disk using OpenCV.
    """
    if current_image is None:
        messagebox.showwarning("No Image", "Load an image first.")
        return

    path = filedialog.asksaveasfilename(
        title="Save Image",
        defaultextension=".png",
        filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg"), ("BMP", "*.bmp"), ("All files", "*.*")]
    )
    if not path:
        return

    cv2.imwrite(path, current_image)
    messagebox.showinfo("Saved", f"Image saved to:\n{path}")


# ── Geometric Transforms ──────────────────────────────────────────────────────
def resize_image():
    """
    Scale the current image to 50% of its size using cv2.resize().
    INTER_AREA is the recommended interpolation method when shrinking —
    it avoids aliasing artifacts by averaging pixel neighborhoods.
    """
    global current_image
    if current_image is None:
        messagebox.showwarning("No Image", "Load an image first.")
        return

    h, w = current_image.shape[:2]
    # fx and fy are the scale factors along x and y axes (0.5 = 50%)
    current_image = cv2.resize(current_image, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
    display_image(current_image)


def rotate_image():
    """
    Rotate the current image 90 degrees clockwise using cv2.rotate().
    cv2.ROTATE_90_CLOCKWISE is a lossless pixel rearrangement — no
    interpolation is needed because the rotation is axis-aligned.
    """
    global current_image
    if current_image is None:
        messagebox.showwarning("No Image", "Load an image first.")
        return

    current_image = cv2.rotate(current_image, cv2.ROTATE_90_CLOCKWISE)
    display_image(current_image)


def flip_image():
    """
    Flip the current image horizontally (mirror left-right) using cv2.flip().
    The flipCode argument controls the axis:
      1  = horizontal (flip around the y-axis)
      0  = vertical   (flip around the x-axis)
     -1  = both axes
    """
    global current_image
    if current_image is None:
        messagebox.showwarning("No Image", "Load an image first.")
        return

    current_image = cv2.flip(current_image, 1)  # 1 = horizontal flip
    display_image(current_image)


# ── Color Space Conversions ───────────────────────────────────────────────────
def to_grayscale():
    """
    Convert the ORIGINAL image to grayscale using cv2.cvtColor().
    Grayscale collapses the three BGR channels into a single luminance
    channel using the weighted formula: Y = 0.114B + 0.587G + 0.299R.
    We always start from the original so color conversions don't stack.
    """
    global current_image
    if original_image is None:
        messagebox.showwarning("No Image", "Load an image first.")
        return

    current_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
    display_image(current_image)


def to_hsv():
    """
    Convert the ORIGINAL image to HSV (Hue, Saturation, Value) color space.
    HSV separates color information (hue) from intensity (value), which makes
    it useful for tasks like color-based segmentation. We display the raw HSV
    array — the colors will look unusual because Tkinter interprets the bytes
    as RGB, but the channel structure is visible.
    """
    global current_image
    if original_image is None:
        messagebox.showwarning("No Image", "Load an image first.")
        return

    current_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    display_image(current_image)


def reset_image():
    """
    Restore the current working image to the original loaded from disk,
    discarding all transforms and color conversions applied since loading.
    """
    global current_image
    if original_image is None:
        messagebox.showwarning("No Image", "Load an image first.")
        return

    current_image = original_image.copy()
    display_image(current_image)


# ── UI Layout ─────────────────────────────────────────────────────────────────
def build_ui(root):
    """
    Construct the Tkinter window: a top toolbar, a scrollable canvas for the
    image, and a status bar at the bottom.
    """
    global canvas, status_var, filename_label
    filename_label = "No image loaded"

    root.title("Interactive Image Viewer")
    root.resizable(True, True)
    root.configure(bg="#2b2b2b")

    # ── Button bar ────────────────────────────────────────────────────────────
    btn_frame = tk.Frame(root, bg="#2b2b2b", pady=6)
    btn_frame.pack(side=tk.TOP, fill=tk.X)

    btn_style = dict(bg="#4a90d9", fg="white", font=("Helvetica", 10, "bold"),
                     relief=tk.FLAT, padx=10, pady=5, cursor="hand2")

    buttons = [
        ("Load Image",      load_image),
        ("Resize (50%)",    resize_image),
        ("Rotate 90°",      rotate_image),
        ("Flip Horizontal", flip_image),
        ("Grayscale",       to_grayscale),
        ("HSV",             to_hsv),
        ("Reset Original",  reset_image),
        ("Save Image",      save_image),
    ]

    for label, command in buttons:
        tk.Button(btn_frame, text=label, command=command, **btn_style).pack(
            side=tk.LEFT, padx=4, pady=2
        )

    # ── Scrollable canvas area ────────────────────────────────────────────────
    canvas_frame = tk.Frame(root, bg="#1e1e1e")
    canvas_frame.pack(fill=tk.BOTH, expand=True)

    h_scroll = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
    v_scroll = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
    h_scroll.pack(side=tk.BOTTOM, fill=tk.X)
    v_scroll.pack(side=tk.RIGHT,  fill=tk.Y)

    canvas = tk.Canvas(canvas_frame, bg="#1e1e1e",
                       xscrollcommand=h_scroll.set,
                       yscrollcommand=v_scroll.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    h_scroll.config(command=canvas.xview)
    v_scroll.config(command=canvas.yview)

    # ── Status bar ────────────────────────────────────────────────────────────
    status_var = tk.StringVar(value="No image loaded — click 'Load Image' to begin.")
    status_bar = tk.Label(root, textvariable=status_var, bg="#1e1e1e", fg="#aaaaaa",
                          font=("Helvetica", 9), anchor=tk.W, padx=8)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)


# ── Entry Point ───────────────────────────────────────────────────────────────
def main():
    root = tk.Tk()
    root.geometry("900x620")
    build_ui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
