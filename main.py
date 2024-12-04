from tkinter import *
import math
import pygame
from tkinter import messagebox
import random
import sqlite3

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 1
SHORT_BREAK_MIN = 1
LONG_BREAK_MIN = 20
reps = 0
timer = None

# Initialize pygame mixer for sound
pygame.mixer.init()

# ---------------------------- DATABASE SETUP ------------------------------- #
# Connect to SQLite database (it will create the database file if it doesn't exist)
conn = sqlite3.connect('pomodoro.db')
c = conn.cursor()

# Create table for user credentials
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT,
        password TEXT
    )
''')
conn.commit()

# ---------------------------- TIMER FUNCTIONS ------------------------------- #
def reset_timer():
    global timer
    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="timer")
    check_marks.config(text="")
    motivation_label.config(text="")
    global reps
    reps = 0

def start_timer():
    global reps
    reps += 1

    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    if reps % 8 == 0:
        count_down(long_break_sec)
        title_label.config(text="long Break", fg=RED)
    elif reps % 2 == 0:
        count_down(short_break_sec)
        title_label.config(text="short Break", fg=PINK)
    else:
        count_down(work_sec)
        title_label.config(text="work", fg=GREEN)

def count_down(count):
    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        global timer
        timer = window.after(1000, count_down, count - 1)
    else:
        sound()  # Play sound when timer ends
        motivationQuotes()  # Show motivational quote
        start_timer()
        marks = ""
        work_sessions = math.floor(reps / 2)
        for _ in range(work_sessions):
            marks += "✔"
        check_marks.config(text=marks)

def sound():
    # Play a sound for 5 seconds
    pygame.mixer.music.load("kitchen-timer-33043.mp3") 
    pygame.mixer.music.play(-1)  # Loop the sound
    window.after(5000, stop_sound)  # Stop after 5 seconds

def stop_sound():
    pygame.mixer.music.stop()  # Stop the sound playback

def motivationQuotes():
    # Display a motivational quote in the UI
    quotes = [
        "You can do it!",
        "Stay focused and productive!",
        "Believe in yourself!",
        "Great job, keep going!",
        "Success is just around the corner!"
    ]
    quote = random.choice(quotes)
    motivation_label.config(text=quote)

# ---------------------------- USER AUTHENTICATION ------------------------------- #
def sign_up():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username already exists
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    user = c.fetchone()
    if user:
        messagebox.showerror("Error", "Username already exists.")
    else:
        # Insert new user into the database
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", "Sign up successful! Please log in.")
        show_login_ui()  # Correctly switch to the login UI

def login():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username and password match
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()

    if user:
        messagebox.showinfo("Success", "Login successful!")
        show_timer_ui()  # Show the Pomodoro Timer UI after login
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# ---------------------------- EXIT FEATURE ------------------------------- #
def exit_app():
    # Create a window with motivational quotes
    motivational_quotes = [
        "Great job today! Stay focused and come back tomorrow!",
        "Success is just a click away, see you tomorrow!",
        "You’re doing awesome! Let’s continue tomorrow!",
        "Keep pushing yourself, tomorrow is another day to achieve!",
        "One step at a time, see you tomorrow for more success!"
    ]
    
    quote = random.choice(motivational_quotes)

    # Hide the timer UI and show the exit motivational page
    for widget in window.winfo_children():
        widget.grid_forget()
    
    exit_message_label = Label(window, text="You're doing great!", font=(FONT_NAME, 30), fg=GREEN, bg=YELLOW)
    exit_message_label.grid(column=1, row=0)
    
    motivational_label = Label(window, text=quote, font=(FONT_NAME, 20), fg=GREEN, bg=YELLOW)
    motivational_label.grid(column=1, row=1)

    exit_button = Button(window, text="Exit", command=window.quit, font=(FONT_NAME, 15))
    exit_button.grid(column=1, row=2)

    return_button = Button(window, text="Return Tomorrow", command=window.quit, font=(FONT_NAME, 15))
    return_button.grid(column=1, row=3)

# ---------------------------- UI SETUP ------------------------------- #

def show_login_ui():
    # Clear current window
    for widget in window.winfo_children():
        widget.grid_forget()

    # Create the login UI elements
    login_label = Label(window, text="Login", font=(FONT_NAME, 40), fg=GREEN, bg=YELLOW)
    login_label.grid(column=1, row=0)

    global username_entry, password_entry
    username_label = Label(window, text="Username", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20))
    username_label.grid(column=1, row=1)

    username_entry = Entry(window, font=(FONT_NAME, 15))
    username_entry.grid(column=1, row=2)

    password_label = Label(window, text="Password", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20))
    password_label.grid(column=1, row=3)

    password_entry = Entry(window, font=(FONT_NAME, 15), show="*")
    password_entry.grid(column=1, row=4)

    login_button = Button(window, text="Login", command=login, font=(FONT_NAME, 15))
    login_button.grid(column=1, row=5)

    signup_button = Button(window, text="Sign up", command=show_signup_ui, font=(FONT_NAME, 15))
    signup_button.grid(column=1, row=6)

def show_signup_ui():
    # Clear current window
    for widget in window.winfo_children():
        widget.grid_forget()

    # Create the sign-up UI elements
    signup_label = Label(window, text="Sign Up", font=(FONT_NAME, 40), fg=GREEN, bg=YELLOW)
    signup_label.grid(column=1, row=0)

    global username_entry, password_entry
    username_label = Label(window, text="Username", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20))
    username_label.grid(column=1, row=1)

    username_entry = Entry(window, font=(FONT_NAME, 15))
    username_entry.grid(column=1, row=2)

    password_label = Label(window, text="Password", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 20))
    password_label.grid(column=1, row=3)

    password_entry = Entry(window, font=(FONT_NAME, 15), show="*")
    password_entry.grid(column=1, row=4)

    signup_button = Button(window, text="Sign Up", command=sign_up, font=(FONT_NAME, 15))
    signup_button.grid(column=1, row=5)

    login_button = Button(window, text="Login", command=show_login_ui, font=(FONT_NAME, 15))
    login_button.grid(column=1, row=6)

def show_timer_ui():
    # Clear current window
    for widget in window.winfo_children():
        widget.grid_forget()

    # Create Pomodoro Timer UI
    global title_label, canvas, timer_text, motivation_label, tomato_img, check_marks
    title_label = Label(window, text="timer", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 40))
    title_label.grid(column=1, row=0)

    canvas = Canvas(window, width=200, height=224, bg=YELLOW, highlightthickness=0)
    
    # Ensure the tomato image is loaded and retained
    tomato_img = PhotoImage(file="tomato.png")
    canvas.create_image(100, 112, image=tomato_img)  # Use the loaded image variable
    timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
    canvas.grid(column=1, row=1)

    start_button = Button(window, text="Start", highlightthickness=0, command=start_timer)
    start_button.grid(column=0, row=2)

    reset_button = Button(window, text="Reset", highlightthickness=0, command=reset_timer)
    reset_button.grid(column=2, row=2)

    check_marks = Label(fg=GREEN, bg=YELLOW)
    check_marks.grid(column=1, row=3)

    # Add motivation quote label
    motivation_label = Label(window, fg=GREEN, bg=YELLOW, font=(FONT_NAME, 15))
    motivation_label.grid(column=1, row=4)

    exit_button = Button(window, text="Exit", highlightthickness=0, command=exit_app)
    exit_button.grid(column=1, row=5)

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

show_login_ui()  # Start by showing the login UI
window.mainloop()
