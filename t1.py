import tkinter as tk
from tkinter import messagebox
from tkcalendar import Calendar
import json
import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import hashlib

# File to store diary entries
DATA_FILE = "diary.json"

# Load data from JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# Save data to JSON
def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# Update calendar highlights
def highlight_dates():
    cal.calevent_remove('all')  # Clear previous highlights

    for date_str, note in diary_data.items():
        if note.strip():  # Only highlight if there is a note
            try:
                # Convert diary date (dd-mm-yyyy) to datetime.date
                date_obj = datetime.strptime(date_str, "%d-%m-%Y").date()
                cal.calevent_create(date_obj, "Entry", "has_entry")
            except Exception as e:
                print("Error parsing date:", e)

    # Configure tag appearance
    cal.tag_config("has_entry", background="green", foreground="white")



# Save diary entry
def save_entry():
    date_str = cal.get_date()
    text = text_box.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Empty Entry", "Please write something before saving!")
        return
    diary_data[date_str] = text
    save_data(diary_data)
    highlight_dates()
    messagebox.showinfo("Saved", f"Entry for {date_str} saved successfully!")

# Load diary entry for selected date
def load_entry(event=None):
    date_str = cal.get_date()
    text_box.delete("1.0", tk.END)
    if date_str in diary_data:
        text_box.insert(tk.END, diary_data[date_str])

# Toggle strike-through on selected text
def strike_text():
    try:
        # Get the selected text indices
        start = text_box.index(tk.SEL_FIRST)
        end = text_box.index(tk.SEL_LAST)
    except tk.TclError:
        messagebox.showwarning("No Selection", "Please select text to strike/unstrike!")
        return

    # Check if selection already has 'strike' tag
    if "strike" in text_box.tag_names(tk.SEL_FIRST):
        # Remove strike-through
        text_box.tag_remove("strike", start, end)
    else:
        # Apply strike-through
        text_box.tag_add("strike", start, end)
        text_box.tag_config("strike", overstrike=1, foreground="black")  # Optional: red color for visibility


# Toggle calendar visibility
def toggle_calendar():
    global calendar_visible
    if calendar_visible:
        cal.pack_forget()
        toggle_btn.config(text="📅 Show Calendar")
    else:
        cal.pack()
        toggle_btn.config(text="📅 Hide Calendar")
    calendar_visible = not calendar_visible

# Initialize data
diary_data = load_data()
calendar_visible = True

# GUI setup
root = tk.Tk()
root.title("My Personal Diary")
root.geometry("550x650")
root.config(bg="#f8f5ec")

# Title
title_label = tk.Label(root, text="My Personal Diary", font=("Segoe Script", 20, "bold"), bg="#f8f5ec")
title_label.pack(pady=5)

# Calendar Frame
calendar_frame = tk.Frame(root, bg="#f8f5ec")
calendar_frame.pack(pady=5)

# Toggle Button
toggle_btn = tk.Button(calendar_frame, text="📅 Hide Calendar", command=toggle_calendar, bg="#e6e6e6", font=("Segoe Script", 12))
toggle_btn.pack(pady=5)

# Calendar Widget
cal = Calendar(calendar_frame, selectmode="day", date_pattern="dd-mm-yyyy", font=("Segoe Script", 10))
cal.pack()
cal.bind("<<CalendarSelected>>", load_entry)

# Apply highlights
highlight_dates()

# Text Box
text_box = tk.Text(root, wrap="word", font=("Segoe Script", 14), height=15, width=50)
text_box.pack(pady=10)

# Buttons Frame
btn_frame = tk.Frame(root, bg="#f8f5ec")
btn_frame.pack(pady=10)

save_btn = tk.Button(btn_frame, text="💾 Save Entry", command=save_entry, bg="#4CAF50", fg="white", font=("Segoe Script", 12, "bold"))
save_btn.grid(row=0, column=0, padx=5)

strike_btn = tk.Button(btn_frame, text="✏ Strike/Unstrike Text", command=strike_text, bg="#FF9800", fg="white", font=("Segoe Script", 12, "bold"))
strike_btn.grid(row=0, column=1, padx=5)

root.mainloop()
