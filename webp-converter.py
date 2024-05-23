import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageOps, ImageTk
import numpy as np
import os

# Function to load and convert image
def load_and_convert_image(filepath):
    image = Image.open(filepath).convert("RGBA")
    return image

# Function to remove background
def remove_background(image, bg_color='white'):
    data = np.array(image)
    r, g, b, a = data.T
    
    if bg_color == 'white':
        replace_color = (r == 255) & (g == 255) & (b == 255)
    elif bg_color == 'black':
        replace_color = (r == 0) & (g == 0) & (b == 0)
    
    data[..., :-1][replace_color.T] = (255, 255, 255, 0)
    
    return Image.fromarray(data)

# Function to resize image
def resize_image(image, size):
    return image.resize(size, Image.ANTIALIAS)

# Function to save image
def save_image(image, output_path):
    image.save(output_path, 'PNG')

# Function to handle image processing
def process_images():
    try:
        bg_color = bg_color_var.get()
        width = width_var.get()
        height = height_var.get()

        # Input validation
        if not width.isdigit() or not height.isdigit():
            messagebox.showerror("Error", "Width and height must be integers")
            return

        width = int(width)
        height = int(height)
        size = (width, height)

        for filepath in filepaths:
            image = load_and_convert_image(filepath)
            image = remove_background(image, bg_color)
            image = resize_image(image, size)

            output_path = os.path.splitext(filepath)[0] + ".png"
            save_image(image, output_path)
        
        messagebox.showinfo("Success", "Images processed successfully")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to handle image selection
def select_images():
    global filepaths
    filepaths = filedialog.askopenfilenames(filetypes=[("WEBP files", "*.webp")])
    if not filepaths:
        return
    display_images(filepaths)

# Function to display selected images
def display_images(filepaths):
    for widget in preview_frame.winfo_children():
        widget.destroy()

    for filepath in filepaths:
        img = Image.open(filepath)
        img.thumbnail((150, 150))
        img = ImageTk.PhotoImage(img)
        panel = ttk.Label(preview_frame, image=img)
        panel.image = img
        panel.pack(side="left", padx=5, pady=5)

# Setup GUI
root = tk.Tk()
root.title("WEBP to PNG Converter")
root.geometry("800x600")

# Apply ttk theme
style = ttk.Style(root)
try:
    root.tk.call("source", "azure.tcl")
    style.theme_use("azure")
except tk.TclError:
    messagebox.showwarning("Theme Error", "Azure theme file not found. Using default theme.")

# Select images button
ttk.Button(root, text="Select Images", command=select_images).grid(row=0, column=0, padx=10, pady=10)

# Background color selection
ttk.Label(root, text="Background color to remove:").grid(row=1, column=0, padx=10, pady=10)
bg_color_var = tk.StringVar(value="white")
ttk.Radiobutton(root, text="White", variable=bg_color_var, value="white").grid(row=1, column=1)
ttk.Radiobutton(root, text="Black", variable=bg_color_var, value="black").grid(row=1, column=2)

# Width input
ttk.Label(root, text="Desired width:").grid(row=2, column=0, padx=10, pady=10)
width_var = tk.StringVar()
ttk.Entry(root, textvariable=width_var).grid(row=2, column=1, columnspan=2)

# Height input
ttk.Label(root, text="Desired height:").grid(row=3, column=0, padx=10, pady=10)
height_var = tk.StringVar()
ttk.Entry(root, textvariable=height_var).grid(row=3, column=1, columnspan=2)

# Process button
ttk.Button(root, text="Convert Images", command=process_images).grid(row=4, column=0, columnspan=3, pady=20)

# Preview frame
preview_frame = ttk.Frame(root)
preview_frame.grid(row=5, column=0, columnspan=3, pady=10)

# Start the GUI event loop
root.state('zoomed')  # Maximize window on load
root.mainloop()
