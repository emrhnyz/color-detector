import pyautogui
import keyboard
import tkinter as tk
import threading

# Global state variable
state = 0
color_list = []  # List to store colors and coordinates

MAX_LIST_SIZE = 5  # Maximum list size

def state_loop():
    global state
    if state == 1:
        # When state is 1, track the cursor position and color
        x, y = pyautogui.position() 
        color = pyautogui.pixel(x, y)

        # Convert RGB to HEX
        r, g, b = color
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        
        # Update text fields with coordinates and color information
        x_text.delete(1.0, tk.END)
        y_text.delete(1.0, tk.END)
        
        x_text.insert(tk.END, f"X: {x}, Y: {y}")
        y_text.insert(tk.END, f"Color (RGB): {color}\nColor (HEX): {hex_color}")
        
        # Center align the text
        x_text.tag_configure("center", justify="center")
        y_text.tag_configure("center", justify="center")
        
        x_text.tag_add("center", 1.0, tk.END)
        y_text.tag_add("center", 1.0, tk.END)

        # Call the state loop again after 10ms if state is still 1
        if state == 1:
            root.after(10, state_loop)

def toggle_action():
    global state
    if state == 0:
        state = 1
        action_button.config(text="Stop", font=("Helvetica", 12,), bg="red")
        x_text.config(state=tk.NORMAL)  # Enable text editing
        
        # Start the state loop in a new thread
        threading.Thread(target=state_loop, daemon=True).start()
    else:
        state = 0
        action_button.config(text="Start", font=("Helvetica", 12,), bg="green")
        x_text.config(state=tk.DISABLED)  # Disable text editing

def save():
    global state
    if state == 1:
        # Get current cursor position and color
        x, y = pyautogui.position()
        color = pyautogui.pixel(x, y)
        r, g, b = color
        hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
        
        # If the list has more than 5 elements, remove the oldest
        if len(color_list) >= MAX_LIST_SIZE:
            color_list.pop(0)
        
        # Add new color and coordinates to the list
        color_list.append((x, y, color, hex_color))

        # Display message that data was saved
        info_label.config(text="Data saved!", fg="green")

        # Clear existing saved items and display the updated list
        for widget in saved_frame.winfo_children():
            widget.destroy()

        for i, (x, y, color, hex_color) in enumerate(color_list):
            color_box = tk.Canvas(saved_frame, width=30, height=30, bg=hex_color, bd=0)
            color_box.grid(row=i, column=0, padx=5, pady=5)
            label = tk.Label(saved_frame, text=f"X: {x}, Y: {y}\nRGB: {color}\nHEX: {hex_color}",
                             font=("Helvetica", 10), width=30, anchor="w", bg="#f0f0f0", bd=0)
            label.grid(row=i, column=1, padx=5, pady=5, sticky="w")

# Create main window
root = tk.Tk()
root.title("Coordinate and Color Tracker")
root.geometry("550x500")
root.config(bg="#f0f0f0")

# Window title label
title_label = tk.Label(root, text="Coordinate and Color Information", font=("Helvetica", 14, "bold"), bg="#f0f0f0")
title_label.pack(pady=10)

# Coordinate input label and text fields
coord_label = tk.Label(root, text="Coordinates (x, y):", font=("Helvetica", 12), bg="#f0f0f0")
coord_label.pack(pady=5)

x_label = tk.Label(root, text="X and Y Coordinates:", bg="#f0f0f0")
x_label.pack()
x_text = tk.Text(root, height=1, width=25, font=("Helvetica", 14), wrap=tk.WORD)
x_text.pack(pady=5)

y_label = tk.Label(root, text="Color Codes:", bg="#f0f0f0")
y_label.pack()
y_text = tk.Text(root, height=2, width=25, font=("Helvetica", 14), wrap=tk.WORD)
y_text.pack(pady=5)

# Frame for displaying saved colors and coordinates
saved_frame = tk.Frame(root, bg="#f0f0f0")
saved_frame.pack(pady=10)

# Information message label
info_label = tk.Label(root, text="", font=("Helvetica", 12), fg="red", bg="#f0f0f0")
info_label.pack(pady=5)

# Instructions to save data by pressing the 'S' key
instructions_label = tk.Label(root, text="Press 'S' to save the data", font=("Helvetica", 12), fg="blue", bg="#f0f0f0")
instructions_label.pack(pady=10)

# Action button to start and stop the tracking
action_button = tk.Button(root, text="Start", command=toggle_action, font=("Helvetica", 12), width=10, height=2, bg="green", fg="white")
action_button.pack(padx=10, pady=20)

# Bind 'S' key to save function
keyboard.add_hotkey('s', save)

# Run the GUI
root.mainloop()
