from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
import os
import json
from datetime import datetime

app = FastAPI()

# Enable CORS for frontend
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
    """Serve the HTML diary frontend."""
    html_path = os.path.join(os.path.dirname(__file__), "t1.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Diary App Backend Running</h1>"

# -------- API Routes --------
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
    highlighted = []
    for date_str in data:
        if data[date_str].strip():
            try:
                d, m, y = date_str.split("-")
                highlighted.append(f"{y}-{m}-{d}")  # ISO format
            except:
                pass
    return {"dates": highlighted}
