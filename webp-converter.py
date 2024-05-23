import tkinter as tk
from tkinter import filedialog, messagebox, ttk
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
def process_image():
    filepaths = filedialog.askopenfilenames(filetypes=[("WEBP files", "*.webp")])
    if not filepaths:
        messagebox.showerror("Error", "No files selected")
        return

    try:
        bg_color = bg_color_var.get()
        width = int(width_var.get())
        height = int(height_var.get())
        size = (width, height)
        
        for filepath in filepaths:
            image = load_and_convert_image(filepath)
            image = remove_background(image, bg_color)
            image = resize_image(image, size)

            output_path = os.path.splitext(filepath)[0] + ".png"
            save_image(image, output_path)
        
        messagebox.showinfo("Success", "Images processed successfully")
        display_images(filepaths)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Function to display selected images
def display_images(filepaths):
    for widget in preview_frame.winfo_children():
        widget.destroy()

    for filepath in filepaths:
        img = Image.open(filepath)
        img.thumbnail((150, 150))
        img = ImageTk.PhotoImage(img)
        panel = tk.Label(preview_frame, image=img)
        panel.image = img
        panel.pack(side="left", padx=5, pady=5)

# Setup GUI
root = tk.Tk()
root.title("WEBP to PNG Converter")
root.geometry("800x600")

# Background color selection
tk.Label(root, text="Background color to remove:").grid(row=0, column=0, padx=10, pady=10)
bg_color_var = tk.StringVar(value="white")
tk.Radiobutton(root, text="White", variable=bg_color_var, value="white").grid(row=0, column=1)
tk.Radiobutton(root, text="Black", variable=bg_color_var, value="black").grid(row=0, column=2)

# Width input
tk.Label(root, text="Desired width:").grid(row=1, column=0, padx=10, pady=10)
width_var = tk.StringVar()
tk.Entry(root, textvariable=width_var).grid(row=1, column=1, columnspan=2)

# Height input
tk.Label(root, text="Desired height:").grid(row=2, column=0, padx=10, pady=10)
height_var = tk.StringVar()
tk.Entry(root, textvariable=height_var).grid(row=2, column=1, columnspan=2)

# Process button
tk.Button(root, text="Convert Images", command=process_image).grid(row=3, column=0, columnspan=3, pady=20)

# Preview frame
preview_frame = tk.Frame(root)
preview_frame.grid(row=4, column=0, columnspan=3, pady=10)

# Start the GUI event loop
root.state('zoomed')  # Maximize window on load
root.mainloop()
