import tkinter as tk

# Initialize variable to store the last text ID and timer ID
last_text_id = None
timer_text_id = None
hold_time = 3  # Time to hold the click (in seconds)
timer_value = hold_time
is_holding = False

def update_timer():
    global timer_value, is_holding
    if is_holding:
        if timer_value > 0:
            canvas.itemconfig(timer_text_id, text=f"Hold for {timer_value:.1f} seconds")
            timer_value -= 0.1  # Reduce timer by 0.1 seconds (100ms)
            canvas.after(100, update_timer)
        else:
            # Time is up, finalize the click and close the app
            finalize_click()

def finalize_click():
    global x, y
    print(f"Final confirmed click at coordinates: ({x}, {y})")
    root.destroy()

def start_holding(event):
    global x, y, last_text_id, timer_value, is_holding
    x, y = event.x_root, event.y_root
    print(f"Mouse pressed at: ({x}, {y})")
    
    # Reset the timer value
    timer_value = hold_time
    is_holding = True
    
    # Delete previous text if it exists
    if last_text_id:
        canvas.delete(last_text_id)
    
    # Display new coordinates and the timer text
    last_text_id = canvas.create_text(x, y, text=f"({x}, {y})", fill="black", font=('Helvetica', 12, 'bold'))
    update_timer()

def stop_holding(event):
    global is_holding
    # Reset the holding status and the timer if the button is released early
    is_holding = False
    canvas.itemconfig(timer_text_id, text="")

def close_app(event):
    root.destroy()

# Create the main window
root = tk.Tk()
root.attributes('-fullscreen', True, "-alpha", 0.4)  # Set to full screen

# Create a canvas to draw on
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack()

# Instruction text
canvas.create_text(326, 90, text=f"Click and hold for 3 seconds to confirm \n(esc to exit)", fill="black", font=('Helvetica', 12, 'bold'))

# Timer display (initially empty)
timer_text_id = canvas.create_text(326, 140, text="", fill="black", font=('Helvetica', 16, 'bold'))

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

print(f"Screen dimensions: {screen_width}x{screen_height}")

# Bind the mouse click and release events
root.bind("<Button-1>", start_holding)  # Start holding
root.bind("<ButtonRelease-1>", stop_holding)  # Stop holding if released early

# Bind the Esc key to exit the application
root.bind("<Escape>", close_app)

# Start the main loop
root.mainloop()
