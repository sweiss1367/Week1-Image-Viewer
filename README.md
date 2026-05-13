# Week 1 Assignment: Interactive Image Viewer

A desktop image viewer built with Python, Tkinter, OpenCV, and Pillow.
Demonstrates basic computer vision concepts including color space conversion,
geometric transforms, and image I/O.

---

## What the App Does

This application lets you load any image from disk and apply common image
processing operations in real time through a simple point-and-click interface.
It is designed to demonstrate foundational computer vision concepts covered in
Week 1: reading images, manipulating pixel data, and converting between color
spaces using OpenCV.

---

## Tools Used

| Tool | Role |
|---|---|
| Python 3.8+ | Programming language |
| Tkinter | GUI framework — window, buttons, canvas (built into Python) |
| OpenCV (`opencv-python`) | Image loading, processing, color space conversion |
| Pillow | Converting OpenCV arrays to Tkinter-displayable images |
| NumPy | Underlying array support (installed with OpenCV) |
| Matplotlib | Visualization tool for comparison images and assignment screenshots |

---

## Project Structure

```
Week1/
├── image_viewer.py       # Main application — all GUI and CV logic
├── sample_image.jpg      # Sample image for testing
├── screenshots/          # UI screenshots for the writeup / submission
├── presentation/         # Slides or PDF for the Week 1 presentation
└── README.md
```

---

## How to Install Dependencies

Tkinter is built into Python on Windows — no install needed.

Install the remaining libraries from your terminal or VS Code terminal:

```bash
pip install opencv-python pillow matplotlib
```

---

## How to Run the App

```bash
python image_viewer.py
```

Requires Python 3.8 or later.

---

## Features

| Button | Operation | OpenCV Call | CV Concept |
|---|---|---|---|
| Load Image | Browse and open any image file | `cv2.imread()` | Reading images into BGR arrays |
| Resize 50% | Scale width and height by half | `cv2.resize()` with `INTER_AREA` | Spatial downsampling |
| Rotate 90° | Rotate clockwise 90 degrees | `cv2.rotate()` | Lossless axis-aligned rotation |
| Flip Horizontal | Mirror left-right | `cv2.flip(img, 1)` | Mirror transform along y-axis |
| Grayscale | Convert to single-channel luminance | `cv2.cvtColor(BGR2GRAY)` | Weighted channel collapse |
| HSV | Convert to Hue/Saturation/Value space | `cv2.cvtColor(BGR2HSV)` | Color space separation |
| Reset Original | Undo all transforms | Restore saved copy | Immutable original pattern |
| Save Image | Write current image to disk | `cv2.imwrite()` | Image file output |

---

## Screenshot Checklist

Save screenshots to the `screenshots/` folder using these names:

```
01_original.png       — image loaded, no transforms
02_resized.png        — after Resize 50%
03_rotated.png        — after Rotate 90°
04_flipped.png        — after Flip Horizontal
05_grayscale.png      — after Grayscale conversion
06_hsv.png            — after HSV conversion
07_saved_output.png   — confirmation of Save Image
```

---

## Key Implementation Notes

**BGR vs RGB**
OpenCV loads images in BGR channel order. Pillow expects RGB. Every image
displayed in the app is converted with `cv2.cvtColor(img, cv2.COLOR_BGR2RGB)`
before being passed to `ImageTk.PhotoImage`.

**Immutable original**
`original_image` is stored at load time and never modified. Color conversions
(grayscale, HSV) always branch from the original so transforms don't stack
unexpectedly. Geometric transforms (resize, rotate, flip) chain on
`current_image` and compose naturally.

**Grayscale display**
`cv2.cvtColor(BGR2GRAY)` returns a 2D array with no channel axis. The display
function checks `len(img.shape)` to handle this case before passing to Pillow.

---

## AI Disclosure

This project was developed with the assistance of Claude (Anthropic) for code
generation, documentation, and project structure guidance. All code has been
reviewed, tested, and understood by the student. AI assistance was used as a
learning and productivity tool in accordance with course guidelines.

---

## References

- OpenCV documentation: https://docs.opencv.org/4.x/
- Pillow (PIL) documentation: https://pillow.readthedocs.io/
- Tkinter reference: https://docs.python.org/3/library/tkinter.html
- OpenCV color space conversions: https://docs.opencv.org/4.x/d8/d01/group__imgproc__color__conversions.html
- NumPy documentation: https://numpy.org/doc/
- Matplotlib documentation: https://matplotlib.org/stable/

---

## Author

Graduate Computer Vision — Week 1 Assignment
