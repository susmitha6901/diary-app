from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import subprocess
import sys
import os
import json

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "diary.json"

# -------- Utility Functions --------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

# -------- Serve Frontend --------
@app.get("/", response_class=HTMLResponse)
def serve_ui():
    html_path = os.path.join(os.path.dirname(__file__), "t1.html")
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()

# -------- API Routes --------
@app.get("/open-diary")
def open_diary():
    """Launch the Tkinter diary app."""
    try:
        script_path = os.path.join(os.path.dirname(__file__), "diary.py")
        subprocess.Popen([sys.executable, script_path])
        return {"status": "success", "message": "Diary app opened successfully"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/entries/{date}")
def get_entry(date: str):
    """Get diary entry for a specific date (dd-mm-yyyy)."""
    data = load_data()
    return {"date": date, "entry": data.get(date, "")}

@app.post("/entries")
def save_entry(entry_data: dict = Body(...)):
    """Save or update diary entry."""
    date = entry_data.get("date")
    text = entry_data.get("text", "")
    if not date or not isinstance(date, str):
        return {"status": "error", "message": "Valid date is required"}
    data = load_data()
    data[date] = text
    save_data(data)
    return {"status": "success", "message": f"Entry for {date} saved."}

@app.get("/highlighted-dates")
def get_highlighted_dates():
    """Return all dates that have entries."""
    data = load_data()
    # Convert dd-mm-yyyy to yyyy-mm-dd for frontend
    highlighted = []
    for date_str in data:
        if data[date_str].strip():
            d, m, y = date_str.split("-")
            highlighted.append(f"{y}-{m}-{d}")
    return {"dates": highlighted}
