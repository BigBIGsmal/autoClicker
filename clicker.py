import tkinter as tk
import pyautogui
import threading
import time
import keyboard
import random

# Initialize variables
last_text_id = None
timer_text_id = None
hold_time = 3  # Time to hold the click (in seconds)
timer_value = hold_time
is_holding = False
stop_event = threading.Event()  # Event to control the autoclick loop

def update_timer():
    global timer_value, is_holding
    if is_holding:
        if timer_value > 0:
            canvas.itemconfig(timer_text_id, text=f"Hold for {timer_value:.1f} seconds")
            timer_value -= 0.1  # Reduce timer by 0.1 seconds (100ms)
            canvas.after(100, update_timer)
        else:
            finalize_click()

def finalize_click():
    global x, y
    print(f"Final confirmed click at coordinates: ({x}, {y})")
    
    # Start autoclick in a separate thread
    stop_event.clear()  # Clear the stop event before starting
    click_thread = threading.Thread(target=autoclick, args=(x, y), daemon=True)
    click_thread.start()
    
    # Hide the canvas window instead of destroying it
    root.withdraw()  # This will hide the Tkinter window

def start_holding(event):
    global x, y, last_text_id, timer_value, is_holding
    x, y = event.x_root, event.y_root
    timer_value = hold_time
    is_holding = True
    if last_text_id:
        canvas.delete(last_text_id)
    last_text_id = canvas.create_text(x, y, text=f"({x}, {y})", fill="black", font=('Helvetica', 12, 'bold'))
    update_timer()

def stop_holding(event):
    global is_holding
    is_holding = False
    canvas.itemconfig(timer_text_id, text="")

def close_app(event=None):
    stop_event.set()  # Signal the autoclick thread to stop
    root.destroy()

def autoclick(x, y):
    while not stop_event.is_set():  # Check the stop event to exit the loop
        pyautogui.click(x, y)  # Perform the click
        random_sleep = random.uniform(0.006, 0.09)  # Random delay between 0.006 and 0.009 seconds
        time.sleep(random_sleep)  # Sleep for the random duration

# Create the main window
root = tk.Tk()
root.attributes('-fullscreen', True, "-alpha", 0.4)  # Set to full screen

# Create a canvas to draw on
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()

# Instruction text
canvas.create_text(326, 90, text=f"Click and hold for 3 seconds to confirm\n(Press Esc to stop auto-clicking)", fill="black", font=('Helvetica', 12, 'bold'))

# Timer display
timer_text_id = canvas.create_text(326, 140, text="", fill="black", font=('Helvetica', 16, 'bold'))

# Key press checking loop (for Escape)
def check_escape():
    if keyboard.is_pressed("escape"):
        close_app()
    root.after(100, check_escape)  # Keep checking every 100ms

# Bind the mouse click and release events
root.bind("<Button-1>", start_holding)  # Start holding
root.bind("<ButtonRelease-1>", stop_holding)  # Stop holding

# Start the Escape key checking loop
check_escape()

# Start the main loop
root.mainloop()
